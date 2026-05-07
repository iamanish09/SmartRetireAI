import pandas as pd
import numpy as np
import random

# Make results repeatable
np.random.seed(42)

data = []
n = 10000

for _ in range(n):
    age = random.randint(21, 60)
    monthly_salary = random.randint(20000, 300000)
    monthly_expenses = random.randint(10000, int(monthly_salary * 0.8))
    current_savings = random.randint(0, 5000000)
    dependents = random.randint(0, 5)

    risk_tolerance = random.choice(["Low", "Medium", "High"])
    goal_type = random.choice(["Normal", "Luxury", "Aggressive"])

    expected_return = random.uniform(6, 14)
    inflation_rate = random.uniform(4, 8)
    retirement_goal_age = random.randint(max(age + 5, 45), 70)

    years_left = retirement_goal_age - age

    # Retirement corpus estimation
    annual_expense = monthly_expenses * 12
    target_corpus = annual_expense * 25 * ((1 + inflation_rate / 100) ** years_left)

    # Risk label logic
    savings_ratio = current_savings / (monthly_salary * 12 + 1)

    if savings_ratio > 2:
        risk_label = "Low"
    elif savings_ratio > 0.5:
        risk_label = "Medium"
    else:
        risk_label = "High"

    data.append([
        age,
        monthly_salary,
        monthly_expenses,
        current_savings,
        dependents,
        risk_tolerance,
        expected_return,
        inflation_rate,
        retirement_goal_age,
        goal_type,
        target_corpus,
        risk_label
    ])

columns = [
    "age",
    "monthly_salary",
    "monthly_expenses",
    "current_savings",
    "dependents",
    "risk_tolerance",
    "expected_return",
    "inflation_rate",
    "retirement_goal_age",
    "goal_type",
    "target_corpus",
    "risk_label"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("dataset.csv", index=False)

print("Dataset created successfully!")
print(df.head())