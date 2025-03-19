import chromadb

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="pdf_docs")

def save_to_chromadb(text, doc_id):
    collection.add(
        documents=[text],
        ids=[doc_id]
    )

def search_in_chromadb(query):
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    return results["documents"][0] if results["documents"] else []
