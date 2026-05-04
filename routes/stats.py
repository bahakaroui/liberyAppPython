import sys
sys.path.append(".")
from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal, Book , User
from pydantic import BaseModel
router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.get("/stats")
def get_stats(db= Depends(get_db)):
    total_books = db.query(Book).count()
    total_available_books = db.query(Book).filter(Book.status == "disponible").count()
    borrowed_books = db.query(Book).filter(Book.status == "emprunté").count()
    reserved_books = db.query(Book).filter(Book.status == "réservé").count()
    total_users = db.query(User).filter(User.role == "user").count()
    total_admin_users = db.query(User).filter(User.role == "admin").count()
    return {"total_books": total_books, "total_available_books": total_available_books, "borrowed_books": borrowed_books, "reserved_books": reserved_books, "total_users": total_users, "total_admin_users": total_admin_users}