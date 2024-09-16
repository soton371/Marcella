from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session

from app.auth import cruds, models, schemas
from core.database import engine, get_db
from utils.app_response import successResponse, failedResponse

models.Base.metadata.create_all(bind=engine)

auth_router = APIRouter()


@auth_router.post("/users/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = cruds.get_user_by_email(db, email=user.email)
        if db_user:
            return failedResponse(status_code=status.HTTP_302_FOUND,message="User already registered")
        
        new_user = cruds.create_user(db=db, user=user)
        # Use model_validate for ORM serialization
        user_data = schemas.User.model_validate(new_user)
        print(f"register new_user: {new_user.__dict__}")
        return successResponse(status_code=status.HTTP_201_CREATED, message="User created successfully", data=user_data)
    except Exception as e:
        print(f"register e: {e}")
        return failedResponse(status_code=status.HTTP_400_BAD_REQUEST,message="Something went wrong")
    
