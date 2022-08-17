
from .. import models,utils,schemas
from fastapi import  Body, FastAPI,HTTPException,APIRouter, Response ,status,Depends
from ..database import engine,get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(

     prefix ="/users",
      tags = ['Users']

)



@router.post("/" , status_code = status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate , db: Session = Depends(get_db)):
   
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
   
   
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user

@router.get("/{id}",response_model = schemas.UserOut)
def get_user(id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id ).first()
    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f "post with id : {id} was not found "}
    #print(post)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f"user with id {id} was not found")
    return  user