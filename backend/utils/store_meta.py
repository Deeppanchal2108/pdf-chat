from uuid import UUID
from utils.models import File
from dotenv import load_dotenv
from sqlalchemy.orm import Session
load_dotenv()


async def store_meta( db:Session ,user_id : UUID, file_name:str ,  content_type :str, file_size:float ):
    try:
        file = File(
        user_id=user_id,
        filename=file_name,
        content_type=content_type,
        file_size=file_size
        )
        db.add(file)
        await db.commit()
        await db.refresh(file)
        return {"success":True, "file":file}
    except Exception as e : 
        await db.rollback()
        return {"success":False, "error":"Something went wrong while storing the meta data"}






