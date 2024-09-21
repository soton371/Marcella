from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session

from app.auth import cruds, models, schemas
from core.database import engine, get_db
from utils.app_response import successResponse, failedResponse
from utils import token_manager

# for send otp
from utils import otp_manager, datetime_manager


models.Base.metadata.create_all(bind=engine)

auth_router = APIRouter()


# for send otp
@auth_router.post("/send-otp")
def sendOtp(getEmail: schemas.TakeEmail, db: Session = Depends(get_db)):
    try:
        cruds.delete_otp_by_email(db=db, email=getEmail.email)
        myOtp = otp_manager.generateOTP()

        otpStore = cruds.otp_store(db=db, otp_code=myOtp, recipient_mail=getEmail.email)
        if not otpStore:
            return failedResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,message="Failed to store otp")

        sendOtp = otp_manager.sendOtpSmtp(otp=myOtp, recipientMail=getEmail.email)
        if not sendOtp:
            return failedResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,message="Failed to send otp")

        return successResponse(status_code=status.HTTP_200_OK, message="Otp code sent successfully")
    except Exception as e:
        print(f"sendOtp e:{e}")
        return failedResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,message="Something went wrong")


# for match otp
@auth_router.post("/match-otp")
def matchOtp(payload: schemas.MatchOtpPayload, db: Session = Depends(get_db)):
    try:
        otpStore = cruds.get_otp(db=db, email= payload.email)
        if not otpStore:
            return failedResponse(status_code=status.HTTP_404_NOT_FOUND,message="Your otp code not found")
        
        if datetime_manager.is_expired(otpStore.send_time):
            return failedResponse(status_code=status.HTTP_400_BAD_REQUEST,message="Your OTP code has expired")
        
        if not payload.otp_code == otpStore.otp:
            return failedResponse(status_code=status.HTTP_404_NOT_FOUND,message="Your otp code does not match")
        cruds.delete_otp_by_email(db=db, email=payload.email)
        matchOtpToken = token_manager.create_match_otp_token(otpStore.to_dict())
        return successResponse(status_code=status.HTTP_200_OK, message="Your otp code matches", token= matchOtpToken)
    except Exception as e:
        print(f"matchOtp e: {e}")
        return failedResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,message="Something went wrong")


@auth_router.post("/users/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = cruds.get_user_by_email(db, email=user.email)
        if db_user:
            return failedResponse(status_code=status.HTTP_302_FOUND,message="User already registered")
        
        new_user = cruds.create_user(db=db, user=user)
        return successResponse(status_code=status.HTTP_201_CREATED, message="User created successfully", data=new_user.to_dict())
    except Exception as e:
        print(f"register e: {e}")
        return failedResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,message="Something went wrong")
    
