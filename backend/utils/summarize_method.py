
from utils.models import Embedding
from sqlalchemy import text
from sqlalchemy.orm import Session
from uuid import UUID
from langchain_core.prompts import PromptTemplate
from langchain_cohere import ChatCohere
chat = ChatCohere()

small_summary_template = PromptTemplate(template=""""You are an expert summarizer. Read the following PDF content and produce a clear and concise summary.

Follow these rules:
- Focus only on the most important ideas, arguments, or facts.
- Do not include unnecessary details or filler.
- Write the summary in 2-3 small points.
- Keep each point brief and impactful.
- Maintain the original meaning and intent of the content.
- Use simple, clear language suitable for a non-expert reader.

Content:
{content}
""", input_variables=["content"])


summary_template = PromptTemplate(
    template="""You are an expert summarizer. Based on the following partial summaries of different sections of a PDF, create a comprehensive final summary.

Follow these rules:
- Summarize in 8–10 bullet points.
- Do not repeat the same idea multiple times.
- Only keep impactful and insightful points.
- Use simple, clear language suitable for a non-expert.

Partial Summaries:
{content}
""", 
    input_variables=["content"]
)

def generate_summary(chunk :str):
    "This function will generate a summary for each given chunk of text"
    try:
        prompt = small_summary_template.invoke({"content": chunk})
        summary = chat.invoke(prompt)
        return summary.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"




async def summarize_method(db :Session, user_id: UUID, session_id: UUID):
    """Funtion to perform the summarization of the whole document """
    try:
        sql_query = text("""
                        SELECT chunk
                        FROM embeddings
                        WHERE user_id = :user_id AND session_id = :session_id
                        """)
        result = await db.execute(
            sql_query,
            {
                "user_id": user_id,
                "session_id": session_id
            }
        ).fetchall()

        if not result:
            return {
                "success": False,
                "message": "No chunks found for the user and session."
            }

        chunks = [row[0] for row in result]
        if not chunks:
            return {
                "success": False,
                "message": "No relevant chunks found."
            }
        
        summaries=[]
        for chunk in chunks:
            summary = generate_summary(chunk)
            summaries.append(summary)
        
        final_summary_prompt = summary_template.invoke({"content": summaries})
        summary = chat.invoke(final_summary_prompt).content
        if not summary:
            return {
                "success": False,
                "message": "Failed to generate final summary."
            }
    

        return {
            "success": True,
            "message": "Summarization completed successfully.",
            "summary": summary
        }
    except Exception as e:
        return {
            "success": False,
            "message": "An error occurred during summarization.",
            "error": str(e)
        }
