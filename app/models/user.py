from sqlalchemy import String , func , DateTime
from sqlalchemy.orm import Mapped, mapped_column , relationship
from datetime import datetime
from app.db.base import Base
from app.core.security import hash_password_manager


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(String(300) , unique= True)
    password : Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    joined_at : Mapped[datetime] = mapped_column(server_default= func.now())
    updated_at : Mapped[datetime] = mapped_column(nullable= True , onupdate= func.now())
    repos:Mapped[list["Repo"]]=relationship(back_populates='user')
    @classmethod
    def hash_password(cls,v:str):
        return hash_password_manager.hash(v)

    


class OTPSignup (Base) : 
    __tablename__='otpsignups'
    id:Mapped[int]=mapped_column(primary_key= True)
    username:Mapped[str]=mapped_column(unique= True)
    code:Mapped[int]
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone= True) , server_default= func.now())
    