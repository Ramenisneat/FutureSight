from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from db import engine, get_db, Base
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles



#This creates the main application.
app = FastAPI()
templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")

#This is an example of a API route.
#On whatever URL this app is hosted on, for example 127.0.0.1
#127.0.0.1/ will return with this JSON message 
@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("main_menu.html", {"request": request})

#CRUD stuff
Base.metadata.create_all(bind=engine)



# @app.post("/add")
# def addItem(item: schemas.ItemCreate, db: Session = Depends(get_db)):
#     return CRUDutils.create_item(db, item)

# @app.patch("/edit/{id}")
# def editItem(id: int, item : schemas.ItemUpdate, db: Session = Depends(get_db)):
#     return CRUDutils.update(db, id, item)

# @app.delete("/remove/{id}")
# def removeItem(id: int, db: Session = Depends(get_db)):
#     return CRUDutils.delete(db, id)

