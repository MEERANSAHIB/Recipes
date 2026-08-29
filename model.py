from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import foreign

from database import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    user_name = Column(String, unique=True)
    hashed_password = Column(String)
    isactive = Column(Boolean)
    role = Column(String)

class Recipe(Base):
    __tablename__="recipe"
    id=Column(Integer,primary_key=True,index=True)
    recipe_name=Column(String)
    description=Column(String)
    cuisine=Column(String)
    prep_time_minutes=Column(Integer)
    cook_time_minutes=Column(Integer)
    servings=Column(Integer)
    difficulty=Column(Integer)
    owner_id=Column(Integer,foreign("users.id"))


