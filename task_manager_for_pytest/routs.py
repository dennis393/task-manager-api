from fastapi import APIRouter, HTTPException
from basemodel import Tasks


router = APIRouter()
fake_db = {
    1: {"task_id": 1, "task_name": "Изучить FastAPI", "task_status": False},
    2: {"task_id": 2, "task_name": "Порешать задачи на LeetCode", "task_status": True}
}
id_t = 3

@router.post("/Create_task")
def create_task(task_name: str, task_status: bool):
    global id_t
    create_task = {"task_id": id_t, "task_name": task_name, "task_status": task_status}
    fake_db[id_t] = create_task
    id_t += 1
    return create_task

@router.get("/Get_tasks")
def get_tasks():
    return fake_db

@router.put("/Tasks/{task_id}")
def update_status(task_id: int, task_status: bool):
    if task_id in fake_db:
        fake_db[task_id]["task_status"] = task_status
        return fake_db[task_id]
    else:
        raise HTTPException(status_code=404, detail="id not found")
    
@router.delete("/Delete_task/{task_id}")
def del_task(task_id: int):
    if task_id not in fake_db:
        raise HTTPException(status_code=404, detail="id not found")
    del fake_db[task_id]
    return {"msg": "Задача успешно удалена"}
        