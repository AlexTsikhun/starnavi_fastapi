from fastapi import Depends, HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from dependencies import get_db
from user import oauth2
from user.models import DBUser
from user.schemas import UserCreate
from user.utils import hash_password, verify

router = APIRouter()


@router.post("/register/")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = DBUser(email=user.email, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"username": new_user.email}


@router.post("/token/")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = db.query(DBUser).filter(DBUser.email == form_data.username).first()
    if not db_user or not verify(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Wrong email or password")

    access_token = oauth2.create_access_token(data={"user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}
