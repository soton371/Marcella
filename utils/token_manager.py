from datetime import timedelta, datetime, timezone
import jwt
from core.constants import SECRET_KEY, ALGORITHM


def create_match_otp_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=2)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt