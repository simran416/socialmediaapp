from sys import prefix
from typing import List,Optional
from urllib import response
from app import oauth2
from sqlalchemy import func
from fastapi import (APIRouter, Body, Depends, FastAPI, HTTPException,
                     Response, status)
from sqlalchemy.orm import Session

from .. import models, schemas,oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix ="/posts",
    tags =['Posts']
)




@router.get("/",response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
    current_user :int = Depends(oauth2.get_current_user),
    limit : int = 10, skip: int =0, search: Optional[str] ="" ):
   
    # posts = db.query(models.Post).all()
    posts = db.query(models.Post ,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,
    isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(
        search)).limit(limit).offset(skip).all()
   
    return  posts
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
   
    # cursor.execute("""SELECT * FROM posts """)
    # posts= cursor.fetchall()
    # print(posts)
    


@router.post("/" , status_code = status.HTTP_201_CREATED,
response_model = schemas.Post)
def create_posts(post:schemas.PostCreate , 
db: Session = Depends(get_db),
current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.id)
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post
    # post_dict = post.dict()
    # post_dict['id']=randrange(0,1000000)
    # my_posts.append(post_dict)
    # return{"data": post_dict} 
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s , %s , %s) """,(
    #     {post.title},{post.content},{post.published}))
    
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s , %s , %s) RETURNING """,
    # (post.title,post.content,post.published))
    # # return{"data": "created post"}
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(**post.dict())
    
   

@router.get("/latest")
def get_latest_post():
    #print(type(id))
    #return { "post_detail" : f"Here is post {id}"}
    post = my_posts[len(my_posts)-1]
    return  post



#id path parameter
@router.get("/{id}",response_model = schemas.PostOut)
def get_post(id : int, db: Session = Depends(get_db),
current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id ).first()
    post =  db.query(models.Post ,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,
    isouter= True).group_by(models.Post.id).filter(models.Post.id == id ).first()
    #print(type(id))
    #return { "post_detail" : f"Here is post {id}"}
    # post = find_post(id)
    # if not post:
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {'message': f "post with id : {id} was not found "}
    # #print(post)
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
    #                     detail = f"post with id {id} was not found")
    # return {"post_detail" : post}
    # cursor.execute("""SELECT * FROM posts  WHERE id = %s """ , (str(id), ))
    # post= cursor.fetchone()
    # print(post)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f "post with id : {id} was not found "}
    #print(post)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f"post with id {id} was not found")

    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")
    return  post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    #delete post 
    #find teh index in array that has required ID
    #my_posts.pop(index)
    # index= find_index_post(id)
  


@router.put("/{id}",response_model = schemas.Post )
def update_post(id : int, updated_post : schemas.PostCreate ,
 db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id )
    # index= find_index_post(id)
    post=post_query.first()
    # print(index)
    if post == None:
       raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = f"post with id {id} DOES NOT exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                        detail = f"not authorized to delete   {id} Cant be deleted")
 
    
    post_query.update(updated_post.dict(),synchronize_session = False)
    db.commit()                   
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] =post_dict                    
    # print( my_posts[index])
    # print(post_dict)
    return post_query.first()
# http://127.0.0.1:8000/docs
@router.get("/")
async def root():
    return {"message":"welcome to my API !"}
    #return "shdhdhdh"

@router.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return {"message":"sucesss"}
    #return "shdhdhdh"
#decorator of an instance http method url
@router.get("/")
def get_posts():
    return {"data": "This is your posts"}

"""
@app.post("/createposts")
async def create_posts(payLoad: dict = Body(...)):
    print(payLoad)
    return {"new_post":f"title: {payLoad['title']} content:{payLoad['content']}"}
#title:str, content:str, category


@app.post("/createposts")
def create_posts(new_post : Post):
    print(new_post)
    print(new_post.dict())
    return {"data": new_post}
    #return {"new_post":f"title{payLoad['title']} content:{payLoad['content']}"}
"""