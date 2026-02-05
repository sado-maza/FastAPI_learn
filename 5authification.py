import uvicorn
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi import FastAPI, Depends, HTTPException, Response
from typing import Annotated
from authx import AuthX, AuthXConfig

config = AuthXConfig()
config.JWT_SECRET_KEY="wtf"
config.JWT_ACCESS_COOKIE_NAME="admin_cookie"
config.JWT_TOKEN_LOCATION=["cookies"]

security = AuthX(config=config)

app = FastAPI()

engine = create_async_engine('sqlite+aiosqlite:///users.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass


class UsersModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    age: Mapped[int]
    password: Mapped[str]


class UsersSchema(BaseModel):
    name: str
    email: EmailStr
    age: int = Field(gt=0, lt=150)
    password: str


@app.post('/setup_database')
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@app.post("/users/regester")
async def add_users(data: UsersSchema,session: SessionDep):
    new_user = UsersModel(
        name=data.name,
        email=data.email,
        age=data.age,
        password=data.password,
    )
    stmt = select(UsersModel).where(UsersModel.email == new_user.email)
    result = await session.execute(stmt)

    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already exists")
    session.add(new_user)
    await session.commit()
    return {"message": "User created successfully"}

@app.get("/users")
async def users_list(session: SessionDep):
    query = select(UsersModel)
    res = await session.execute(query)
    return res.scalars().all()

@app.post("/login")
async def login(creds: UsersSchema, session: SessionDep, response: Response):
    stmt = select(UsersModel).where(UsersModel.email == creds.email)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif user.password == creds.password:
        token = security.create_access_token(str(user.id))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"message": "Login Successful", "access_token": token}
    return {"message": "Incorrect Password"}

@app.get("/protected",dependencies=[Depends(security.access_token_required)])
async def protected(session: SessionDep):
    query = select(UsersModel)
    res = await session.execute(query)
    return res.scalars().all()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

