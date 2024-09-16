from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

from auth import cruds, models, schemas
from core.database import SessionLocal, engine
from utils.app_response import successResponse, failedResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = cruds.get_user_by_email(db, email=user.email)
    if db_user:
        return failedResponse(status_code=status.HTTP_302_FOUND,message="User already registered.")
    
    new_user = cruds.create_user(db=db, user=user)
    return successResponse(status_code=status.HTTP_201_CREATED, message="User created successfully", data=new_user)
    