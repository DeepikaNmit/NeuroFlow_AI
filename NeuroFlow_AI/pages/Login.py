import streamlit as st

st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
</style>
""", unsafe_allow_html=True)
st.title("🔐 NeuroFlow AI Login")

menu = ["Login", "Sign Up"]
choice = st.selectbox("Select Option", menu)

if choice == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "123":
            st.success("Login Successful ✅")
        else:
            st.error("Invalid credentials ❌")

elif choice == "Sign Up":
    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")

    if st.button("Sign Up"):
        st.success("Account Created ✅ (Demo Mode)")