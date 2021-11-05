from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int]


posts_list = []


def find_post(post_id: int) -> Optional[dict]:
    for post in posts_list:
        if post["id"] == post_id:
            return post


def find_index_post(post_id: int) -> Optional[int]:
    for index, post in enumerate(posts_list):
        if post["id"] == post_id:
            return index


@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.get("/posts")
async def get_posts():
    return {"data": posts_list}


@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} was not found"
        )
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(payload: Post):
    post_dict = payload.dict()
    post_dict["id"] = posts_list[-1]["id"] + 1 if len(posts_list) > 0 else 1
    posts_list.append(post_dict)
    return {"message": "New post created", "data": post_dict}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    post_index = find_index_post(post_id)
    if post_index is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} was not found"
        )
    del posts_list[post_index]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
async def update_post(post_id: int, payload: Post):
    post_index = find_index_post(post_id)
    if post_index is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} was not found"
        )
    post_dict = payload.dict()
    post_dict["id"] = post_id
    posts_list[post_index] = post_dict
    return {"data": post_dict}
