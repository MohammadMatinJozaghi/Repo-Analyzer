from pydantic import BaseModel


class RepoURL(BaseModel):
    url:str
    
class RegisterRepoOut(BaseModel):
    analyze_text:str