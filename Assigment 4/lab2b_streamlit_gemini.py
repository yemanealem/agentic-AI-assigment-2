import os
from dotenv import load_dotenv

try:
    import streamlit as st
    USE_STREAMLIT = True
except ImportError:
    USE_STREAMLIT = False

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

try:
    import google.generativeai as genai
    genai.configure(api_key=API_KEY)
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

MODEL_NAME = "gemini-2.0-flash-exp"

# =========================
# Helper functions
# =========================
def get_documents_content(file_paths):
    contents = []
    for path in file_paths:
        with open(path, "r", encoding="utf-8") as f:
            contents.append(f.read())
    return contents

def generate_gemini_response(documents, query):
    """Call Gemini SDK or fallback to mock."""
    prompt_parts = ["\n".join(documents), query]

    if not HAS_GENAI:
        return f"RESPONSE: You asked '{query}'. Gemini SDK not installed."

    try:
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        return f"RESPONSE: Cannot connect to Gemini API. {str(e)}"

# =========================
# Terminal Mode
# =========================
def run_terminal():
    num_docs = int(input("How many documents? "))
    file_paths = [input(f"Path for document {i+1}: ") for i in range(num_docs)]
    documents = get_documents_content(file_paths)
    query = input("Enter your query: ")
    answer = generate_gemini_response(documents, query)
    print("\n===== Gemini / Mock Response =====")
    print(answer)

# =========================
# Streamlit Mode
# =========================
def run_streamlit():
    st.title("Lab 2B - connecting streamlit app to an external LLM model -Gemini")

    uploaded_files = st.file_uploader("Upload documents", type=["txt"], accept_multiple_files=True)
    query = st.text_input("Enter your query")

    if st.button("Get Response"):
        if not uploaded_files:
            st.warning("Please upload at least one document.")
        elif not query:
            st.warning("Please enter a query.")
        else:
            file_contents = [file.read().decode("utf-8") for file in uploaded_files]
            answer = generate_gemini_response(file_contents, query)
            st.subheader("Response:")
            st.write(answer)

# =========================
# Main
# =========================
if __name__ == "__main__":
    if USE_STREAMLIT:
        run_streamlit()
    else:
        run_terminal()
