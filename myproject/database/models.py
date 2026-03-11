
from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Integer, Text, String, Date,
     Enum, ForeignKey,
     DateTime
)
from datetime import date,datetime
from enum import Enum as PyEnum
from typing import List

class RoleChoices(PyEnum):
    client = 'client'
    owner = 'owner'
    courier = 'courier'




class UserProfile(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String, unique=True)
    phone_number: Mapped[str] = mapped_column(String)
    user_role: Mapped[str] = mapped_column(Enum(RoleChoices),default=RoleChoices.client)
    date_register : Mapped[date] = mapped_column(Date, default=date.today)

    owners: Mapped[List['Store']] = relationship(back_populates='owner',cascade='all, delete-orphan')
    client_order: Mapped[List['Order']] = relationship(back_populates='client', cascade='all, delete-orphan', foreign_keys='Order.client_id')
    courier_order: Mapped[List['Order']] = relationship(back_populates='courier', cascade='all, delete-orphan',foreign_keys='Order.courier_id')
    user_courier: Mapped[List['Courier']] = relationship(back_populates='couriers', cascade='all, delete-orphan')
    reviews: Mapped[List['Review']] =  relationship(back_populates='client_review',cascade='all, delete-orphan' )

    def __str__(self):
        return f'{self.first_name},{self.username}'


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    token_user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_token')
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(50))
    store_category: Mapped[List['Store']] = relationship(back_populates='category',cascade='all, delete-orphan' )

    def __str__(self):
        return self.category_name

class Store(Base):
    __tablename__ = 'store'

    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped[Category] = relationship(back_populates='store_category')
    store_name: Mapped[str] = mapped_column(String(30))
    store_img: Mapped[str] = mapped_column(String)
    descriptions: Mapped[str] = mapped_column(Text)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    owner: Mapped[UserProfile] = relationship(back_populates='owners')
    created_date: Mapped[date] = mapped_column(Date, default=date.today)
    store_contact: Mapped[List['Contact']] = relationship(back_populates='store', cascade='all, delete-orphan' )
    store_address: Mapped[List['Address']] = relationship(back_populates='address_store', cascade='all, delete-orphan' )
    product_store: Mapped[List['Product']] = relationship(back_populates='product_store',cascade='all, delete-orphan' )
    review_store:Mapped[List['Review']] = relationship(back_populates='store_review', cascade='all,delete-orphan')
    def __str__(self):
        return self.store_name


class Contact(Base):
    __tablename__ = 'contact'

    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store: Mapped[Store] = relationship(back_populates='store_contact')
    contact_name: Mapped[str] = mapped_column(String(30))
    contact_number: Mapped[str] = mapped_column(String)

    def __str__(self):
        return f'{self.store},{self.contact_name}'

class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    address_store: Mapped[Store] = relationship(back_populates='store_address')
    address_name: Mapped[str] = mapped_column(String(50))

    def __str__(self):
        return self.address_name

class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    product_store: Mapped[Store] = relationship(back_populates='product_store')
    product: Mapped[str] = mapped_column(String(50))
    product_img: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    product_description : Mapped[str] = mapped_column(Text)

    product_order: Mapped[List['Order']] = relationship(back_populates='product', cascade='all, delete-orphan')


class StatusChoices(PyEnum):
    pending = 'pending'
    canceled = 'canceled'
    delivered = 'delivered'



class Order(Base):
    __tablename__ = 'order'


    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    client: Mapped[UserProfile] = relationship(back_populates='client_order', foreign_keys=[client_id])
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped[Product] = relationship(back_populates='product_order')
    status: Mapped[str] = mapped_column(Enum(StatusChoices))
    delivery_address: Mapped[str] = mapped_column(Text)
    courier_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    courier: Mapped[UserProfile] = relationship(back_populates='courier_order',foreign_keys=[courier_id])
    created_at: Mapped[date] = mapped_column(Date, default=date.today)
    courier_order:Mapped[List['Courier']] = relationship(back_populates='current', cascade='all, delete-orphan')

    def __str__(self):
        return f'{self.client}, {self.product}, {self.status}'

class CourierStatusChoices(PyEnum):
    busy = 'busy'
    available = 'available'


class Courier(Base):
    __tablename__ = 'courier'

    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    couriers_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    couriers: Mapped[UserProfile] = relationship(back_populates='user_courier')
    current_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    current: Mapped[Order] = relationship(back_populates='courier_order')
    courier_status: Mapped[str] = mapped_column(Enum(CourierStatusChoices))
    review_courier: Mapped[List['Review']] = relationship(back_populates='courier_review', cascade='all, delete-orphan')

    def __str__(self):
        return f'{self.courier_status},{self.couriers}'

class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    client_review: Mapped[UserProfile] = relationship(back_populates='reviews')
    store_id:Mapped[int] = mapped_column(ForeignKey('store.id'))
    store_review:Mapped[Store] = relationship(back_populates='review_store')
    courier_id: Mapped[int] = mapped_column(ForeignKey('courier.id'))
    courier_review: Mapped[Courier] = relationship(back_populates='review_courier')
    text: Mapped[str] = mapped_column(Text)
    created_date:Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'{self.client_review}'