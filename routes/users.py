import sys
sys.path.append(".")
from fastapi.security import OAuth2PasswordBearer
from auth import decode_token, hash_password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal, User
from pydantic import BaseModel 
class UserCreate(BaseModel):
    nom: str
    prenom: str
    email: str
    mot_de_passe: str
    role: str = "user"
router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def get_current_user(token: str = Depends(oauth2_scheme), db= Depends(get_db)):
    payload  = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload
def get_current_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user
@router.post("/users")
def create_user(user: UserCreate, db= Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.mot_de_passe)
    new_user = User(
        nom=user.nom,
        prenom=user.prenom,
        email=user.email,
        mot_de_passe=hashed_password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.get("/users")
def get_users(db= Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    users = db.query(User).all()    
    return users
@router.get("/users/{user_id}")
def get_user(user_id: int, db= Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
@router.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate, db= Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    existing_user = db.query(User).filter(User.id_user == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    existing_user.nom = user.nom
    existing_user.prenom = user.prenom
    existing_user.email = user.email
    existing_user.mot_de_passe = hash_password(user.mot_de_passe)
    existing_user.role = user.role
    db.commit()
    db.refresh(existing_user)
    return existing_user
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db= Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    user = db.query(User).filter(User.id_user == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}


