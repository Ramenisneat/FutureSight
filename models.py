from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from db import Base
import json

class DeviceModel(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    ipaddr = Column(String, index=True)
    macaddr = Column(String, index=True)
    OUIlookup = Column(String, index=True)
    devicetype = Column(String, index=True)
    #serialized
    knowndests = Column(String, index=True)
    knownprotos = Column(String, index=True)
    flowrisks = Column(String, index=True)
    flowcount = Column(Integer, index=True)
    flowriskcount = Column(Integer, index=True)
    totalriskscore = Column(Integer, index=True)

    dateAdded = Column(DateTime, nullable=False, default=func.now())
    lastused = Column(DateTime, nullable=False, 
                        default=func.now(), onupdate=func.now())
    
    def __init__(self, ipaddr, macaddr, devicetype):
        self.ipaddr = ipaddr
        self.macaddr = macaddr
        self.devicetype = devicetype
        self.knowndests = "{}"
        self.knownprotos = "{}"
        self.flowrisks = "{}"
        self.totalriskscore = 0
        self.flowcount = 0
        self.flowriskcount = 0

    
    @property
    def dests(self):
        return json.loads(self.knowndests)
    
    @dests.setter
    def dests(self, value):
        temp = json.loads(self.knowndests)
        temp[value] = temp.get(value, 0) + 1
        self.knowndests = json.dumps(temp)

    @property
    def protos(self):
        return json.loads(self.knownprotos)


    @protos.setter
    def protos(self, value):
        temp = json.loads(self.knownprotos)
        temp[value] = temp.get(value, 0) + 1
        self.knownprotos = json.dumps(temp)
        self.flowcount += 1

    
    @property
    def risks(self):
        return json.loads(self.flowrisks)

    @risks.setter
    def risks(self, value):
        temp = json.loads(self.flowrisks)
        temp[value] = temp.get(value, 0) + 1
        self.flowrisks = json.dumps(temp)
        self.flowriskcount += 1

    
    

    
    #add tags later



"""
    columns to be added
    name: str
    description: str
    quantity: int
    dateAdded: datetime
    dateEdited: datetime
    tags: List[str]
"""