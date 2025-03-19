import streamlit as st
import requests
import time

API_URL = "http://api:8000"

# Streamlit UI Configuration
st.set_page_config(page_title="📄 AI-Powered PDF Chatbot", layout="wide")

# Page Title
st.title("📄 AI-Powered PDF Chatbot 🤖")

# Model Selection Dropdown
available_models = ["gemini-1.0-pro", "gemini-2.0-flash-lite", "gemini-1.5-pro"]
selected_model = st.selectbox("Select AI Model:", available_models)

# Sidebar - PDF Upload
st.sidebar.header("📂 Upload PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("📤 Uploading PDF..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        response = requests.post(f"{API_URL}/upload/", files=files)
        time.sleep(2)  # Simulated wait time
    if response.status_code == 200:
        st.sidebar.success("✅ File uploaded successfully!")
    else:
        st.sidebar.error("❌ Error uploading file!")

# Chat Section
st.subheader("💬 Chat with AI")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.text_input("Ask a Question:")

if st.button("Ask"):
    with st.spinner("⏳ Retrieving response..."):
        response = requests.get(f"{API_URL}/ask/", params={"question": question, "model": selected_model})

    if response.status_code == 200:
        answer = response.json()["answer"]
        st.session_state.chat_history.append({"question": question, "answer": answer})
    else:
        st.error("❌ Error retrieving response from API!")

# Chat History Display
if st.session_state.chat_history:
    st.subheader("📝 Chat History")
    for chat in st.session_state.chat_history:
        with st.container():
            st.write(f"**📢 Question:** {chat['question']}")
            st.success(f"**🤖 Answer:** {chat['answer']}")
