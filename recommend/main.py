from fastapi import FastAPI
from .types import RecommendInput
from .recommend import preprocessing


app = FastAPI()


@app.get("/")
async def say_hello():
    return {"say": "hello"}


@app.post("/recommend")
async def recommend_size(recommend_input: RecommendInput):
    return preprocessing(recommend_input)
