from fastapi.testclient import TestClient
from routs import fake_db
from main import app
import pytest


#Фикстуры
#Сама фикстура, которую в дальнейшем нужно предавать в качестве параметра функции
@pytest.fixture
def client(): #Главная фикстура, которая возвращает подключение к API
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_db(): #Фикстура которая очищает базу и приводит ее в исходное состояние
    fake_db.clear() #Очищаем базу
    fake_db.update({
        1: {"task_id": 1, "task_name": "Изучить FastAPI", "task_status": False},
        2: {"task_id": 2, "task_name": "Порешать задачи на LeetCode", "task_status": True}
    }) #Приводим базу в первоначальное состояние

#Параметризация - позволяет запустить один тест с разными входными данными, эта параметризация для создания задачи
@pytest.mark.parametrize("task_name, task_status", [
    ("Задача1", False),
    ("Задача2", True),
    ("Задача3", False),
])

def test_create_task(client, task_name, task_status):
    response = client.post(f"/Create_task?task_name={task_name}&task_status={task_status}")
    assert response.status_code == 200
    assert response.json()["task_name"] == task_name
    assert response.json()["task_status"] == task_status

#Параметризация для метода Get    
@pytest.mark.parametrize("task_id, task_name, task_status", [
    (1, "Задача1", False),
    (2, "Задача2", True),
    (3, "Задача3", False),    
])

def test_get_task(client, task_id, task_name, task_status):
    responce = client.get("/Get_tasks") #Отправляем запрос get к эндпоинту который отвечает за возврат задач
    assert responce.status_code == 200 #Проверка, что сервер вернул статус 200
    assert responce.json() == {
    "1": {"task_id": 1, "task_name": "Изучить FastAPI", "task_status": False},
    "2": {"task_id": 2, "task_name": "Порешать задачи на LeetCode", "task_status": True}
} #Проверяем что сервер вернул JSON точно такого же формата как написан у меня
    
#Параметризация для метода put
@pytest.mark.parametrize("task_status", [
    (True),
    (False),   
])
def test_put_task(client, task_status):
    responce = client.put(f"/Tasks/1?task_status={task_status}") #Шлем запрос на обновления статуса
    assert responce.status_code == 200 #Проверяем что сервер возвращаеи 200 статус
    assert responce.json()["task_status"] == task_status #Проверяем что статус действительно обновился

#Параметризация для метода delete
@pytest.mark.parametrize("task_id", [
    (1),
    (2), 
])   
def test_delete_task(client, task_id):
    responce = client.delete(f"/Delete_task/{task_id}")
    assert responce.status_code == 200 #Проверяем что сервер возвращаеи 200 статус
    assert responce.json() == {"msg": "Задача успешно удалена"}
    
"""    
def test_get_list_tasks(client): #Тестирование метода GET

    responce = client.get("/Get_tasks") #Отправляем запрос get к эндпоинту который отвечает за возврат задач
    assert responce.status_code == 200 #Проверка, что сервер вернул статус 200
    assert responce.json() == {
    "1": {"task_id": 1, "task_name": "Изучить FastAPI", "task_status": False},
    "2": {"task_id": 2, "task_name": "Порешать задачи на LeetCode", "task_status": True}
} #Проверяем что сервер вернул JSON точно такого же формата как написан у меня

def test_create_new_task(client): #Тестирование метода Post
    responce = client.post("/Create_task?task_name=Новая задача&task_status=false") #Передаем Query парметры напрямую, иначе
    #Имитация запроса на создание новой задачи
    assert responce.status_code == 200 #проверка на успешный статус код
    assert responce.json()["task_name"] == "Новая задача" #Проверяем что поле task_name совпадает с тем, что отправили
    assert responce.json()["task_status"] == False
    
def test_put_status_task(client): #Тестирование метода Put
    responce = client.put("/Tasks/1?task_status=true") #Шлем запрос на обновления статуса
    assert responce.status_code == 200 #Проверяем что сервер возвращаеи 200 статус
    assert responce.json()["task_status"] == True #Проверяем что статус действительно обновился

def test_delete_task(client): #Тестирование метода Delete
    responce = client.delete("/Delete_task/1")
    assert responce.status_code == 200 #Проверяем что сервер возвращаеи 200 статус
    assert responce.json() == {"msg": "Задача успешно удалена"}


client = TestClient(app)

def test_get_list_tasks(): #Тестирование метода GET

    responce = client.get("/Get_tasks") #Отправляем запрос get к эндпоинту который отвечает за возврат задач
    assert responce.status_code == 200 #Проверка, что сервер вернул статус 200
    assert responce.json() == {
    "1": {"task_id": 1, "task_name": "Изучить FastAPI", "task_status": False},
    "2": {"task_id": 2, "task_name": "Порешать задачи на LeetCode", "task_status": True}
} #Проверяем что сервер вернул JSON точно такого же формата как написан у меня
    
def test_create_new_task(): #Тестирование метода Post
    responce = client.post("/Create_task?task_name=Новая задача&task_status=false") #Передаем Query парметры напрямую, иначе
    #Имитация запроса на создание новой задачи
    assert responce.status_code == 200 #проверка на успешный статус код
    assert responce.json()["task_name"] == "Новая задача" #Проверяем что поле task_name совпадает с тем, что отправили
    assert responce.json()["task_status"] == False
    
def test_put_status_task(): #Тестирование метода Put
    responce = client.put("/Tasks/1?task_status=true") #Шлем запрос на обновления статуса
    assert responce.status_code == 200 #Проверяем что сервер возвращаеи 200 статус
    assert responce.json()["task_status"] == True #Проверяем что статус действительно обновился
    
def test_delete_task(): #Тестирование метода Delete
    responce = client.delete("/Delete_task/1")
    assert responce.status_code == 200 #Проверяем что сервер возвращаеи 200 статус
    assert responce.json() == {"msg": "Задача успешно удалена"}
    
def test_delete_task_404_status():#Тестирование метода Delete, на статус код 404
    responce = client.delete("/Delete_task/10")
    assert responce.status_code == 404 #Проверяем что сервер возвращает 404 статус
"""

    