from pydantic import BaseModel
from typing import List

# Although strings are inefficient, good for MVP
class device(BaseModel):
    ip_addr : str
    mac_addr: str
    OUI_lookup: str
    deviceType: str
    #nmap results: ?
    #Serialized
    known_dests: str
    known_protos: str
    flow_risks: str #ids to read from list of risks used by ndpi
    flow_score: int

class deviceTemp(BaseModel):
    name: str
    ip_addr: str
    mac_addr: str
    device_type: str
    risks: List[str]
    score: str