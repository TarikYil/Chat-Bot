import google.generativeai as genai
import os
from dotenv import load_dotenv

AVAILABLE_MODELS = ["gemini-1.0-pro", "gemini-2.0-flash-lite", "gemini-1.5-pro"]

load_dotenv()

# Get API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def ask_llm(question, context_docs, model="gemini-1.5-pro"):
    if model not in AVAILABLE_MODELS:
        return "Seçilen model desteklenmiyor!"

    context = "\n".join(context_docs)
    prompt = f"Answer this question based on the context:\n\n{context}\n\nQuestion: {question}\nAnswer:"

    gen_model = genai.GenerativeModel(model)
    response = gen_model.generate_content(prompt)

    return response.text if response else "Üzgünüm, bir hata oluştu."

