import streamlit as st
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
</style>
""", unsafe_allow_html=True)
st.title("🚗 Ride Sharing System")

start = st.text_input("Start Location")
end = st.text_input("Destination")
start = st.text_input("Start Location")
end = st.text_input("Destination")

if start and end:
    st.success(f"Showing route from {start} → {end}")

if st.button("Find Ride"):
    st.success("Matched with users on same route ✅")

    st.write("👤 User1: Same route")
    st.write("👤 User2: 80% route match")

    st.info("Carpool reduces traffic by 30% 🌱")