from fastapi import APIRouter, HTTPException, Depends
from myproject.database.models import Address
from myproject.database.schema import AddressSchema, AddressSchemaOut
from myproject.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

address_router = APIRouter(prefix='/address', tags=['Address CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@address_router.post('/', response_model=AddressSchema)
async def address_create(address: AddressSchema, db: Session = Depends(get_db)):
    address_db = Address(**address.dict())
    db.add(address_db)
    db.commit()
    db.refresh(address_db)
    return address_db

@address_router.get('/', response_model=List[AddressSchemaOut])
async def address_list(db: Session = Depends(get_db)):
    return db.query(Address).all()

@address_router.get('/{address_id}', response_model=AddressSchemaOut)
async def address_detail(address_id: int, db: Session = Depends(get_db)):
    address_db = db.query(Address).filter(Address.id ==address_id).first()
    if not address_db:
        raise HTTPException(detail="Address not found", status_code=404)
    return address_db

@address_router.put('/{address_id}/', response_model=dict)
async def update_address(address_id: int,address:AddressSchema, db: Session = Depends(get_db)):
    address_db = db.query(Address).filter(Address.id == address_id).first()
    if not address_db:
        raise HTTPException(detail="Address not found", status_code=404)

    for address_key, address_value in address.dict().items():
        setattr(address_db, address_key, address_value)

    db.commit()
    db.refresh(address_db)
    return {'message': 'Address changed'}

@address_router.delete('/{address_id}/', response_model=dict)
async def delete_address(address_id: int, db: Session = Depends(get_db)):
    address_db = db.query(Address).filter(Address.id == address_id).first()
    if not address_db:
        raise HTTPException(detail="Address not found", status_code=400)

    db.delete(address_db)
    db.commit()
    return {'message': 'Address deleted'}
