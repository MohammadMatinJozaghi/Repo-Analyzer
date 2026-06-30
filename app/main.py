from fastapi import FastAPI

from app.api.routers.user import router as user_router
from app.api.routers.repo import router as repo_router

app = FastAPI()
app.include_router(user_router)
app.include_router(repo_router,prefix='/repos')


@app.get("/")
async def root():
    return {"status": "ok"}
