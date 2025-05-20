from fastapi import FastAPI,Request
from routes.chat import router as router_chat 
from routes.upload import router as router_upload

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(router_chat , prefix="/chat")
app.include_router(router_upload,prefix="/upload")


@app.get('/health')
@limiter.limit("5/minute")
def health(request :Request):
    return {"Status":"Healthy"}
