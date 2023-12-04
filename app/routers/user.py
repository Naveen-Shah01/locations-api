from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException,status,Response,Depends,APIRouter
from ..import models,schemas,Utils
from ..database import get_db

router = APIRouter(
    tags=['User']
)


@router.post("/add_user", status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def add_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    print(user)
    # new_location = models.Location(longitude=location.longitude,latitude=location.latitude,
    #                 name=location.name,description=location.description)
    hashed_password = Utils.get_password_hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user


@router.get("/get_user/{id}",response_model=schemas.UserResponse)
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if user.first() == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    
    return user.first()

