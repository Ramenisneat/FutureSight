from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from db import engine, get_db, Base



#This creates the main application.
app = FastAPI()
templates = Jinja2Templates(directory="app/templates/")

#This is an example of a API route.
#On whatever URL this app is hosted on, for example 127.0.0.1
#127.0.0.1/ will return with this JSON message 
@app.get("/")
def root(request: Request):
     return templates.TemplateResponse("index.html", {"request": request})


#CRUD stuff
Base.metadata.create_all(bind=engine)


@app.get("/items")
def getItems(request: Request, db: Session = Depends(get_db)):
    items = CRUDutils.get_items(db)
    return templates.TemplateResponse("items.html", {"request": request, "items": items})

@app.get("/item{id}")
def getItem(id: int, db: Session = Depends(get_db)):
    return CRUDutils.get_item(db, id)


@app.post("/add")
def addItem(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return CRUDutils.create_item(db, item)

@app.patch("/edit/{id}")
def editItem(id: int, item : schemas.ItemUpdate, db: Session = Depends(get_db)):
    return CRUDutils.update(db, id, item)

@app.delete("/remove/{id}")
def removeItem(id: int, db: Session = Depends(get_db)):
    return CRUDutils.delete(db, id)

