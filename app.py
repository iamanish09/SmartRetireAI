import streamlit as st
import joblib
import pandas as pd
from reportlab.pdfgen import canvas

model = joblib.load("retire_model.pkl")

st.set_page_config(page_title="SmartRetire AI", page_icon="💰", layout="wide")

st.title("💰 SmartRetire AI")
st.caption("AI-powered retirement planning assistant")

with st.sidebar:
    st.header("User Profile")
    age = st.slider("Age", 20, 60, 30)
    salary = st.number_input("Monthly Salary (₹)", 10000, 500000, 50000)
    expenses = st.number_input("Monthly Expenses (₹)", 5000, 300000, 20000)
    savings = st.number_input("Current Savings (₹)", 0, 10000000, 100000)
    dependents = st.slider("Dependents", 0, 5, 1)
    risk = st.selectbox("Risk Tolerance", ["Low", "Medium", "High"])
    goal = st.selectbox("Goal Type", ["Normal", "Luxury", "Aggressive"])
    expected_return = st.slider("Expected Return (%)", 5.0, 15.0, 10.0)
    inflation = st.slider("Inflation Rate (%)", 3.0, 10.0, 6.0)
    retirement_age = st.slider("Desired Retirement Age", age + 5, 70, 60)

if st.button("🚀 Analyze Retirement Plan"):
    input_df = pd.DataFrame([{
        "age": age,
        "monthly_salary": salary,
        "monthly_expenses": expenses,
        "current_savings": savings,
        "dependents": dependents,
        "risk_tolerance": risk,
        "expected_return": expected_return,
        "inflation_rate": inflation,
        "retirement_goal_age": retirement_age,
        "goal_type": goal
    }])

    corpus = model.predict(input_df)[0]
    monthly_save_target = max((salary - expenses) * 0.30, 1000)
    years_left = retirement_age - age

    # Safety score
    savings_score = min((savings / 1000000) * 20, 30)
    income_score = min(((salary - expenses) / salary) * 40, 40)
    time_score = min(years_left * 1.2, 20)
    expense_score = max(10 - (expenses / salary) * 10, 0)

    score = int(savings_score + income_score + time_score + expense_score)
    score = min(score, 100)
    if score >= 70:
        risk_meter = "🟢 Low Risk"
    elif score >= 35:
        risk_meter = "🟡 Medium Risk"
    else:
        risk_meter = "🔴 High Risk"

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Required Corpus", f"₹{corpus:,.0f}")

    with c2:
        st.metric("Monthly Saving Target", f"₹{monthly_save_target:,.0f}")

    with c3:
        st.metric("Years Left", years_left)

    st.subheader("Retirement Safety Score")
    st.progress(score / 100)
    st.write(f"{score}/100")

    st.subheader("Risk Analysis")
    st.info(risk_meter)

    # Chart
    if salary > expenses:
        save_pct = ((salary - expenses) / salary) * 100
        expense_pct = (expenses / salary) * 100

        chart = pd.DataFrame({
            "Category": ["Expenses", "Saving Potential"],
            "Amount": [expense_pct, save_pct]
        }).set_index("Category")

        st.subheader("Income Split")
        st.bar_chart(chart)

    # AI recommendation
    emergency = expenses * 6

    st.subheader("🤖 AI Recommendation")
    st.write(f"• Save at least ₹{monthly_save_target:,.0f}/month")
    st.write(f"• Build emergency fund of ₹{emergency:,.0f}")
    st.write("• Consider SIP / Mutual Fund investing")
    st.write("• Review expenses every 6 months")

    # PDF generation
    pdf_name = "retirement_report.pdf"
    c = canvas.Canvas(pdf_name)
    c.drawString(100, 800, "SmartRetire AI - Retirement Report")
    c.drawString(100, 760, f"Required Corpus: ₹{corpus:,.0f}")
    c.drawString(100, 740, f"Monthly Saving Target: ₹{monthly_save_target:,.0f}")
    c.drawString(100, 720, f"Safety Score: {score}/100")
    c.drawString(100, 700, f"Risk: {risk_meter}")
    c.save()

    with open(pdf_name, "rb") as file:
        st.download_button(
            "📄 Download Retirement Report",
            file,
            file_name=pdf_name
        )