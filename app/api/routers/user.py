from fastapi import APIRouter , Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import LoginIn , LoginOut , SignupIn , SignupOut , VerifySignupIN , VerifySignupOut
from app.services.user import (
    login_service , signup_service , create_otp_signup_service , verify_signup_service , 
    create_user_service , delete_otp_service
    )
from app.db.session import get_db
from app.core.redis import redis
from app.utils.random_code import generate_code_for_signup
from app.tasks.user import send_email_task
from app.utils.jwt import create_access_token , create_refresh_token
import json

router = APIRouter()


@router.post('/login',response_model=LoginOut)
async def login(data:LoginIn,session:AsyncSession=Depends(get_db)): 
    result_login=await login_service(data,session)
    if not result_login : 
        raise HTTPException(
            status_code= 401 , 
            detail = 'نام کاربری یا رمزعبور نادرست می باشد'
        )
    access=create_access_token(str(result_login.id))
    refresh=create_refresh_token(str(result_login.id))
    return {
        'user':result_login , 
        'success':'باموفقیت وارد شدید' , 
        'access':access,
        'refresh':refresh
    }


@router.post('/signup',response_model=SignupOut)
async def signup(data:SignupIn,session:AsyncSession=Depends(get_db)) : 
    result_signup=await signup_service(data,session)
    await redis.set(
        f'username_{result_signup.username}', 
        json.dumps({
            'username':result_signup.username, 
            'password':result_signup.password, 
            'email':result_signup.email
        }), 
        ex=300
    )
    code=generate_code_for_signup()
    send_email_task.delay(result_signup.email,code)

   
    otp_signup=await create_otp_signup_service(code,result_signup.username,session)

    return otp_signup


@router.post('/verify_signup/{otp_id}',response_model= VerifySignupOut)
async def verify_signup(otp_id:int,data:VerifySignupIN,session:AsyncSession=Depends(get_db)): 
    
    result_verify_signup_service=await verify_signup_service(otp_id,data,session)
    user = await redis.get(f'username_{result_verify_signup_service.username}')
    user = json.loads(user)
    create_user = await create_user_service(user , session)

    await redis.delete(f'username_{result_verify_signup_service.username}')
    
    await delete_otp_service(otp_id , result_verify_signup_service.username , session)

    return {
        'success' : 'ثبت نام باموفقیت انجام شد' , 
        'user' : create_user
    }

    

    

