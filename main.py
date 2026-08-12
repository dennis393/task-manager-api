from fastapi import FastAPI
from routs import router

app = FastAPI()

app.include_router(router)

def main_func():
    return {"task manager для изучения Pytest"}