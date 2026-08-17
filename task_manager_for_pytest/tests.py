from fastapi.testclient import TestClient
from routs import fake_db
from main import app
import pytest


#Фикстуры
#Сама фикстура, которую в дальнейшем нужно предавать в качестве параметра функции
@pytest.fixture
def client(): #Главная фикстура, которая возвращает подключение к API
    return TestClient(app)

@pytest.fixture
def reset_db(autouse=True): #Фикстура которая очищает базу и приводит ее в исходное состояние
    fake_db.clear() #Очищаем базу
    fake_db.update({
        1: {"task_id": 1, "task_name": "Изучить FastAPI", "task_status": False},
        2: {"task_id": 2, "task_name": "Порешать задачи на LeetCode", "task_status": True}
    }) #Приводим базу в первоначальное состояние


#Маркеры используются для того, чтобы помечать тесты тегами
#skip полностью пропустит тест
@pytest.mark.skip(reason="Этот эндпоинт еще не готов")
def test_post(client):
    responce = client.get("/Get_tasks") #Отправляем запрос get к эндпоинту который отвечает за возврат задач
    assert responce.status_code == 200 #Проверка, что сервер вернул статус 200
    assert responce.json() == {
    "1": {"task_id": 1, "task_name": "Изучить FastAPI", "task_status": False},
    "2": {"task_id": 2, "task_name": "Порешать задачи на LeetCode", "task_status": True}
} #Проверяем что сервер вернул JSON точно такого же формата как написан у меня
    
   
#skipif пропустит тест, если услолвие True
#Например @pytest.mark.skipif(sys.platform == "win32", reason="Не работает на windows")
@pytest.mark.skipif(True, reason="Причина")
def test_post(client):
    responce = client.get("/Get_tasks") #Отправляем запрос get к эндпоинту который отвечает за возврат задач
    assert responce.status_code == 200 #Проверка, что сервер вернул статус 200
    assert responce.json() == {
    "1": {"task_id": 1, "task_name": "Изучить FastAPI", "task_status": False},
    "2": {"task_id": 2, "task_name": "Порешать задачи на LeetCode", "task_status": True}
} #Проверяем что сервер вернул JSON точно такого же формата как написан у меня   

#xFail ожидаемо падает и Pytest не считает это ошибкой
@pytest.mark.xfail(reason="баг в удалении задачи пока не починили")
def test_delete(client):
    responce = client.delete("/Delete_task/99")
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

    