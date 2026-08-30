from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import session
from starlette import status

from database import sessionLocal
from model import Recipe
from routers.auth import get_current_user

router=APIRouter(
    prefix="/recipes",
    tags=["recipes"]
)
def try_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[session,Depends(try_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]
class recipe(BaseModel):
    recipe_name:str
    description:str
    cuisine:str
    prep_time_minutes:int
    cook_time_minutes:int
    servings:int
    difficulty:int

@router.post("/create_new_recipe")
async def new_recipe(user:user_dependency,db:db_dependency,new_recipe:recipe):
    if user.get('user_name') is None or user.get('id') is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    recipe_model=Recipe(**new_recipe.model_dump())
    recipe_model.owner_id=user.get('id')
    db.add(recipe_model)
    db.commit()

@router.get("/users/recipes",status_code=status.HTTP_200_OK)
async def users_recipe(user:user_dependency,db:db_dependency):
    return db.query(Recipe).filter(Recipe.owner_id==user.get('id')).all()
@router.get("/get_all_recipe")
async def get_all_users(db:db_dependency):
    return db.query(Recipe).all()



