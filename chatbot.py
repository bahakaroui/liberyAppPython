import sys
sys.path.append(".")
import google.generativeai as genai
from fastapi import APIRouter, Depends
from database import SessionLocal, Book, User
from pydantic import BaseModel

router = APIRouter()
genai.configure(api_key="AIzaSyDBNNh_L-_MyDgTxCIPBJcMXySFMJ8mvBc")
model = genai.GenerativeModel("gemini-2.0-flash")
class ChatMessage(BaseModel):
    message: str
    role: str = "user"
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/chat")
def chat(message: ChatMessage, db = Depends(get_db)):
    # 1. Get all books from DB
    books = db.query(Book).all()
    
    # 2. Format books as text
    books_list = "\n".join([
        f"- {b.titre} by {b.auteur} | category: {b.categorie} | status: {b.status} | quantity: {b.quantite_disponible}"
        for b in books
    ])
    
    # 3. Build smart prompt
    if message.role == "admin":
        role_rules = "The user is an ADMIN. They can ask anything about books and users."
    else:
        role_rules = "The user is a USER. Only answer questions about book availability."
    
    prompt = f"""You are a library assistant.
Here are the books in the library :
{books_list}

{role_rules}
Question : {message.message}"""

    # 4. Send to Gemini
    response = model.generate_content(prompt)
    return {"response": response.text}