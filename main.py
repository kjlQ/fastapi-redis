import json
from fastapi import FastAPI
import requests
import redis

app = FastAPI()

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/posts")
def read_root():
    cached_posts = redis_client.get("posts")

    if cached_posts:
        posts = json.loads(cached_posts)
    else:
        posts = requests.get('https://jsonplaceholder.typicode.com/posts').json()
        redis_client.setex("posts", 3600, json.dumps(posts))
  
    return {"Posts": posts}

@app.get("/posts/{id}")
def read_root(id):
    cached_post = redis_client.get(f"post_{id}")

    if cached_post:
        post = json.loads(cached_post)
    else:
        post = requests.get(f'https://jsonplaceholder.typicode.com/posts/{id}').json()
        redis_client.setex(f"post_{id}", 3600, json.dumps(post))
  
    return {"Post": post}