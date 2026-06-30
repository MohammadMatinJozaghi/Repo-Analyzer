from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped , mapped_column , relationship
from app.db.base import Base
from datetime import datetime



class Repo(Base):
    __tablename__='repos'
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]
    url:Mapped[str]
    node_id:Mapped[str]=mapped_column(unique=True)
    user_id:Mapped[int]=mapped_column(ForeignKey('users.id'))
    user:Mapped["User"]=relationship(back_populates='repos')
    created_at:Mapped[str]
    updated_at:Mapped[str]
    is_private:Mapped[bool]
    owner:Mapped[str]
    language:Mapped[str]
    stargazers_count:Mapped[int]
    watchers_count:Mapped[int]
    default_branch:Mapped[str]
    analyze:Mapped[str]=mapped_column(nullable= True)

