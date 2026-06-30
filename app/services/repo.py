from fastapi.exceptions import ValidationException,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.repo import Repo
from app.repositories.repo import create_repo_repository,save_analyze_repo
import httpx

async def repo_create_service(data,user,session:AsyncSession)->Repo:
    try:
        repo_url=data.url
        repo_list_url=repo_url.split('/')
        owner_name=repo_list_url[-2]
        repo_name=repo_list_url[-1]
        repo_url=f'https://api.github.com/repos/{owner_name}/{repo_name}'
    except Exception:
        raise HTTPException(
            status_code=401,
            detail='لطفا آدرس را به درستی وارد کنید'
        )
    async with httpx.AsyncClient() as client:
        response=await client.get(repo_url)
        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail='پروژه یافت نشد'
            )
        if response.status_code == 200:
            response_py:dict=response.json()
        
        repo=await create_repo_repository(response_py,repo_url,user,session)
        return repo


async def project_structure_service(repo_owner:str,repo_name:str):
    api=f'https://api.github.com/repos/{repo_owner}/{repo_name}/git/trees/main?recursive=1'
    async with httpx.AsyncClient() as client:
        response=await client.get(url=api)
        response_py:dict=response.json()
        return response_py['tree']
    

async def prompt_ai_service(repo,structure):
    prompt=f"""
        این اطلاعات یک پروژه گیت هاب هست که بهت میدم :
        نام:{repo.name}
        نویسنده:{repo.owner} 
        زمان ایجاد پروژه:{repo.created_at}
        آخرین ویرایش پروژه:{repo.updated_at}
        عمومی/خصوصی:{repo.is_private}
        زبان توسعه ی پروژه:{repo.language}
        تعداد استارز:{repo.stargazers_count}
        تعداد تماشا پروژه:{repo.watchers_count}

        حالا میخوام وقتی که این اطلاعات را دیدی و اینم از ساختار پروژه:
        {structure}
        میخوام یه آنالیز خیلی خفن بکنی از این پروژه 
        میخوام نقاط قوت و ضعف و چینش ساختار پروژه رو بگی
        اینکه از نام پروژه بگی آیا این پروژه جذاب هست یا نه و کارفرما ها 
        بهش توجه میکنن یا نه
        خیلی مرتب و شمرده شمرده بگو که گیچ کننده نباشه
    """
    return prompt


async def save_analyze_service(repo,msg,session):
    await save_analyze_repo(repo,msg,session)