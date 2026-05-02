import sys
sys.path.append(".")
from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal, User
from pydantic import BaseModel
from auth import verify_password, create_token
class LoginRequest(BaseModel):
    email: str
    mot_de_passe: str
router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/login")
def login(request: LoginRequest, db= Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.mot_de_passe, user.mot_de_passe):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token_data = {"user_id": user.id_user, "role": user.role}
    access_token = create_token(token_data)
    return {"access_token": access_token, "token_type": "bearer","role": user.role}
