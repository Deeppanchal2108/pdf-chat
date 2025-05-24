from utils.models import Message
from sqlalchemy.orm import Session
from uuid import UUID

async def load_history(db: Session, user_id: UUID, session_id: UUID, n:int=10):
    """ Function to load chat history from the database"""
    try:
        messages = await db.query(Message).filter(
            Message.user_id == user_id,
            Message.session_id == session_id
        ).order_by(Message.timestamp.desc()).limit(n).all()

        messages = messages[::-1]

        return {"success": True, "messages": messages}
    except Exception as e:
        await db.rollback()
        return {"success": False, "error": "Something went wrong while loading the message history"}
