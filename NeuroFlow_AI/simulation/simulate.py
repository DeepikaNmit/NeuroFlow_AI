import streamlit as st
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
</style>
""", unsafe_allow_html=True)
def simulate_reduction(traffic, adoption_rate):
    reduction = traffic * (adoption_rate * 0.4)
    return traffic - reduction