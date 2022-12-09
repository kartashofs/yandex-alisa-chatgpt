from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import json

from fastapi import FastAPI, Request, status
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

import uvicorn
from uvicorn import Config, Server

from ChatGPT import ChatGPT

host_address = 'UNSPECIFIED'

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/alisa-request")
@limiter.limit("50/minute")
async def handle_alisa_request(response: str, request: Request):
    data = await request.json()
    
    question = str(data["request"]["original_utterance"])
  
    if question:
        chat = ChatGPT.Chat(email="EMAIL", password="PASS")
        answer = chat.ask(question)
    
        return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"session": data["session"],
                         "version": data["version"],
                         "response": {"end_session": False,
                                      "text": answer} })
    else:
        return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"session": data["session"],
                         "version": data["version"],
                         "response": {"end_session": False,
                                      "text": "Привет, я GPT-bot, который работает на основе нейронной сети от OpenAI. Я могу фантазировать, делать технические расчеты - быть твоим умным собеседником и другом. Можешь ознакомиться с кодом в телеграм канале: @kartashofs"} })

if __name__ == '__main__':
    uvicorn.run("server:app", 
    port=80,
    reload=True)
