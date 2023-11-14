from db import get_db
import json
from dataclasses import dataclass
from typing import List


# Although strings are inefficient, good for MVP
@dataclass
class device:
    ip_addr : str
    mac_addr: str
    OUI_lookup: str
    deviceType: str
    #nmap results: ?
    known_dests: List[str]
    known_protos: List[str]
    flow_risks: List[float] #ids to read from list of risks used by ndpi
    flow_score: int


def ingest_file(filename: str):
    with open(filename, "r") as f:
        packets = [json.loads(line) for line in f]

    # for packet in packets:


    print(packets[3]["ndpi"])


if __name__ == "__main__":
    ingest_file("example.json")