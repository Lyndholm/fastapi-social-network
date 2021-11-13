from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm.session import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/{post_id}", response_model=schemas.Post)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} was not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(payload: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if post.first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} was not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schemas.Post)
async def update_post(post_id: int, payload: schemas.PostCreate, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if post.first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} was not found")
    post.update(payload.dict(), synchronize_session=False)
    db.commit()
    return post.first()
