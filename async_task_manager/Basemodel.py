from pydantic import BaseModel



#Для задач
class Tasks(BaseModel):
    id: int | None = None
    title: str | None = None
    status: bool = False