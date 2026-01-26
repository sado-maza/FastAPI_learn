import uvicorn
from fastapi import FastAPI, HTTPException
from books_data import data
from pydantic import BaseModel

app = FastAPI()

@app.get("/books", tags=["books"], summary="get all books")
def get_books():
    return data

@app.get("/books/{book_id}", tags=["books"], summary="get one book by id")
def get_book(book_id: int):
    for book in data:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="book not found")


class NewBook(BaseModel):
    title: str
    author: str
    number_of_pages: int
    year_published: str


@app.post("/bookss", tags=["books"], summary="create new book")
def add_book(new_book: NewBook):
    data.append({
        "id": data[-1]["id"]+1,
        "title": new_book.title,
        "author": new_book.author,
        "number_of_pages": new_book.number_of_pages,
        "year_published": new_book.year_published
    })
    return data[-1]


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

