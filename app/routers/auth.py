from ..import database,schemas,models,Utils,oauth2
from sqlalchemy.orm import Session
from fastapi import Depends,status,HTTPException,Response,APIRouter


router = APIRouter(
    tags=['Authentication']
)

@router.post("/login")
def login(user_credentials : schemas.UserLogin,db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"INVALID")
    
    if not Utils.verify_password(user_credentials.password,user.password):
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"INVALID Passwrod")
    access_token = oauth2.create_access_token(data = {"user_id":user.id})
    return {"Token":access_token}