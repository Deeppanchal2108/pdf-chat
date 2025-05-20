from fastapi import FastAPI,Request,APIRouter
# from routes.chat import router as router_chat 
# from routes.upload import router as router_upload

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

router=APIRouter()


@router.get("/")
def chat():
    return {"chat":"Ok"}