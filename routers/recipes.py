from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import session

from database import sessionLocal
from model import Recipe

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
class recipe(BaseModel):
    recipe_name:str
    description:str
    cuisine:str
    prep_time_minutes:int
    cook_time_minutes:int
    servings:int
    difficulty:int
    owner_id:int

@router.post("/create_new_recipe")
async def new_user(db:db_dependency,new_recipe:recipe):
    recipe_model=Recipe(**new_recipe.model_dump())
    db.add(recipe_model)
    db.commit()

@router.get("/get_all_recipe")
async def get_all_users(db:db_dependency):
    return db.query(Recipe).all()


