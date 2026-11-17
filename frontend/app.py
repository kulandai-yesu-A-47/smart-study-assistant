
import streamlit as st
import requests

st.set_page_config(
    page_title="AI Smart Study Assistant",
    page_icon="📚",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

st.title("📚 AI Smart Study Assistant")
st.write("Your personal AI-powered learning assistant.")

st.sidebar.title("Features")

feature = st.sidebar.selectbox(
    "Choose a feature",
    [
        "PDF Summarizer",
        "Document Chatbot",
        "Quiz Generator",
        "Study Planner",
        "Learning Assistant"
    ]
)

st.header(feature)

if feature == "PDF Summarizer":

    st.write("Upload your PDF and get an AI-generated summary.")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"]
    )

    if st.button("Summarize PDF"):
        if uploaded_file is not None:

            with st.spinner("Generating summary..."):

                response = requests.post(
                    f"{API_URL}/summarize-pdf",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf"
                        )
                    }
                )

            if response.status_code == 200:
                st.success("Summary generated successfully!")
                st.write(response.json()["summary"])
            else:
                st.error(response.text)

        else:
            st.warning("Please upload a PDF file.")


if feature == "Document Chatbot":

    st.write("Upload a PDF and ask questions about its content.")

    uploaded_file = st.file_uploader(
        "Upload your document",
        type=["pdf"],
        key="chat_pdf"
    )

    if st.button("Process Document"):
        if uploaded_file is not None:

            with st.spinner("Processing document..."):

                response = requests.post(
                    f"{API_URL}/upload-pdf",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf"
                        )
                    }
                )

            if response.status_code == 200:
                st.session_state["document_ready"] = True
                st.session_state["document_id"] = response.json()["document_id"]
                st.success("Document uploaded successfully!")
            else:
                st.error(response.text)

        else:
            st.warning("Please upload a PDF file.")

    if st.session_state.get("document_ready", False):

        question = st.text_input("Ask a question about your document")

        if st.button("Ask AI"):
            if question.strip():

                with st.spinner("Finding the answer..."):

                    response = requests.post(
                        f"{API_URL}/chat-with-document",
                        json={
                            "question": question,
                            "document_id": st.session_state["document_id"]
                        }
                    )

                if response.status_code == 200:
                    st.write("### AI Answer")
                    st.write(response.json()["answer"])
                else:
                    st.error(response.text)


if feature == "Quiz Generator":

    st.write("Generate multiple-choice questions using AI.")

    study_text = st.text_area(
        "Enter your study material",
        height=200,
        placeholder="Paste your study content here..."
    )

    if st.button("Generate Quiz"):

        if study_text.strip():

            with st.spinner("Generating quiz..."):

                response = requests.post(
                    f"{API_URL}/generate-quiz",
                    json={"text": study_text}
                )

            if response.status_code == 200:
                st.success("Quiz generated successfully!")
                st.write(response.json()["quiz"])
            else:
                st.error(response.text)

        else:
            st.warning("Please enter some study material.")


if feature == "Study Planner":

    st.write("Create a personalized AI study plan.")

    subject = st.text_input("Enter subject")

    hours = st.number_input(
        "Available study hours per day",
        min_value=1,
        max_value=12,
        value=2
    )

    days = st.number_input(
        "Number of study days",
        min_value=1,
        max_value=30,
        value=7
    )

    if st.button("Generate Study Plan"):

        if subject.strip():

            with st.spinner("Creating your study plan..."):

                response = requests.post(
                    f"{API_URL}/generate-study-plan",
                    json={
                        "subject": subject,
                        "hours": hours,
                        "days": days
                    }
                )

            if response.status_code == 200:
                st.success("Study plan generated!")
                st.write(response.json()["study_plan"])
            else:
                st.error(response.text)

        else:
            st.warning("Please enter a subject.")


if feature == "Learning Assistant":

    st.write("Learn any topic with the help of AI.")

    topic = st.text_input(
        "Enter a topic",
        placeholder="Example: Machine Learning"
    )

    if st.button("Explain Topic"):

        if topic.strip():

            with st.spinner("AI is preparing an explanation..."):

                response = requests.post(
                    f"{API_URL}/explain-topic",
                    json={"topic": topic}
                )

            if response.status_code == 200:
                st.success("Explanation generated!")
                st.write(response.json()["explanation"])
            else:
                st.error(response.text)

        else:
            st.warning("Please enter a topic.")
