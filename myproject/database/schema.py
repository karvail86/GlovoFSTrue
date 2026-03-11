from pydantic import BaseModel, EmailStr
from .models import StatusChoices, RoleChoices, CourierStatusChoices
from datetime import date, datetime

class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    phone_number: str
    user_role: RoleChoices
    email: EmailStr
    date_register: date

class UserProfileSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    phone_number: str
    user_role: RoleChoices
    email: EmailStr
    password: str

class CategorySchema(BaseModel):
    category_name: str

class CategoryOutSchema(BaseModel):
    id: int
    category_name: str

class StoreSchema(BaseModel):
    category_id:int
    store_name:str
    store_img:str
    descriptions:str
    owner_id:int

class StoreSchemaOut(BaseModel):
    id:int
    category_id:int
    store_name:str
    store_img:str
    descriptions:str
    owner_id:int
    created_date:date

class ContactSchemaOut(BaseModel):
    id: int
    store_id:int
    contact_name:str
    contact_number:str

class ContactSchema(BaseModel):
    store_id:int
    contact_name:str
    contact_number:str

class AddressSchemaOut(BaseModel):
    id:int
    store_id: int
    address_name: str

class AddressSchema(BaseModel):
    store_id: int
    address_name: str

class Login(BaseModel):
    username: str
    password: str

class ProductOutSchema(BaseModel):
    id: int
    store_id: int
    product: str
    product_img:str
    price:int
    product_description:str

class ProductSchema(BaseModel):
    store_id: int
    product_img:str
    product: str
    price:int
    product_description:str

class OrderSchemaOut(BaseModel):
    id:int
    client_id:int
    product_id:int
    status:StatusChoices
    delivery_address:str
    courier_id:int
    created_at:date

class OrderSchema(BaseModel):
    client_id:int
    product_id:int
    status:StatusChoices
    delivery_address:str
    courier_id:int

class CourierSchemaOut(BaseModel):
    id:int
    couriers_id:int
    current_id:int
    courier_status: CourierStatusChoices

class CourierSchema(BaseModel):
    couriers_id:int
    current_id:int
    courier_status: CourierStatusChoices

class ReviewOutSchema(BaseModel):
    id:int
    client_id:int
    store_id:int
    courier_id:int
    text:str
    created_date:datetime

class ReviewSchema(BaseModel):
    client_id:int
    store_id:int
    courier_id:int
    text:str
