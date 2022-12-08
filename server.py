from loader import dp, bot
from loader import token

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import pathlib
from urllib.parse import unquote 
import json

from aiogram.utils.markdown import hide_link
from handlers.users.user_status import *
from utils.set_bot_commands import set_default_commands
from keyboards.inline.choice_but_start_test import *
from aiogram.utils.web_app import check_webapp_signature, safe_parse_webapp_init_data

from fastapi import FastAPI, Request, status
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
import uvicorn
from uvicorn import Config, Server

host_address = ''

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

front_path, build_path = pathlib.Path(__file__).parent.resolve() / 'public', pathlib.Path(__file__).parent.resolve() / 'build'

@app.get("/api/alisa-request/{response}")
@limiter.limit("50/minute")
async def sample_function(response: str, request: Request):
    data = response.rsplit("_", 1)
    verify_data, additional_data = data[-2], data[-1]

    check_string = unquote(verify_data)

    valid_status = check_webapp_signature(token=token, init_data=liker_check_string)

    if valid_status:
        data = safe_parse_webapp_init_data(token=token, init_data=check_string, _loads=json.loads)


        return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={ "message": "Успешно отправлен запрос!" }
        )
    else:
        return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={ "message": "Вы не авторизованы." }
        )
    
app.mount("/", StaticFiles(directory=build_path, html=True), name="front")

@app.get('/')
@limiter.limit("20/minute")
async def front(request: Request):
   return RedirectResponse(url='front')

if __name__ == '__main__':
    uvicorn.run("main:app", 
    port=80,
    host=host_address,
    reload=False)
