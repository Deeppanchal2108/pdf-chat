from uuid import UUID
from utils.models import Embedding
from sqlalchemy.orm import Session
from langchain_text_splitters import RecursiveCharacterTextSplitter
from fastapi import UploadFile
from langchain_cohere import CohereEmbeddings
import fitz  # PyMuPDF

embedding_model = CohereEmbeddings(model="embed-english-v3.0")

async def store_data(db: Session, user_id: UUID, file_id: UUID, file: UploadFile):
    """ Function to store data in the database """
    try:
        content = await file.read()
        pdf = fitz.open(stream=content, filetype="pdf")  

        pages = [page.get_text() for page in pdf]

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

        for page_text in pages:
            chunks = text_splitter.split_text(page_text)
            embeddings = embedding_model.embed_documents(chunks)

            for chunk, embedding in zip(chunks, embeddings):
                embedding_obj = Embedding(
                    user_id=user_id,
                    file_id=file_id,
                    chunk=chunk,
                    embedding=embedding
                )
                db.add(embedding_obj)

        await db.commit()
        print("Data stored successfully.")
    
    except Exception as e:
        await db.rollback()
        print(f"Error occurred: {e}")
