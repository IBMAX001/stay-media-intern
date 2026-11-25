from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import engine, SessionLocal, Base
from models import InternDB

Base.metadata.create_all(bind=engine)   # creates the table if missing

app = FastAPI(title="STAY MEDIA Backend")


class InternCreate(BaseModel):
    name: str
    email: str
    role: str


class InternOut(InternCreate):
    id: int
    model_config = {"from_attributes": True}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Welcome to STAY MEDIA Python Backend Development"}


@app.get("/interns", response_model=list[InternOut])
def get_interns(db: Session = Depends(get_db)):
    return db.query(InternDB).all()


@app.get("/interns/{intern_id}", response_model=InternOut)
def get_intern(intern_id: int, db: Session = Depends(get_db)):
    intern = db.get(InternDB, intern_id)
    if not intern:
        raise HTTPException(status_code=404, detail="Intern not found")
    return intern


@app.post("/interns", response_model=InternOut, status_code=201)
def create_intern(intern: InternCreate, db: Session = Depends(get_db)):
    db_intern = InternDB(**intern.model_dump())
    db.add(db_intern)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    db.refresh(db_intern)
    return db_intern
