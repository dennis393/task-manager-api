import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker,DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
from fastapi import FastAPI

class Base(DeclarativeBase):
    pass
load_dotenv()
#Асинхронное подключение к базе данных
async_engine = create_async_engine(f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}") #Создаем базу данных при помощи ассинхрона

#Асинхронная сессия
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

class Task(Base):
   __tablename__ = "Tasks" 
   id: Mapped[int] = mapped_column(primary_key=True)
   title: Mapped[str] = mapped_column(String(200))
   status: Mapped[bool] = mapped_column(default=False)

#Запуск ORM сервером
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield