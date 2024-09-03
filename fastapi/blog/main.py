from fastapi import FastAPI
from blog.schema import Blog
from blog import models, schema
from blog.database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends

app = FastAPI()
# create the database
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog/create")
def create_blog(request: Blog, db: Session = Depends(get_db)):
    new_blog_data = models.Blog(
        id=request.id,
        title=request.title,
        author=request.author,
        written_date=request.written_date,
        content=request.content,
        likes=request.likes,
        published=request.published
    )
    db.add(new_blog_data)
    db.commit()
    db.refresh(new_blog_data)
    return {"message": "Blog created successfully", "data": new_blog_data}

