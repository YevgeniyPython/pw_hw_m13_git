from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, schemas
from datetime import datetime, timedelta

async def create_contact(db: Session, contact: schemas.ContactCreate, user: models.User):
    contact = models.Contact(**contact.model_dump(), user_id = user.id)

    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def get_contact(db: Session, contact_id: int, user: models.User):
    return db.query(models.Contact).filter(and_(models.Contact.user_id == user.id, models.Contact.id == contact_id)).first()

async def get_contacts(db: Session, user: models.User, skip: int = 0, limit: int = 10):
    return db.query(models.Contact).filter(models.Contact.user_id == user.id).offset(skip).limit(limit).all()

async def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate, user: models.User):
    db_contact = db.query(models.Contact).filter(and_(models.Contact.user_id == user.id, models.Contact.id == contact_id)).first()
    for key, value in contact.model_dump().items():
        setattr(db_contact, key, value)
    db.commit()
    return db_contact

async def delete_contact(db: Session, contact_id: int, user: models.User):
    db_contact = db.query(models.Contact).filter(and_(models.Contact.user_id == user.id, models.Contact.id == contact_id)).first()
    db.delete(db_contact)
    db.commit()
    return db_contact

async def search_contacts(db: Session, query: str, user: models.User):
    return db.query(models.Contact).filter(models.Contact.user_id == user.id).filter(
        (models.Contact.first_name.ilike(f"%{query}%")) |
        (models.Contact.last_name.ilike(f"%{query}%")) |
        (models.Contact.email.ilike(f"%{query}%"))
    ).all()

async def get_birthdays_in_next_7_days(db: Session, user: models.User):
    today = datetime.today().date()
    next_week = today + timedelta(days=7)
    return db.query(models.Contact).filter(and_(models.Contact.user_id == user.id,
        models.Contact.birthday.between(today, next_week))
    ).all()



