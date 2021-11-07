from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]


@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.get("/posts")
async def get_posts():
    return {"data": "Here will be a list of posts."}


@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    return {"data": "Here will be a post with the specified id."}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(payload: Post):
    return {"message": "New post created."}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
async def update_post(post_id: int, payload: Post):
    return {"data": "Post updated."}
