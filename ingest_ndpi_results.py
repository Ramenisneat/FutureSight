from db import get_db
import json


def ingest_file(filename: str):
    with open(filename, "r") as f:
        packets = [json.loads(line) for line in f]

    # for packet in packets:


    print(packets[0].keys())


if __name__ == "__main__":
    ingest_file("example.json")