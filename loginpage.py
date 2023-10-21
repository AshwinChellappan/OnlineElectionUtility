import streamlit as st
import sqlite3
import hashlib


role = None
username = None



def login():
    global role, username
    # Create a connection to the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create a table to store user details (if it doesn't exist)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            role TEXT
        )
    ''')
    conn.commit()

    # Streamlit app title
    # st.title("User Login")

    # Login or Registration choice
    login_or_register = st.radio("Login / Register", ("Login", "Register"))

    if login_or_register == "Register":
        st.header("User Registration")

        # Input fields for registration
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Admin", "Candidate", "Voter"])
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Button to submit registration
        if st.button("Register"):
            # Check if the user already exists
            existing_user = cursor.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()

            if existing_user:
                st.error("User already exists. Please login.")
            else:
                # Insert the user data into the database
                cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                               (username, hashed_password, role))
                conn.commit()
                st.success("Registration successful! Please login.")

    if login_or_register == "Login":
        st.header("User Login")

        # Input fields for login
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Button to submit login
        if st.button("Login"):
            # Check if the user exists in the database
            user = cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                                  (username, hashed_password)).fetchone()

            if user:
                role = user[3]
                st.success(f"Welcome, {username}! Your role is {user[3]}.")
            else:
                st.error("Invalid username or password. Please try again.")

    # Close the database connection
    conn.close()
    return role, username


if __name__ == '__main__':
    role, username = login()
    print(f"Role: {role}")
