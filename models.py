from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from db import Base

class ItemModel(Base):
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
    flowscore = Column(Integer, index=True)

    dateAdded = Column(DateTime, nullable=False, default=func.now())
    lastused = Column(DateTime, nullable=False, 
                        default=func.now(), onupdate=func.now())
    
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