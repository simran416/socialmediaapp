# from importlib.resources import contents
# from multiprocessing import synchronize
# from typing import Optional,List
from fastapi import  Body, FastAPI
from . import models
from .database import engine,get_db
from .routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware

from app import database
from .config import Settings

# create db tables automtically
# models.Base.metadata.create_all(bind=engine)
# fetch('http://localhost:8000/').then(res=> res.json()).then(console.log)
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
#path operations
#request Get method url : "/"

#"/" is the path we have to go in the url #root url
#app is an instance
#get is an HTTP METHOD
#app is used as decorator
#function with def and a decorator with @
#path operation fucntion named  as root for now
#return gets back msg to the user
# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# class Post(BaseModel):
#     title: str
#     content : str
#     publish : bool = True
#     #rating : Optional[int] = None

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i

