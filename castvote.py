import streamlit as st
import sqlite3

def create_or_connect_db():
    conn = sqlite3.connect('candidates.db')
    cursor = conn.cursor()

    # Create a table to store candidate details (if it doesn't exist)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            candidate_id INTEGER,
            FOREIGN KEY (candidate_id) REFERENCES candidates (id)
        )
    ''')

    # Create a table to store the users who have voted
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS voters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT
        )
    ''')

    conn.commit()
    return conn, cursor

def has_user_voted(user_id, cursor):
    # Check if the user has already voted
    user = cursor.execute("SELECT * FROM voters WHERE user_id=?", (user_id,)).fetchone()
    return user is not None

def castVote(user_id):
    conn, cursor = create_or_connect_db()

    if has_user_voted(user_id, cursor):
        st.warning("You have already cast your vote. You cannot vote again.")
        return

    st.subheader("Cast Your Vote")

    # Retrieve the list of approved candidates
    approved_candidates = cursor.execute("SELECT * FROM candidates WHERE approved=1").fetchall()

    if not approved_candidates:
        st.warning("No approved candidates available for voting.")
        return

    # Use radio buttons for voting
    selected_candidate = st.radio("Select a candidate to vote for", [f"{candidate[1]} ({candidate[4]} years old)" for candidate in approved_candidates])

    if st.button("Cast Your Vote"):
        # Extract the selected candidate's ID
        selected_candidate_id = approved_candidates[[f"{candidate[1]} ({candidate[4]} years old)" for candidate in approved_candidates].index(selected_candidate)][0]

        # Insert the vote into the database
        cursor.execute("INSERT INTO votes (user_id, candidate_id) VALUES (?, ?)", (user_id, selected_candidate_id))
        conn.commit()
        st.success("Your vote has been cast successfully.")

        # Add the user to the voters table to track that they have voted
        cursor.execute("INSERT INTO voters (user_id) VALUES (?)", (user_id,))
        conn.commit()

    # Close the database connection
    conn.close()

if __name__ == '__main__':
    st.title("Candidate Voting System")
    user_id = "name1"  # Replace with the actual user ID
    castVote(user_id)
