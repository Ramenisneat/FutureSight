from db import get_db
import json
from sqlalchemy.sql import exists    
import models
from db import SessionLocal, engine
import nmap
import arpreq
import requests
import netifaces

models.Base.metadata.create_all(bind=engine)

def ingest_file(filename: str):
    db = SessionLocal()

    with open(filename, "r") as f:
        packets = [json.loads(line) for line in f]

    # for packet in packets:

    addrs = netifaces.ifaddresses('wlp6s0')

    subnet = addrs[netifaces.AF_INET][0]['netmask']
    af_inet = addrs[netifaces.AF_INET][0]['addr']

    #TODO: VERY SIMPLE AND DUMB MASKING SHOULD CHANGE
    def in_submask(ip):
        for group in subnet.split("."):
            i = 0
            if (group == "255"):
                if af_inet.split(".")[i] != ip.split(".")[i]:
                    return False
            i = i + 1
        
        return True


    #TODO: Enforce srcs from subnet

    for flow in packets:
        #Ignoring ipv6 srcs for now
        if (":" in  flow["src_ip"]):
            continue

        if (not in_submask(flow["src_ip"])):
            continue


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
            #TODO:IDENTIFY DEVICE 

            print(flow["src_ip"])

            # try:
            #     mac_addr = arpreq.arpreq(flow["src_ip"])
            #     oui_lookup = OUI_lookup(mac_addr)
            # except:
            #     print("error searching mac addr")
                
            # print(mac_addr)
            # print(oui_lookup)

            mac_addr = "default"
            oui_lookup = "default"

            #TODO: OFFLOAD NMAP SCAN TO CHILD PROCESS
            
            # cves = nmap_scan(flow["src_ip"])
            cves = []
            db_item = models.DeviceModel(flow["src_ip"], mac_addr, oui_lookup)
            parse_flow(flow, db_item)

            if cves:
                for cve in cves:
                    db_item.cves = cve

            #TODO:ANOMOLY DETECTION

            db.add(db_item)
            db.commit()
            db.refresh(db_item)


    db.close()

def nmap_scan(ipaddr: str):
    nm = nmap.PortScanner()

    result = nm.scan(hosts=ipaddr, arguments="nmap -sV --script nmap-vulners/")
    #TODO: Make sure to raise exception if no vulners
    # print(result)
    try:
        for k in result["scan"][ipaddr]["tcp"].values():
            if "script" in k:
                if "vulners" in k["script"]:
                    vulners = list(map(str.strip,k["script"]["vulners"].split("\n")))

                    exploits = [vuln for vuln in vulners if "EXPLOIT" in vuln]
                    CVEs = [cve.split("\t")[0] for cve in exploits]
                    if CVEs == None:
                        return []
                    return CVEs
    except:
        return []

def OUI_lookup(mac_addr: str):
    r = requests.get(url = f"https://api.macvendors.com/{mac_addr}")
    if "errors" in r.text:
        return "Unknown vendor"
    return r.text


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