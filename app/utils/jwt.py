from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import ValidationException,HTTPException
from app.db.session import get_db
from app.repositories.user import get_current_user_repo
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime , timezone , timedelta
import jwt , os
from dotenv import load_dotenv

load_dotenv()
secret_key=os.getenv('SECRET_KEY')

def create_access_token(user_id:str):
    access_token=jwt.encode(
        {
            "sub":user_id,
            "type":"access",
            "exp":datetime.now(timezone.utc) + timedelta(hours=1)
        } , 
        secret_key , 
        "HS256"
    )
    return access_token


def create_refresh_token(user_id:str):
    refresh_token=jwt.encode(
        {
            "sub":user_id,
            "type":"refresh",
            "exp":datetime.now(timezone.utc) + timedelta(hours=1)
        },
        secret_key,
        "HS256"
    )
    return refresh_token


async def get_current_user(token:str=Depends(OAuth2PasswordBearer(tokenUrl='login')),
                           session:AsyncSession=Depends(get_db)):
    try:
        access_token=jwt.decode(token,secret_key,algorithms=['HS256'])
        user_id=access_token['sub']
    except Exception:
        raise jwt.PyJWTError('توکن نامعتبر می باشد')
    if access_token.get('type')!='access':
        raise ValidationException('access token not found!')
    user=await get_current_user_repo(int(user_id),session)
    if not user:
        raise HTTPException(
            status_code=401,
            detail='کاربری یافت نشد'
        )
    return user
    
    

        