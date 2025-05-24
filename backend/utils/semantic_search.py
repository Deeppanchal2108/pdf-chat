from langchain_cohere import CohereEmbeddings
from utils.models import Embedding
from sqlalchemy import text
from sqlalchemy.orm import Session
from uuid import UUID

embedding_model = CohereEmbeddings(model="embed-english-v3.0")


async def semantic_search(db :Session,query: str , user_id: UUID, session_id: UUID):
    """ Function to perform semantic search using embeddings  and return relevant chunks"""
    try:
        embeddings = embedding_model.embed_documents([query])

        if not embeddings or len(embeddings) == 0:
            return {
                "success": False,
                "message": "No embeddings generated for the query."
            }
        sql_query = text("""
                        SELECT chunk
                        FROM embeddings
                        WHERE user_id = :user_id AND session_id = :session_id
                        ORDER BY embedding <-> :embedding
                        LIMIT :top_k
                         """)
        result =db.execute(
            sql_query,
            {
                "user_id": user_id,
                "session_id": session_id,
                "embedding": embeddings[0],
                "top_k": 5  # Adjust the number of results you want to retrieve
            }
        ).fetchall()

        if not result:
            return {
                "success": False,
                "message": "No relevant chunks found."
            }
        chunks = [row[0] for row in result]
        return {
            "success": True,
            "message": "Semantic search completed successfully.",
            "chunks": chunks
        }
    except Exception as e:
        return {
            "success": False,
            "message": "An error occurred during semantic search.",
            "error": str(e)
        }
        
