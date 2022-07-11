from fastapi import FastAPI
from .types import ProductRecommendInput, DogInfo
from .recommend_product import preprocessing
from .recommend_dog_size import recommend_dog_size

app = FastAPI()


@app.get("/")
async def say_hello():
    return {"say": "hello"}


@app.post("/v1/recommend/product")
async def recommend_product_size(recommend_input: ProductRecommendInput):
    return preprocessing(recommend_input)


@app.post("/v1/recommend/dog")
async def recommend_dog(recommend_input: DogInfo):
    return recommend_dog_size(recommend_input)
