from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import session
from model import Users
from database import sessionLocal
from passlib.context import CryptContext

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
router=APIRouter(
    prefix="/auth",
    tags=["auth"]
)
class user(BaseModel):
    email:str
    user_name:str
    hashed_password:str
    isactive:bool
    role:str

def try_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[session,Depends(try_db)]

@router.post("/create_new_user")
async def create_new_user(db:db_dependency,new_user:user):
    user_model=Users(**new_user.model_dump())
    user_model.hashed_password=bcrypt_context.hash(new_user.hashed_password)
    db.add(user_model)
    db.commit()
@router.get("/get_all_users")
async def get_all_users(db:db_dependency):
    return db.query(Users).all()
