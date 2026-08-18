import time

from typing import Annotated
from fastapi import FastAPI, Depends, Request
from basemodel import Tasks
from db_new import Base, Task
from routs_for_db import router
from secure import oauth2_scheme

app = FastAPI()
app.include_router(router)

@app.middleware("http")
async def process_time(request: Request, call_nxt):
    #Время до выполнения CRUD операции
    start = time.perf_counter()
    
    #Передаем запрос дальше в соответствующий маршрут
    response = await call_nxt(request)
    
    #Вычисляем время
    time_ = time.perf_counter() - start
    
    #Добавляем время в заголовок ответа
    response.headers["Process-Time"] = str(time_)
    return response

@app.get("/auth")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

def main_func():
    return {"Добро пожаловать в приложение"}