import sys
sys.path.append(".")
from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal, Book
from pydantic import BaseModel
class BookCreate(BaseModel):
    titre: str
    auteur: str
    categorie: str
    annee_publication: int
    quantite_disponible: int = 1
    status: str = "disponible"
router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.get("/books")
def get_books(db= Depends(get_db)):
    books = db.query(Book).all()    
    return books
@router.post("/books")
def create_book(book: BookCreate, db= Depends(get_db)):
    new_book = Book(
        titre=book.titre,
        auteur=book.auteur,
        categorie=book.categorie,
        annee_publication=book.annee_publication,
        quantite_disponible=book.quantite_disponible,
        status=book.status
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book
@router.get("/books/{book_id}")
def get_book(book_id: int, db= Depends(get_db)):
    book = db.query(Book).filter(Book.id_livre == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
@router.put("/books/{book_id}")
def update_book(book_id: int, book: BookCreate, db= Depends(get_db)):
    existing_book = db.query(Book).filter(Book.id_livre == book_id).first()
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    existing_book.titre = book.titre
    existing_book.auteur = book.auteur
    existing_book.categorie = book.categorie
    existing_book.annee_publication = book.annee_publication
    existing_book.quantite_disponible = book.quantite_disponible
    existing_book.status = book.status
    db.commit()
    db.refresh(existing_book)
    return existing_book
@router.delete("/books/{book_id}")
def delete_book(book_id: int, db= Depends(get_db)):
    book = db.query(Book).filter(Book.id_livre == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"detail": "Book deleted successfully"}
