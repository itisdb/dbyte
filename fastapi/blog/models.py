from sqlalchemy import Column, Integer, String, Text, String, Boolean
from blog.database import Base


class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    written_date = Column(String)
    content = Column(Text)
    likes = Column(Integer)
    published = Column(Boolean)
