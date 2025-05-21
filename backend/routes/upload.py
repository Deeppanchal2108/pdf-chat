from fastapi import FastAPI,APIRouter,UploadFile, File

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

router=APIRouter()


@router.post("/")
async def upload(file :UploadFile= File(...)):
    content = await file.read()

    
    return {
      "filename":  file.filename,
       "file content type ":  file.content_type,
        "Size":round(len(content)/(1024*1024),2)
    }
