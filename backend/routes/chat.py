from fastapi import FastAPI,Request,APIRouter ,HTTPException
from uuid import UUID
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage 
from utils.semantic_search import semantic_search
from utils.load_history import load_history
from utils.save_messages import save_message
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from utils.db import get_db
from langchain_cohere import ChatCohere
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

template= ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant who answers based only on the provided PDF chunks."),
    ("system", "PDF Content:\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{query}")
])

@router.post("/")
@limiter.limit("20/minute")
async def chat(user_id: UUID, session_id: UUID, request: Request):
    try:
        data = await request.json()
        query = data.get("query")
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        search_result = await semantic_search(db, query, user_id, session_id)

        if not search_result["success"]:
            raise HTTPException(
                status_code=400,
                detail=search_result["message"]
            )
        
        chunks = search_result["chunks"]
        if not chunks:
            raise HTTPException(
                status_code=404,
                detail="No relevant chunks found for the query."
            )
        context=load_history(db, user_id, session_id, n=5)

        if not context["success"]:
            raise HTTPException(
                status_code=500,
                detail=context["message"]
            )
        context_messages = context["messages"]

        model = ChatCohere(temperature=0.1)
        chain = template | model
        response = chain.invoke({"chat_history": context_messages, "query": query, "context": chunks})

        if not response["success"]:
           raise HTTPException(
               status_code=500,
               detail=response["message"]
           )
        
        save_message(db, user_id, session_id, HumanMessage(content=query))
        save_message(db, user_id, session_id, AIMessage(content=response.content))
       


        
        return {
           "success": True,
           "message": response.content
       }



    except Exception as e:
        return {
            "success": False,
            "message": "Something went wrong",
            "error": str(e)
        }
    
    


    
