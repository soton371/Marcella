from datetime import timedelta, datetime, timezone
import jwt
from core.constants import SECRET_KEY, ALGORITHM
from fastapi import Request


def create_match_otp_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=2)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




def extract_token(authorization: str) -> str:
    try:        
        if authorization and authorization.startswith("Bearer "):
            return authorization[7:]  
        else:
            return None
    except Exception as e:
        print(f"extract_token exception: {e}")
        return None


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  
    except Exception as e:
        print(f'verify_token e: {e}')
        return None