from fastapi import Depends, HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from dependencies import get_db
from user import oauth2
from user.crud import toggle_auto_reply
from user.models import DBUser
from user.oauth2 import get_current_user
from user import schemas
from user.utils import hash_password, verify

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register/")
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = DBUser(email=user.email, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"username": new_user.email}


@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = db.query(DBUser).filter(DBUser.email == form_data.username).first()
    if not db_user or not verify(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Wrong email or password")

    access_token = oauth2.create_access_token(data={"user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: str = Depends(get_current_user)):
    return current_user


@router.put("/auto-reply", response_model=schemas.AutoReplyToggleResponse)
async def update_auto_reply(
    db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)
):
    previous_state = current_user.auto_reply_enabled
    updated_user = toggle_auto_reply(db, current_user)
    new_state = updated_user.auto_reply_enabled

    response = schemas.AutoReplyToggleResponse(
        previous_state=previous_state,
        new_state=new_state,
        message="Auto-reply setting updated successfully.",
    )

    return response


@router.put("/reply-delay")
async def update_reply_delay(
    request: schemas.UpdateReplyDelayRequest,
    db: Session = Depends(get_db),
    user: DBUser = Depends(get_current_user),
):
    user.reply_delay = request.delay
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Reply delay updated", "new_delay": user.reply_delay}
