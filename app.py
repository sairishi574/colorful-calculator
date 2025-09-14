import streamlit as st
import math, operator, re

st.title("🎨 Colourful Calculator (Stack-based)")

# Same tokenize, shunting_yard, eval_rpn, safe_eval functions here...

expr = st.text_input("Enter expression:")
if st.button("Evaluate"):
    try:
        result = safe_eval(expr)
        st.success(f"Result: {result}")
    except Exception as e:
        st.error(f"Error: {e}")
