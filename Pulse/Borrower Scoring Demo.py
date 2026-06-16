import streamlit as st
import pandas as pd

# Demo borrower dataset
data = {
    "Borrower": ["Alice", "Bob", "Carlos", "Diana"],
    "Loan Amount": [5000, 12000, 8000, 15000],
    "Credit Score": [720, 650, 580, 700],
    "Risk Tier": ["Low", "Medium", "High", "Medium"],
    "Probability of Default (PD)": [0.05, 0.15, 0.35, 0.12],
    "Loan-to-Value (LTV)": [0.45, 0.70, 0.85, 0.60],
}

df = pd.DataFrame(data)

st.title("Pulse Lending – Borrower Scoring Demo")
st.write("This dashboard showcases borrower risk metrics for demo purposes.")

# Show table
st.dataframe(df)

# Highlight PD distribution
st.bar_chart(df.set_index("Borrower")["Probability of Default (PD)"])
