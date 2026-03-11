from fastapi import APIRouter, HTTPException, Depends
from myproject.database.models import Store
from myproject.database.schema import StoreSchema, StoreSchemaOut
from myproject.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

store_router = APIRouter(prefix='/store', tags=['Store CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@store_router.post('/', response_model=StoreSchema)
async def store_create(store: StoreSchema, db: Session = Depends(get_db)):
    store_db = Store(**store.dict())
    db.add(store_db)
    db.commit()
    db.refresh(store_db)
    return store_db

@store_router.get('/', response_model=List[StoreSchemaOut])
async def store_list(db: Session = Depends(get_db)):
    return db.query(Store).all()

@store_router.get('/{store_id}', response_model=StoreSchemaOut)
async def store_detail(store_id: int, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if not store_db:
        raise HTTPException(detail="Store not found", status_code=404)
    return store_db

@store_router.put('/{store_id}/', response_model=dict)
async def update_store(store_id: int, store: StoreSchema, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if not store_db:
        raise HTTPException(detail="Store not found", status_code=404)

    for store_key, store_value in store.dict().items():
        setattr(store_db, store_key,store_value)

    db.commit()
    db.refresh(store_db)
    return {'message': 'Store changed'}

@store_router.delete('/{store_id}/', response_model=dict)
async def delete_store(store_id: int, db: Session = Depends(get_db)):
    store_db = db.query(Store).filter(Store.id == store_id).first()
    if not store_db:
        raise HTTPException(detail="Store not found", status_code=400)

    db.delete(store_db)
    db.commit()
    return {'message': 'Store deleted'}
