from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import (
    LoginIn , UserOut
)
from app.repositories.user import (
    search_user_for_login , search_user_for_signup_repo , search_otp_signup_repo_and_delete , verify_signup_repo , 
    create_user_repo , create_otp_signup_repo , signup_repo  , delete_otp_repo
    ) 
from app.models.user import User
from app.core.security import hash_password_manager

from datetime import datetime , timedelta , timezone



async def login_service(data:LoginIn,session:AsyncSession): 
    search_user=await search_user_for_login(data.username,data.password,session)
    if search_user and hash_password_manager.verify(data.password,search_user.password):
        return search_user


async def signup_service (data , session : AsyncSession) : 
    result_search_user_repo = await search_user_for_signup_repo(data , session)
    if result_search_user_repo is None: 
        create_user_repo = await signup_repo(data , session)
        return create_user_repo
    raise HTTPException(
        status_code= 401 , 
        detail= 'این کاربر قبلا ثبت نام کرده است'
    )
    
    


async def create_otp_signup_service(code:str,username:str,session:AsyncSession): 
    await search_otp_signup_repo_and_delete(username , session)
    return await create_otp_signup_repo(code , username , session)



async def verify_signup_service (otp_id : int , data , session : AsyncSession): 
    result_verify_signup = await verify_signup_repo(otp_id , data , session)
    if not result_verify_signup : 
        raise HTTPException(
            status_code= 401 , 
            detail= 'کد تایید نامعتبر می باشد'
        )
    if result_verify_signup.created_at < datetime.now(timezone.utc) - timedelta(minutes= 2) : 
        raise HTTPException(
            status_code= 401 , 
            detail= 'کد تایید منقضی شده است'
        )
    if result_verify_signup.code != data.code :
        raise HTTPException(
            status_code= 401 , 
            detail= 'کد تایید نادرست می باشد'
        )
    return result_verify_signup
    

async def create_user_service(user,session:AsyncSession): 
    result_create_user_repo = await create_user_repo(user , session)
    return result_create_user_repo



async def delete_otp_service (otp_id , username , session : AsyncSession) : 
    return await delete_otp_repo(otp_id , username , session)

