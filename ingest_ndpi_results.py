from db import get_db
import json
from sqlalchemy.sql import exists    
import models
from db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def ingest_file(filename: str):



    db = SessionLocal()

    with open(filename, "r") as f:
        packets = [json.loads(line) for line in f]

    # for packet in packets:

    for flow in packets:
        if db.query(exists().where(models.ItemModel.ipaddr == flow["src_ip"])).scalar() > 0:
            #Update device
            print("found")
        
        else:
            #Totally new device
            print("not found")
    

    db.close()

if __name__ == "__main__":
    ingest_file("example.json")