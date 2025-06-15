from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.orm import Session
from utils.store_meta import store_meta
from utils.store_data import store_data
from utils.db import get_db
from fastapi import Request

router = APIRouter()

@router.post("/")
async def upload(request: Request, db: Session = Depends(get_db)):
    try:
        form = await request.form()
        file = form.get("file")
        content = await file.read()
        
        # Store the file metadata in the database
        result = store_meta(
            db=db,
            user_id=request.user.id,
            file_name=file.filename,
            content_type=file.content_type,
            file_size=round(len(content)/(1024*1024), 2)
        )

        if not result["success"]:
            return {
                "success": False,
                "message": "Something went wrong while storing the file metadata",
                "error": result["error"]
            }
        
        store_data(
            db=db,
            user_id=request.user.id,
            file_id=result.file.file_id,
            file=file
        )

        return {
            "filename": file.filename,
            "file_content_type": file.content_type,
            "size": round(len(content)/(1024*1024), 2),
            "message": "File uploaded successfully",
            "success": True
        }
    except Exception as e:
        return {
            "success": False,
            "message": "Error processing file upload",
            "error": str(e)
        }
