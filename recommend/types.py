from pydantic import BaseModel
from typing import List


class ProductInfo(BaseModel):
    product_uuid: str
    seller_uuid: str
    product_name: str
    product_img: List[str]
    product_hashtag: List[str]
    product_price: int
    product_effective_price: int
    product_discount_ratio: int
    product_create_time: str


class ProductDetail(BaseModel):
    product_color: str
    product_size: str
    size_add_price: int
    product_stock: bool
    product_sales: int
    size_chest: float
    size_back: float
    size_leg: float
    size_margin: float


class DogInfo(BaseModel):
    dog_uuid: str
    user_uuid: str
    dog_nickname: str
    dog_type: str
    dog_gender: str
    dog_weight: float
    dog_size_img: str | None
    dog_size_chest: float
    dog_size_back: float
    dog_size_neck: float
    dog_size_leg: float
    dog_create_time: str
    is_default: bool
    is_delete: bool


class RecommendInput(BaseModel):
    product_info: ProductInfo
    product_details: List[ProductDetail]
    dog_info: DogInfo
