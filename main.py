from fastapi import FastAPI,Depends,HTTPException,Query
from sqlalchemy.orm import Session
from database import engine,SessionLocal
import models,schemas
from auth import create_token,verify_token

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# db dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# login api
@app.post('/login')
def login():
    return {
        'access_token':create_token({'user':'admin'}),
        'token_type':'bearer'
    }

@app.get('/')
def home():
    return{
        'message':'Blog api started'
    }

# create blog (Protected)
@app.post('/blogs',response_model=schemas.BlogResponse)
def create_blog(blog:schemas.BlogCreate,db:Session=Depends(get_db),user=Depends(verify_token)):
    new_blog=models.Blog(
        title=blog.title,
        content=blog.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# read all blog
@app.get('/blogs')
def get_blogs(page:int = 1 ,limit:int=5,search:str=Query(default=''),db:Session=Depends(get_db)):
    query = db.query(models.Blog)
    if search:
        query = query.filter(models.Blog.title.ilike(f'%{search}'))

    total = query.count()
    start = (page-1)*limit
    blogs = query.offset(start).limit(limit).all()

    return {
        'page':page,
        'limit':limit,
        'total':total,
        'data':blogs
    }

# get specific blog (Protected)
@app.get('/blogs/{blog_id}',response_model=schemas.BlogResponse)
def get_specific_blog(blog_id:int,db:Session=Depends(get_db),user=Depends(verify_token)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404,
                            detail='Blog not found')
    return blog

# update blog api (Protected)
@app.put('/blogs/{blog_id}')
def update_blog(blog_id:int,blog:schemas.BlogCreate,db:Session=Depends(get_db),user=Depends(verify_token)):
    existing_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not existing_blog:
        raise HTTPException(status_code=404,
                            detail='Blog not found')
    existing_blog.title = blog.title
    existing_blog.content = blog.content
    db.commit()
    db.refresh(existing_blog)
    return existing_blog

# delete blog api (Protected)
@app.delete('/blogs/{blog_id}')
def delete_blog(blog_id:int,db:Session=Depends(get_db),user=Depends(verify_token)):
    # existing_blog = db.query(models.Blog).filter(models.id == blog_id).first()
    existing_blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    # if not existing_blog:
    #     raise HTTPException(status_code=404,
    #                         detail='Blog id is not found')
    if not existing_blog.first():
        raise HTTPException(status_code=404,
                            detail='Blog id is not found')
    existing_blog.delete()
    db.commit()
    return {
        'message':'Blog deleted sucessfully'
    }