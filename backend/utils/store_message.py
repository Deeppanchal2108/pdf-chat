from uuid import UUID

from sqlalchemy.orm import Session
from utils.models import Message


def store_message(db: Session, user_id: UUID, session_id: UUID, content: str):
    """ Function to store messages of the chat in the database"""
    try:
        message = Message(
            user_id=user_id,
            session_id=session_id,
            content=content
        )
        db.add(message)
        db.commit()
        db.refresh(message) 
        return {"success": True, "message": message}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": "Something went wrong while storing the message"}
    


  