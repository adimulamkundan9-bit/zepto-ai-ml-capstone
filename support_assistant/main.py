import os
import json
from typing import TypedDict
from fastapi import FastAPI

import chromadb
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "chroma_db")

MOCK_LLM = os.getenv("MOCK_LLM", "1")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=DB_DIR)

collection = client.get_collection("zepto_policies")


prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
ROLE:
You are a Zepto customer support assistant.

CONTEXT:
Use only the Zepto policy information provided below.

{context}

TASK:
Answer the customer's question using the provided policy context.
If the answer is not present in the context, clearly state that the provided
policy context does not contain the answer.

FORMAT:
Return valid JSON with exactly these fields:
answer: string
sources: list of document or chunk IDs
confidence: number between 0 and 1

LENGTH:
Keep the answer concise and directly relevant to the customer's question.

NEGATIVE CONSTRAINT:
Do not answer using information that is not present in the provided context.
Do not invent or assume Zepto policies.

FEW-SHOT EXAMPLE:
Question: What is the delivery fee for an order below INR 149?
Context: Standard delivery is free on orders over INR 149; orders below this
threshold incur a flat INR 25 delivery fee.
Answer:
{{"answer":"Orders below INR 149 incur a flat INR 25 delivery fee.",
"sources":["doc_01"],"confidence":1.0}}

Customer Question:
{question}
"""
)


class SupportResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(ge=0, le=1)


class GraphState(TypedDict, total=False):
    query: str
    intent: str
    answer: str
    sources: list[str]
    confidence: float
    retrieved_documents: list[str]
    retrieved_ids: list[str]


def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0
    )


def classify_intent(state: GraphState):
    query = state["query"]

    if MOCK_LLM != "0":
        keywords = [
            "delivery",
            "return",
            "refund",
            "membership",
            "tracking",
            "cancel",
            "gift card",
            "support hours"
        ]

        query_lower = query.lower()

        if any(keyword in query_lower for keyword in keywords):
            intent = "policy_question"
        else:
            intent = "general_question"

        return {"intent": intent}

    llm = get_llm()

    prompt = f"""
Classify the following customer question into exactly one category:
policy_question
general_question

Use policy_question when the question concerns Zepto delivery, returns,
refunds, membership, tracking, cancellation, gift cards, or support.

Question:
{query}

Return only:
policy_question
or
general_question
"""

    response = llm.invoke(prompt)
    intent = response.content.strip()

    if intent not in ["policy_question", "general_question"]:
        intent = "general_question"

    return {"intent": intent}


def retrieve_and_answer(state: GraphState):
    query = state["query"]

    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    documents = results["documents"][0]
    ids = results["ids"][0]

    if MOCK_LLM != "0":
        top_chunk_snippet = documents[0][:200]

        answer = f"Based on the retrieved context: {top_chunk_snippet}"

        return {
            "answer": answer,
            "sources": ids,
            "confidence": 1.0,
            "retrieved_documents": documents,
            "retrieved_ids": ids
        }

    context_parts = []

    for document_id, document in zip(ids, documents):
        context_parts.append(
            f"Document ID: {document_id}\n{document}"
        )

    context = "\n\n".join(context_parts)

    prompt = prompt_template.format(
        context=context,
        question=query
    )

    llm = get_llm()

    for attempt in range(3):
        try:
            response = llm.invoke(prompt)
            raw_output = response.content

            parsed = json.loads(raw_output)
            validated = SupportResponse.model_validate(parsed)

            return {
                "answer": validated.answer,
                "sources": validated.sources,
                "confidence": validated.confidence,
                "retrieved_documents": documents,
                "retrieved_ids": ids
            }

        except Exception:
            prompt = f"""
The previous response failed JSON schema validation.

Return ONLY valid JSON with exactly:
{{
  "answer": "string",
  "sources": ["document_id"],
  "confidence": 0.0
}}

The confidence must be between 0 and 1.

Do not use information outside the provided context.

Context:
{context}

Question:
{query}
"""

    return {
        "answer": "ERROR: The real LLM response could not be validated.",
        "sources": ids,
        "confidence": 0.0,
        "retrieved_documents": documents,
        "retrieved_ids": ids
    }


def direct_answer(state: GraphState):
    query = state["query"]

    if MOCK_LLM != "0":
        return {
            "answer": "I can only answer questions about Zepto policies right now.",
            "sources": [],
            "confidence": 1.0
        }

    llm = get_llm()

    prompt = f"""
Answer the following question.

Return ONLY valid JSON with exactly:
{{
  "answer": "string",
  "sources": [],
  "confidence": 0.0
}}

Do not retrieve policy information.

Question:
{query}
"""

    for attempt in range(3):
        try:
            response = llm.invoke(prompt)
            parsed = json.loads(response.content)
            validated = SupportResponse.model_validate(parsed)

            return {
                "answer": validated.answer,
                "sources": [],
                "confidence": validated.confidence
            }

        except Exception:
            prompt = f"""
Your previous response failed validation.

Return ONLY valid JSON:
{{
  "answer": "string",
  "sources": [],
  "confidence": 0.0
}}

Question:
{query}
"""

    return {
        "answer": "ERROR: The real LLM response could not be validated.",
        "sources": [],
        "confidence": 0.0
    }


def route_intent(state: GraphState):
    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"


graph_builder = StateGraph(GraphState)

graph_builder.add_node("classify_intent", classify_intent)
graph_builder.add_node("retrieve_and_answer", retrieve_and_answer)
graph_builder.add_node("direct_answer", direct_answer)

graph_builder.set_entry_point("classify_intent")

graph_builder.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer"
    }
)

graph_builder.add_edge("retrieve_and_answer", END)
graph_builder.add_edge("direct_answer", END)

graph = graph_builder.compile()


def ask_question(query: str):
    result = graph.invoke({"query": query})

    response = SupportResponse(
        answer=result["answer"],
        sources=result.get("sources", []),
        confidence=result.get("confidence", 1.0)
    )

    return response
app = FastAPI(title="Zepto Support Assistant")


class AskRequest(BaseModel):
    query: str


@app.post("/ask", response_model=SupportResponse)
def ask(request: AskRequest):
    return ask_question(request.query)

if __name__ == "__main__":
    policy_result = ask_question(
        "What is the delivery fee for orders below INR 149?"
    )

    general_result = ask_question(
        "What is the capital of India?"
    )

    print("\nPolicy question:")
    print(policy_result.model_dump_json(indent=2))

    print("\nGeneral question:")
    print(general_result.model_dump_json(indent=2))