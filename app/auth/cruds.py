from sqlalchemy.orm import Session
from app.auth import schemas, models
from datetime import datetime




def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.Users(email=user.email, full_name = user.full_name, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def otp_store(db: Session, otp_code: str, recipient_mail: str):
    try:
        current_time = str(datetime.now())
        db_otp_store = models.OtpStore(email=recipient_mail, otp=otp_code, send_time=current_time)
        db.add(db_otp_store)
        db.commit()
        db.refresh(db_otp_store)
        return True
    except Exception as e:
        print(f'otp_store e: {e}')
        return False
    
