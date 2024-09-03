from fastapi import FastAPI
from typing import Optional

# all the data validation is done by pydantic
from pydantic import BaseModel

# creating an instance of FastAPI
app = FastAPI()

# function name doesn't matter
# what matters is the route
# it can even be the same name function for different routes. it will still work

# defining a path
@app.get("/")
def home():
    return {"message": 'FastAPI is great!'}

@app.get("/about")
def about():
    return {"message": 'This is the about page!'}

# paramaterized path
@app.get("/blog/{blog_id}") #dynamic path variable
def show_blog(blog_id: int = None): #here the path parameter should be same as that of the dynamic path variable
    blog_data = {"blog_id": blog_id, "title": "Blog Title", "content": "Blog Content"}
    return blog_data

@app.get("/blog/{blog_id}/comments")
def show_comments(blog_id: int):
    blog_data = {"blog_id": blog_id, "comments": ["comment1", "comment2"]}
    return blog_data

# # this will not work if the path is same as the above one and it reads line by line and executes the first match of dynamic path variable
# # to make it work, move this above the above one with dynamic path variable
# @app.get("/blog/unpublished")
# def unpublished():
#     unpublished_data = {"title": "Unpublished Blog", "content": "Unpublished Content"}
#     return unpublished_data

# query parameter
@app.get("/blog")
def show_blog(limit: int = 10, published: bool = True, sort : Optional[bool] = None): #removing the default value will make it mandatory to send the query parameter
    if published:
        blog_data = {"data": ["blog1", "blog2"], "limit": limit, "published": published}
    else:
        blog_data = {"data": ["blog1"], "limit": limit, "published": published}
    return blog_data


# differentiate btw query and path parameter
@app.get("/blog/query/{blog_id}")
def show_blog(blog_id: int, limit: int, published: bool = True, sort : Optional[bool] = None): #removing the default value will make it mandatory to send the query parameter
    if published:
        blog_data = {"data": ["blog1", "blog2"], "limit": limit, "published": published, "blog_id": blog_id}
    else:
        blog_data = {"data": ["blog1"], "limit": limit, "published": published, "blog_id": blog_id}
    return blog_data


# Post request

# creating a pydantic model
class Comment(BaseModel):
    commenter: str
    comment: str
    commented_date: str
class Blog(BaseModel):
    title: str
    author: str
    written_date: str
    content: str
    likes: int
    comments: Comment
    published: Optional[bool] 

# create a blog
@app.post("/blog")
def create_blog(request: Blog):
    # perform any operation here
    return request

