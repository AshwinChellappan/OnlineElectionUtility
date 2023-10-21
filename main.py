import streamlit as st
import username as username

from AdminCandidatelist import adminCandidatureApprove
from candidate import candidateRegistration
from castvote import castVote
from loginpage import login
import getpass as gt

if "page" not in st.session_state:
    st.session_state.page = 0

def nextpage(): st.session_state.page += 1
def restart(): st.session_state.page = 0
def adminCandidate(): st.session_state.page = 4
def candidateRegister(): st.session_state.page = 3
def homepage(): st.session_state.page = 0
def castVoting(): st.session_state.page = 2

global userName
placeholder = st.empty()
# st.button("Next",on_click=nextpage,disabled=(st.session_state.page > 4))
st.button("Go to Home Page", on_click=homepage, disabled=(st.session_state.page > 4))

if st.session_state.page == 0:
    # Replace the placeholder with some text:
    result = login()
    if result is not None:
        role, username = result[0], result[1]
        print("Username--->" + username)
        print("Role--->" + role)
        userName=username
        if role == 'Admin':
            # placeholder.text(f"Hello, this is page {st.session_state.page}")
            print("Inside Admin loop")
            st.button("CandidateList", on_click=adminCandidate, disabled=(st.session_state.page > 4))
        elif role == 'Candidate':
            st.button("CandidateRegistration", on_click=candidateRegister, disabled=(st.session_state.page > 4))
        elif role == 'Voter':
            print("Inside voter loop")
            st.button("Cast Vote", on_click=castVoting(), disabled=(st.session_state.page > 4))
    else:
        st.write("Login failed. Handle the error or provide a suitable message")

elif st.session_state.page == 1:
    # Replace the text with a chart:
    placeholder.line_chart({"data": [1, 5, 2, 6]})

elif st.session_state.page == 2:
    with placeholder.container():
        print("Inside vote block"+username)
        castVote(username)
        st.write("This is one element")
        st.write("This is another")
        st.metric("Page:", value=st.session_state.page)

elif st.session_state.page == 3:
    # placeholder.markdown(r"$f(x) = \exp{\left(x^🐈\right)}$")
    print("Inside Candidate Registration block")
    with placeholder.container():
        candidateRegistration()

elif st.session_state.page == 4:
    print("Inside Candidature Approval")
    # Replace the chart with several elements:
    with placeholder.container():
        adminCandidatureApprove()

else:
    with placeholder:
        st.write("This is the end")
        st.button("Restart", on_click=restart)

