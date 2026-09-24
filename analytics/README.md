## Module 2 - Analytics & Machine Learning

Module 2 performs exploratory data analysis, machine learning model development, evaluation, and residual analysis using the Titanic dataset prepared in Module 1.

### Exploratory Data Analysis

The EDA includes:

- Data distribution analysis
- Survival analysis by passenger class
- Survival analysis by gender
- Fare distribution
- Correlation analysis
- Feature relationships and visualizations

### Machine Learning Classification

The following classification models were developed and evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- Tuned Random Forest

The models were evaluated using:

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix
- ROC Curve
- ROC-AUC

The tuned Random Forest achieved a ROC-AUC score of approximately **0.8362** on the test dataset.

### Feature Importance

Feature importance was analyzed using the tuned Random Forest model.

The important features included:

- sex_male
- fare
- age
- pclass
- sibsp
- parch
- embarked_S
- embarked_Q

### Regression Analysis

A Random Forest Regression model was developed to predict passenger fare.

The regression model was evaluated using:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score

Residual analysis was also performed using a residuals-versus-predicted-values plot.

### Saved Models and Results

The following files are generated as part of Module 2:

- `analytics/random_forest_tuned.joblib`
- `analytics/random_forest_regressor.joblib`
- `analytics/model_results.csv`

### Running Module 2

Navigate to the project directory and open the modeling notebook:

```text
analytics/02_modeling.ipynb