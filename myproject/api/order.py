from fastapi import APIRouter, HTTPException, Depends
from myproject.database.models import Order
from myproject.database.schema import OrderSchema, OrderSchemaOut
from myproject.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

order_router = APIRouter(prefix='/order', tags=['Order CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@order_router.post('/', response_model=OrderSchema)
async def order_create(order: OrderSchema, db: Session = Depends(get_db)):
    order_db = Order(**order.dict())
    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db

@order_router.get('/', response_model=List[OrderSchemaOut])
async def order_list(db: Session = Depends(get_db)):
    return db.query(Order).all()

@order_router.get('/{order_id}', response_model=OrderSchemaOut)
async def order_detail(order_id: int, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()
    if not order_db:
        raise HTTPException(detail="Order not found", status_code=404)
    return order_db

@order_router.put('/{order_id}/', response_model=dict)
async def update_porder(order_id: int, order: OrderSchema, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()
    if not order_db:
        raise HTTPException(detail="Order not found", status_code=404)

    for order_key, order_value in order.dict().items():
        setattr(order_db, order_key, order_value)

    db.commit()
    db.refresh(order_db)
    return {'message': 'Order changed'}

@order_router.delete('/{order_id}/', response_model=dict)
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order_db = db.query(Order).filter(Order.id == order_id).first()
    if not order_db:
        raise HTTPException(detail="Order not found", status_code=400)

    db.delete(order_db)
    db.commit()
    return {'message': 'Order deleted'}
