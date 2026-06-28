from sqlalchemy import Column,Integer,String,Float,Text
from database import Base

class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    title = Column(String)
    content = Column(Text)
