from pyexpat import model
from typing import Optional
from fastapi import  Body, FastAPI
from fastapi.params import Body
from pydantic import BaseModel
app = FastAPI()



class Post(BaseModel):
    title: str
    content : str
    pubished : bool = True
    rating : Optional[int] = None


my_posts = [{"title": "title1" , "content":"content1","id":1 },{"title": "title12" , "content":"content12","id":2 }]
#path operations
#request Get method url : "/"

#"/" is the path we have to go in the url #root url
#app is an instance
#get is an HTTP METHOD
#app is used as decorator
#function with def and a decorator with @
#path operation fucntion named  as root for now
#return gets back msg to the user
@app.get("/")
async def root():
    return {"message":"welcome to my API !"}
    #return "shdhdhdh"


#decorator of an instance http method url
@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

"""
@app.post("/createposts")
async def create_posts(payLoad: dict = Body(...)):
    print(payLoad)
    return {"new_post":f"title: {payLoad['title']} content:{payLoad['content']}"}
#title:str, content:str, category

"""
@app.post("/createposts")
def create_posts(new_post : Post):
    print(new_post)
    print(new_post.dict())
    return {"data": new_post}
    #return {"new_post":f"title{payLoad['title']} content:{payLoad['content']}"}
