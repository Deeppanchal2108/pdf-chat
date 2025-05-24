from utils.models import Message
from sqlalchemy.orm import Session
from uuid import UUID

async def save_message(db: Session, user_id: UUID, session_id: UUID, content: str):
    """ Function to save messages of the chat in the database"""
    try:
        message = Message(
            user_id=user_id,
            session_id=session_id,
            content=content
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return {"success": True, "message": message}
    except Exception as e:
        await db.rollback()
        return {"success": False, "error": "Something went wrong while saving the message"}
