from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default is true
    rating: Optional[int] = None


my_posts = [{"id": 1, "title": "title of post 1", "content": "content of post 1"},
            {"id": 2, "title": "title of post 2", "content": "content of post 2"}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get('/')
async def root():
    return {"message": "Hello world"}


@app.get("/posts")
def get_posts():
    # when sending array, fastapi automatically seralizes it to json
    return {"data": my_posts}


# using second parameter for default status code
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # pydantic model to dictionary
    post_dict = post.dict()
    # random id generation
    post_dict['id'] = randrange(0, 10000000)
    # append latest id wala to my_post list
    my_posts.append(post_dict)
    return {"message": "successfully created", "data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)

    if not post:
        # response.status_code = 404
        # we could even use status library if we forget status code
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Error: ": f"Post with id {id} not found"}

        # or use http exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id; {id} was not found")

    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesnt exits")

    my_posts.pop(index)
    # we cant send data when sending 404 not found
    # return{"message": "Successfully deleted", "Revised_data: ": my_posts}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post, response:Response):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} doesnt not exits to modify it")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict

    print(post)
    return {"data": post_dict}
