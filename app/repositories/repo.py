from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.repo import Repo
from app.models.user import User

async def create_repo_repository(response_py:dict,repo_url:str,user:User,session:AsyncSession)->Repo:
    repos=await session.execute(
        select(Repo).where(Repo.node_id == response_py['node_id'],Repo.user_id == user.id)
    )
    result=repos.scalars().first()
    if result:
        raise HTTPException(
            status_code=401,
            detail='این پروژه از قبل ثبت شده است'
        )
    repo=Repo(
            name=response_py['name'],
            url=repo_url,
            node_id=response_py['node_id'],
            user_id=user.id,
            user=user,
            created_at=response_py['created_at'],
            updated_at=response_py['updated_at'],
            is_private=response_py['private'],
            owner=response_py['owner']['login'],
            language=response_py['language'],
            stargazers_count=response_py['stargazers_count'],
            watchers_count=response_py['watchers_count'],
            default_branch=response_py['default_branch']
        )
    session.add(repo)
    await session.commit()
    await session.refresh(repo)
    return repo


async def save_analyze_repo(repo,msg,session:AsyncSession):
    repo.analyze=msg
    await session.commit()
    await session.refresh(repo)
    