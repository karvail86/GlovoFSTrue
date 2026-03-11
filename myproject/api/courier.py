from fastapi import APIRouter, HTTPException, Depends
from myproject.database.models import Courier
from myproject.database.schema import CourierSchema, CourierSchemaOut
from myproject.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

courier_router = APIRouter(prefix='/courier', tags=['Courier CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@courier_router.post('/', response_model=CourierSchema)
async def courier_create(courier: CourierSchema, db: Session = Depends(get_db)):
    courier_db = Courier(**courier.dict())
    db.add(courier_db)
    db.commit()
    db.refresh(courier_db)
    return courier_db

@courier_router.get('/', response_model=List[CourierSchemaOut])
async def courier_list(db: Session = Depends(get_db)):
    return db.query(Courier).all()

@courier_router.get('/{courier_id}', response_model=CourierSchemaOut)
async def courier_detail(courier_id: int, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id ==courier_id).first()
    if not courier_db:
        raise HTTPException(detail="Courier not found", status_code=404)
    return courier_db

@courier_router.put('/{courier_id}/', response_model=dict)
async def update_courier(courier_id: int, courier: CourierSchema, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if not courier_db:
        raise HTTPException(detail="Courier not found", status_code=404)

    for courier_key, courier_value in courier.dict().items():
        setattr(courier_db, courier_key, courier_value)

    db.commit()
    db.refresh(courier_db)
    return {'message': 'Courier changed'}

@courier_router.delete('/{courier_id}/', response_model=dict)
async def delete_courier(courier_id: int, db: Session = Depends(get_db)):
    courier_db = db.query(Courier).filter(Courier.id == courier_id).first()
    if not courier_db:
        raise HTTPException(detail="Courier not found", status_code=400)

    db.delete(courier_db)
    db.commit()
    return {'message': 'Courier deleted'}
