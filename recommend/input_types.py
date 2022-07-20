from pydantic import BaseModel
from typing import List


class ProductInfo(BaseModel):
    category: str
    important_size: str
    size_margin: float


class ProductDetail(BaseModel):
    product_size: str
    size_chest: float
    size_back: float
    size_neck: float
    size_leg: float


class DogInfo(BaseModel):
    dog_type: str
    dog_weight: float
    dog_size_chest: float
    dog_size_back: float
    dog_size_neck: float
    dog_size_leg: float
    dog_age: float



class ProductRecommendInput(BaseModel):
    product_info: ProductInfo
    product_details: List[ProductDetail]
    dog_info: DogInfo
