import os
from datetime import datetime,timedelta,timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError,VerificationError
from dotenv import load_dotenv
from fastapi import Depends,HTTPException
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer

load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is missing in .env")

Algorithm="HS256"
Token_Hours=24

hasher=PasswordHasher()
barer=HTTPBearer()

def hash_password(password:str):
    return hasher.hash(password)

def verify_password(password:str,pasword_hash:str)->bool:
    try:
        return hasher.verify(pasword_hash,password)
    except(VerificationError,InvalidHashError):
        return False

def create_token(user_id:int)->str:
    payload={
        "sub":str(user_id),
        "exp":datetime.now(timezone.utc)+timedelta(hours=Token_Hours)
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=Algorithm)

def get_current_user_id(cradentials:HTTPAuthorizationCredentials=Depends(barer),)->int:
    try:
        payload=jwt.decode(cradentials.credentials,SECRET_KEY,algorithms=[Algorithm])
        return int(payload["sub"])
    except (jwt.PyJWKError,KeyError,ValueError):
        raise HTTPException(status_code=401,detail="Invalid or expired token")

