from fastapi import APIRouter , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.user import User
from app.schemas.repo import RepoURL,RegisterRepoOut
from app.services.repo import repo_create_service,project_structure_service,prompt_ai_service,save_analyze_repo
from app.utils.jwt import get_current_user
from app.utils.api_to_ai import ai_analyze


router=APIRouter()

@router.post('/',response_model=RegisterRepoOut)
async def register_repo(data:RepoURL,user:User=Depends(get_current_user),session:AsyncSession=Depends(get_db)):
    repo=await repo_create_service(data,user,session)
    structure=await project_structure_service(repo.owner,repo.name)
    prompt=await prompt_ai_service(repo,structure)
    analyze= await ai_analyze(prompt)
    await save_analyze_repo(repo,analyze,session)
    return analyze

    

