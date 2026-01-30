from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from fastapi import FastAPI,Depends
from typing import Annotated

app = FastAPI()

engine = create_async_engine('sqlite+aiosqlite:///books.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass

class Books(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]


@app.post('/setup_database')
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class BookSchema(BaseModel):
    title: str
    author: str


@app.post("/books")
async def add_books(data: BookSchema,session: SessionDep):
    new_book = Books(
        title=data.title,
        author=data.author,
    )
    session.add(new_book)
    await session.commit()

@app.get("/books")
async def get_books(session: SessionDep):
    query = select(Books)
    res = await session.execute(query)
    return res.scalars().all()