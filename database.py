from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from auth import hash_password
engine = create_engine('sqlite:///biblio.db',connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
class Book(Base):
    __tablename__ = 'books'
    id_livre = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String, nullable=False)
    auteur = Column(String, nullable=False)
    categorie = Column(String, nullable=False)
    annee_publication = Column(Integer, nullable=False)
    quantite_disponible = Column(Integer, nullable=False)
    status = Column(String, nullable=False,default='disponible')
class User(Base):
    __tablename__ = 'users'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String, nullable=True)
    prenom = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    mot_de_passe = Column(String, nullable=False)
    role = Column(String, nullable=False, default='user')
Base.metadata.create_all(engine)
def create_default_admin():
    db = SessionLocal()
    existing = db.query(User).filter(User.role == "admin").first()
    if not existing:
        hashed = hash_password("admin123")
        admin = User(
            nom="Admin",
            prenom="Admin",
            email="admin@library.com",
            mot_de_passe=hashed,
            role="admin"
        )
        db.add(admin)
        db.commit()
        print("✅ Default admin created !")
    db.close()
