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
        if  db.query(models.DeviceModel).filter(models.DeviceModel.ipaddr == flow["src_ip"]).first():
            #Update device
            db_item = db.query(models.DeviceModel).filter(models.DeviceModel.ipaddr == flow["src_ip"]).first()
            parse_flow(flow, db_item)

            #TODO:ANOMOLY DETECTION

            db.add(db_item)
            db.commit()
            db.refresh(db_item)
        
        else:
            #Totally new device
            #TODO:IDENTIFY DEVICE and MAC
            #TODO:NMAP SCAN with CVES
            db_item = models.DeviceModel(flow["src_ip"], "testing", "testing")
            parse_flow(flow, db_item)

            #TODO:ANOMOLY DETECTION

            db.add(db_item)
            db.commit()
            db.refresh(db_item)


    db.close()



def parse_flow(flow, db_item):
    db_item.dests = flow["dest_ip"]
    db_item.protos = flow["ndpi"]["proto"]
            
    if "flow_risk" in flow["ndpi"].keys():
        for risk in flow["ndpi"]["flow_risk"].values():
            db_item.risks = risk["risk"]
            # print(risk["risk_score"])
            db_item.totalriskscore += int(risk["risk_score"]["total"])

if __name__ == "__main__":
    ingest_file("example.json")