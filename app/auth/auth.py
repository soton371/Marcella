from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session

from app.auth import cruds, models, schemas
from core.database import engine, get_db
from utils.app_response import successResponse, failedResponse

# for send otp
from email.message import EmailMessage
import smtplib
import random

models.Base.metadata.create_all(bind=engine)

auth_router = APIRouter()


# for send otp
@auth_router.post("/send-otp")
def sendOtp(getEmail: schemas.TakeEmail):
    try:
        generateOtp = ''
        for i in range(5):
            generateOtp += str(random.randint(0,9))

        smtpServer = smtplib.SMTP('smtp.gmail.com', 587)
        smtpServer.starttls()
        smtpServer.login('tasmia437@gmail.com', 'ceeb akto jmmq ivfk')

        msg = EmailMessage()
        msg['Subject'] = 'Otp Verification'
        msg['from'] = 'tasmia437@gmail.com'
        msg['to'] = getEmail.email
        msg.set_content(f"Your otp code is: {generateOtp}")

        smtpServer.send_message(msg)

        return successResponse(status_code=status.HTTP_201_CREATED, message="User created successfully")
    except Exception as e:
        print(f"{e}")
        return failedResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,message="Something went wrong")




@auth_router.post("/users/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = cruds.get_user_by_email(db, email=user.email)
        if db_user:
            return failedResponse(status_code=status.HTTP_302_FOUND,message="User already registered")
        
        new_user = cruds.create_user(db=db, user=user)
        user_data = schemas.User.model_validate(new_user)
        print(f"register new_user: {new_user.__dict__}")
        return successResponse(status_code=status.HTTP_201_CREATED, message="User created successfully", data=user_data)
    except Exception as e:
        print(f"register e: {e}")
        return failedResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,message="Something went wrong")
    
