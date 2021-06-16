from typing import List
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import get_db
from models import Name as N

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class Name(BaseModel):
    name: str


def create_name(db: Session, name: Name):
    db_name = N(name=name.name)
    db.add(db_name)
    db.commit()
    db.refresh(db_name)
    return db_name


@app.post("/add_name")
def add_name(name: Name, db: Session = Depends(get_db)):
    db_name = create_name(db, name=name)
    return db_name


def get_names(db: Session):
    return db.query(N).all()


def create_name_response(query):
    return {'name': query.name}


@app.get("/get_name", response_model=List[Name])
def get_name(db: Session = Depends(get_db)):
    names = get_names(db)
    return [create_name_response(name) for name in names]


@app.get("/", response_model=List[Name])
def get(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
