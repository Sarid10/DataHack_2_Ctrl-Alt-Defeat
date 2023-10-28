import streamlit as st

def main():
    st.title("Login Page")

    # Create input fields for username and password
    username = st.text_input("Username",)
    password = st.text_input("Password", type="password")

    # Check if the login button is pressed
    if st.button("Login"):
        # Hardcoded username and password for demonstration purposes
        if username == "demo" and password == "demo123":
            st.success("Login Successful")
            # Add your app logic or redirect to another page here
        else:
            st.error("Invalid Username or Password")

if __name__ == "__main__":
    main()


