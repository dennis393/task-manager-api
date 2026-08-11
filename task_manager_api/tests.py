
from dotenv import load_dotenv
import os

load_dotenv(encoding="utf-8")

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_list_tasks():

    responce = client.get("/Task") #Отправляем запрос get к эндпоинту который отвечает за возврат задач
    assert responce.status_code == 200 #Проверка, что сервер вернул статус 200
    
    