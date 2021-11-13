from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app import schemas

from .. import models, oauth2, utils
from ..database import get_db

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
async def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.username).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    if not utils.verify_password(credentials.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    acces_token = oauth2.create_acces_token(data={"user_id": user.id})
    return {"acces_token": acces_token, "token_type": "bearer"}
