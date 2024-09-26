from fastapi import Depends, HTTPException
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from typing import List

from repository import contacts as repository_contacts
import models, schemas
from db import get_db
from services.auth import auth_service


router = APIRouter(prefix='/contacts', tags=["contacts"])


# Создать новый контакт
@router.post("/", response_model=schemas.Contact)
async def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db), 
                         current_user: models.User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(db, contact, current_user)

# Получить список всех контактов
@router.get("/", response_model=List[schemas.Contact])
async def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), 
                         current_user: models.User = Depends(auth_service.get_current_user)):
    return await repository_contacts.get_contacts(db, current_user,skip=skip, limit=limit,)


# @router.get("/", response_model=List[schemas.Contact], description='No more than 10 requests per minute',
#             dependencies=[Depends(RateLimiter(times=10, seconds=60))])
# async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
#                      current_user: models.User = Depends(auth_service.get_current_user)):
#     contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
#     return contacts



# Получить один контакт по идентификатору
@router.get("/{contact_id}", response_model=schemas.Contact)
async def read_contact(contact_id: int, db: Session = Depends(get_db), 
                         current_user: models.User = Depends(auth_service.get_current_user)):
    db_contact = await repository_contacts.get_contact(db, contact_id, current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

# Обновить контакт
@router.put("/{contact_id}", response_model=schemas.Contact)
async def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db), 
                         current_user: models.User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(db, contact_id, contact, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

# Удалить контакт
@router.delete("/{contact_id}")
async def delete_contact(contact_id: int, db: Session = Depends(get_db), 
                         current_user: models.User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.delete_contact(db, contact_id, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

# Поиск по имени, фамилии или email
@router.get("/contacts/search/", response_model=List[schemas.Contact])
async def search_contacts(query: str, db: Session = Depends(get_db), 
                         current_user: models.User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.search_contacts(db, query, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

# Контакты с днями рождения в ближайшие 7 дней
@router.get("/contacts/birthdays/", response_model=List[schemas.Contact])
async def upcoming_birthdays(db: Session = Depends(get_db), 
                         current_user: models.User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_birthdays_in_next_7_days(db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

