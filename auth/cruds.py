from sqlalchemy.orm import Session
from auth import schemas, models




def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.Users(email=user.email, full_name = user.full_name, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

