from fastapi import FastAPI,Request,APIRouter ,HTTPException
from uuid import UUID
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from utils.semantic_search import semantic_search

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from utils.db import get_db
from langchain_cohere import ChatCohere
from langchain_cohere import CohereEmbeddings

chat = ChatCohere()

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

router = APIRouter()
db = get_db()

"""
Soo  im thinking of having three routes inn this /chat/summarize , /chat only for the chat normal about the pdf and /chat/compare between the current scenerio and the pdf thing (will fetch the current data from the pdf and compare it with the current data)
the chat will be stored in the database

will use some tools for agents

"""

@router.post("/")
@limiter.limit("20/minute")

async def chat(user_id:UUID , session_id:UUID , request:Request):
    try:
        data =await request.json()
        query=data.get("query")
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        search_result = await semantic_search(db, query, user_id, session_id)

        if not search_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=search_result["message"]
            )
        
        chunks = search_result["chunks"]

        




    except Exception as e:
        return {
            "success": False,
            "message": "Something went wrong",
            "error": str(e)
        }
    
    


    
