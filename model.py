import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Load dataset
df = pd.read_csv("dataset.csv")

# Features / target
X = df.drop(["target_corpus", "risk_label"], axis=1)
y = df["target_corpus"]

# Categorical columns
categorical_cols = ["risk_tolerance", "goal_type"]
numeric_cols = [col for col in X.columns if col not in categorical_cols]

# Preprocess
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", "passthrough", numeric_cols)
    ]
)

# Model pipeline
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=100,
        random_state=42
    ))
])

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
preds = model.predict(X_test)

# Accuracy
mae = mean_absolute_error(y_test, preds)
print("Model trained successfully!")
print("Mean Absolute Error:", round(mae, 2))

# Save model
joblib.dump(model, "retire_model.pkl")
print("Model saved as retire_model.pkl")