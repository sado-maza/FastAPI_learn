import uvicorn
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from fastapi import FastAPI
users_data = [
    {
        "name": "Mark",
        "email": "user@gmail.com",
        "age": 13
    }
]

app = FastAPI()

class Users_no_age(BaseModel):
    name: str
    email: EmailStr

    model_config = ConfigDict(extra="forbid")


class Users(Users_no_age):
    age: int = Field(gt=0, lt=150)


@app.get("/users")
def list_users():
    return users_data

@app.post("/usersadd")
def users_add(user: Users):
    users_data.append(user)
    return users_data





if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


