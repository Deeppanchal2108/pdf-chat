from fastapi import FastAPI,APIRouter,UploadFile, File

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from utils.store_meta import store_meta
from utils.store_data import store_data
from utils.db import get_db

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

router=APIRouter()
db = get_db()

@router.post("/")
async def upload(file :UploadFile= File(...)):
    content = await file.read()
    print(content)
    # Store the file metadata in the database
    result=store_meta (
        db=db,
        user_id=...,
        file_name=file.filename,
        content_type=file.content_type,
        file_size=round(len(content)/(1024*1024),2)
    )

    if(result["success"]==False):
        return {
            "success":False,
            "message":"Something went wrong while storing the file metadata",
            "error":result["error"]
        }
    
    store_data(
        db=db,
        user_id=...,
        file_id=result.file.file_id,
        file=file
    )

    return {
        "filename":  file.filename,
        "file content type ":  file.content_type,
        "Size":round(len(content)/(1024*1024),2),
        "message":"File uploaded successfully",
        "success":True
    }
