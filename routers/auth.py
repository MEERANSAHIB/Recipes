from datetime import datetime, timezone, timedelta

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import session
from starlette import status

from model import Users
from database import sessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt, JWTError
router=APIRouter(
    prefix="/auth",
    tags=["auth"])


bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')

SECRET_KEY="a7f3c91e82b64d0fa13e5b729c4d86ab"
ALGORITHM="HS256"



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

def authenticate_user(username,password,db):
    user_model=db.query(Users).filter(Users.user_name==username).first()
    if not user_model:
        return False
    if not bcrypt_context.verify(password,user_model.hashed_password):
        return False
    return user_model

def create_access_token(username:str,id:int,expire_delta:timedelta):
    encode={"sub":username,"id":id}
    expires= datetime.now(timezone.utc) + expire_delta
    encode.update({"exp":expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_name=payload.get('sub')
        user_id=payload.get('id')
        if user_name is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        else:
            return {'user_name':user_name,'id':user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
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

@router.post("/token")
async def token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    user_model=authenticate_user(form_data.username,form_data.password,db)
    if not user_model:
        return "Failed Authentication"
    token=create_access_token(user_model.user_name,user_model.id,timedelta(minutes=20))
    return token