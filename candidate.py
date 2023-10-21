import streamlit as st
import sqlite3
from datetime import datetime
import json  # Import the JSON module


def candidateRegistration():
    # Create a connection to an SQLite database
    conn = sqlite3.connect('candidates.db')
    cursor = conn.cursor()

    # Create a table to store candidate data (if it doesn't exist)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            dob DATE,
            age INTEGER,
            skills TEXT,
            documents TEXT,  -- Store serialized documents as text
            approved INTEGER  -- 1 for approved, 0 for not approved
        )
    ''')
    conn.commit()

    print("Inside Candidate class")
    # Streamlit app title
    st.title("Candidate Registration")

    # Input fields for candidate information
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    dob = st.date_input("Date of Birth")
    skills = st.text_area("Skills")

    # File uploader for multiple documents
    documents = st.file_uploader("Upload Documents (PDF, Word, etc.)", type=["pdf", "docx", "doc", "txt"],
                                 accept_multiple_files=True)

    # Button to submit the registration
    if st.button("Register"):
        # Calculate age based on the Date of Birth
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        # Serialize the list of documents to JSON
        document_data = [document.read() for document in documents] if documents else []
        document_data = json.dumps(document_data)

        # Insert the candidate data into the database, including serialized documents
        cursor.execute(
            "INSERT INTO candidates (name, email, phone, dob, age, skills, documents) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, email, phone, dob, age, skills, document_data))
        conn.commit()
        st.success("Registration successful!")

    # Close the database connection
    conn.close()


if __name__ == '__main__':
    candidateRegistration()
