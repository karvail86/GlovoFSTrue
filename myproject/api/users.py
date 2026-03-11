from fastapi import APIRouter, HTTPException,Depends
from myproject.database.models import UserProfile
from myproject.database.schema import UserProfileSchema,UserProfileOutSchema
from myproject.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

user_router = APIRouter(prefix='/users', tags=['UserProfile CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.post('/', response_model=UserProfileSchema)
async def user_create(user: UserProfileSchema, db: Session = Depends(get_db)):
    user_db = UserProfile(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@user_router.get('/', response_model=List[UserProfileOutSchema])
async def user_list(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()

@user_router.get('/{user_id}/', response_model=UserProfileOutSchema)
async def user_detail(user_id:int,db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user_db:
        raise HTTPException(detail={'We don`t have information'}, status_code=400)
    return user_db

@user_router.put('/{user_id}/', response_model=dict)
async def update_user(user_id:int,user: UserProfileSchema,
                      db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user_db:
        raise HTTPException(detail={'We don`t have information'}, status_code=400)
    for user_key, user_value in user.dict().items():
     setattr(user_db,user_key, user_value)

    db.commit()
    db.refresh(user_db)
    return {'message': 'User change'}

@user_router.delete('/{user_id}/', response_model=dict)
async def user_delete(user_id:int,db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(detail={'We don`t have information'}, status_code=400)

    db.delete(user_db)
    db.commit()
    return {'message': 'User delete'}