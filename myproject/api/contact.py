from fastapi import APIRouter, HTTPException, Depends
from myproject.database.models import Contact
from myproject.database.schema import ContactSchema, ContactSchemaOut
from myproject.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

contact_router = APIRouter(prefix='/contact', tags=['Contact CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contact_router.post('/', response_model=ContactSchema)
async def contact_create(contact: ContactSchema, db: Session = Depends(get_db)):
    contact_db = Contact(**contact.dict())
    db.add(contact_db)
    db.commit()
    db.refresh(contact_db)
    return contact_db

@contact_router.get('/', response_model=List[ContactSchemaOut])
async def contact_list(db: Session = Depends(get_db)):
    return db.query(Contact).all()

@contact_router.get('/{contact_id}', response_model=ContactSchemaOut)
async def contact_detail(contact_id: int, db: Session = Depends(get_db)):
    contact_db = db.query(Contact).filter(Contact.id ==contact_id).first()
    if not contact_db:
        raise HTTPException(detail="Contact not found", status_code=404)
    return contact_db

@contact_router.put('/{contact_id}/', response_model=dict)
async def update_contact(contact_id: int, contact: ContactSchema, db: Session = Depends(get_db)):
    contact_db = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact_db:
        raise HTTPException(detail="Contact not found", status_code=404)

    for contact_key, contact_value in contact.dict().items():
        setattr(contact_db, contact_key, contact_value)

    db.commit()
    db.refresh(contact_db)
    return {'message': 'Contact changed'}

@contact_router.delete('/{contact_id}/', response_model=dict)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact_db = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact_db:
        raise HTTPException(detail="Order not found", status_code=400)

    db.delete(contact_db)
    db.commit()
    return {'message': 'Contact deleted'}
