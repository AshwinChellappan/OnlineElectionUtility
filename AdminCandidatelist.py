import streamlit as st
import sqlite3
import pandas as pd

def adminCandidatureApprove():
    # Create a connection to the SQLite database
    conn = sqlite3.connect('candidates.db')

    # Streamlit app title
    st.title("Candidate Data Editor and Approver")

    # Retrieve data from the database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates")
    data = cursor.fetchall()

    # Convert the data to a Pandas DataFrame for easier editing
    df = pd.DataFrame(data, columns=["ID", "Name", "Email", "Phone", "DOB", "Age", "Skills", "Documents", "Approved"])

    # Display the data in a Streamlit table
    st.write("Candidate Data:")
    st.write(df)

    # Edit and approve data
    selected_id = st.number_input("Enter the ID of the candidate to edit and approve:")
    if selected_id > 0:
        candidate_data = df[df['ID'] == selected_id]

        # Display the candidate data for editing
        st.write("Candidate Data for Editing:")
        st.write(candidate_data)

        # Allow editing and approval
        new_name = st.text_input("Name", candidate_data["Name"].values[0])
        new_email = st.text_input("Email", candidate_data["Email"].values[0])
        new_phone = st.text_input("Phone", candidate_data["Phone"].values[0])
        new_skills = st.text_area("Skills", candidate_data["Skills"].values[0])
        approval = st.checkbox("Approve")

        if st.button("Update Data"):
            # Update the data in the DataFrame
            df.loc[df['ID'] == selected_id, ["Name", "Email", "Phone", "Skills", "Approved"]] = [new_name, new_email, new_phone, new_skills, approval]

            # Update the database
            cursor.execute("UPDATE candidates SET name=?, email=?, phone=?, skills=?, approved=? WHERE id=?",
                           (new_name, new_email, new_phone, new_skills, approval, selected_id))
            conn.commit()

    # Close the database connection
    conn.close()
