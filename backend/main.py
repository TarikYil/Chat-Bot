from fastapi import FastAPI, File, UploadFile, HTTPException
import os
from backend.pdf_processor import extract_text_from_pdf
from backend.vector_db import save_to_chromadb, search_in_chromadb
from models.model import ask_llm
from fastapi.middleware.cors import CORSMiddleware
import logging

# Logging Configuration
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (Frontend apps)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Uploads a PDF, extracts text, and saves it to a vector database.
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        logging.info(f"Received file: {file.filename}")

        # Save file to disk
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        logging.info(f"File saved: {file_path}")

        # Extract text from PDF
        text = extract_text_from_pdf(file_path)
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF!")

        logging.info(f"Extracted text: {text[:500]}...")  # Log first 500 chars

        # Save extracted text to ChromaDB
        save_to_chromadb(text, file.filename)
        logging.info(f"Added to Vector DB: {file.filename}")

        return {"filename": file.filename, "message": "PDF successfully processed!"}

    except Exception as e:
        logging.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/ask/")
async def ask_question(question: str):
    """
    Searches vector database for the most relevant answer and responds.
    """
    try:
        logging.info(f"User question: {question}")

        # Retrieve most relevant documents
        docs = search_in_chromadb(question)
        if not docs:
            return {"question": question, "answer": "No relevant information found in the documents."}

        # Generate response using LLM
        response = ask_llm(question, docs)
        logging.info(f"🤖 AI Response: {response}")

        return {"question": question, "answer": response}

    except Exception as e:
        logging.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=f" Internal Server Error: {str(e)}")
