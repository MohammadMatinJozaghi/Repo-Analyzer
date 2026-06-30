from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User , OTPSignup


async def search_user_for_login(username:str,password:str,session:AsyncSession)->User|None:
    result=await session.execute(
        select(User).where(User.username == username)
    )
    user=result.scalars().first()
    if not user: 
        return None
    return user

    

async def search_user_for_signup_repo(data,session:AsyncSession)->User|None:
    search_user = await session.execute(
        select(User).where(
            (User.username == data.username) | (User.email == data.email)
            )
    )
    exist_user = search_user.scalars().first()
    return exist_user

async def signup_repo (data,session:AsyncSession):
    user=User(
        username=data.username, 
        password=User.hash_password(data.password), 
        email=data.email
    )
    return user


async def search_otp_signup_repo_and_delete(username:str,session:AsyncSession): 
    result=await session.execute(
        select(OTPSignup).where(
            OTPSignup.username == username
        )
    )
    otps=result.scalars().all()
    for otp in otps : 
        await session.delete(otp)
    await session.commit()
    return True



async def create_otp_signup_repo (code:str,username:str,session:AsyncSession)->OTPSignup: 
    otp_signup = OTPSignup(
        username = username , 
        code = code
    )
    session.add(otp_signup)
    await session.commit()
    await session.refresh(otp_signup)
    return otp_signup



async def verify_signup_repo (otp_id : int , data , session  : AsyncSession) -> OTPSignup|None :
    result = await session.execute(
        select(OTPSignup).where(
            OTPSignup.id == otp_id , OTPSignup.code == data.code
        )
    ) 
    otp = result.scalars().first()
    return otp


async def create_user_repo (user,session:AsyncSession)->User: 
    new_user = User(**user)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def delete_otp_repo (otp_id:int,username:str,session:AsyncSession): 
    qs = await session.execute(
        select(OTPSignup).where(OTPSignup.id == otp_id,OTPSignup.username == username) 
    )
    result=qs.scalars().first()
    await session.delete(result)
    await session.commit()
    return True



async def get_current_user_repo(user_id:int,session:AsyncSession)->User|None:
    qs=await session.execute(
        select(User).where(User.id == user_id)
    )
    result=qs.scalars().first()
    return result
