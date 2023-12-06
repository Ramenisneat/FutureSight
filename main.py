from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from db import engine, get_db, Base
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from models import DeviceModel
from schemas import deviceTemp



#This creates the main application.
app = FastAPI()
templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")

#This is an example of a API route.
#On whatever URL this app is hosted on, for example 127.0.0.1
#127.0.0.1/ will return with this JSON message 
@app.get("/")
def root(request: Request, db: Session = Depends(get_db)):
    devices = db.query(DeviceModel).offset(0).limit(100).all()
    result=[]
    for i in devices:
        result.append({"name": i.ipaddr, "type": i.devicetype, "id": i.id})
    print(result)
    return templates.TemplateResponse("main_menu.html", {"request": request, "devices" : result})



@app.get("/view/{id}")
def root(id:str, request: Request, db: Session = Depends(get_db)):
    device = db.query(DeviceModel).filter(DeviceModel.id == id).first()
    result = deviceTemp(
    name = device.OUIlookup if device.OUIlookup != None else "default",
    ip_addr = device.ipaddr,
    mac_addr = device.macaddr,
    score = str(round(device.totalriskscore / device.flowriskcount)),
    device_type = device.devicetype,
    risks = list(device.risks)
    )
    return templates.TemplateResponse("Device_Info.html", {"request": request, "device": dict(result)})



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

