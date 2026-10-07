import streamlit as st

from peer_lending_backend.src.routers.loans import router as loan_router

st.set_page_config(page_title="Pulse Risk Engine", layout="wide")
st.title("Pulse Lending Risk Engine")

st.caption(f"Loan routes served by Ancla API: {', '.join(sorted(r.path for r in loan_router.routes))}")

st.subheader("Pending loans")
try:
    pending = next(r for r in loan_router.routes if r.path == "/api/loans/pending").endpoint()
    st.dataframe(pending)
except Exception as exc:
    st.error(f"Could not load loans: {exc}")
