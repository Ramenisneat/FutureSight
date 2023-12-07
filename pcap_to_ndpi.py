import subprocess
from pathlib import Path
import sys
import datetime
from ingest_ndpi_results import ingest_file
import os


if (args_count := len(sys.argv)) > 2:
    print(f"One argument expected, got {args_count - 1}")
    raise SystemExit(2)
elif args_count < 2:
    print("You must specify the target .pcap")
    raise SystemExit(2)

target_pcap = Path(sys.argv[1])

date = datetime.datetime.now().strftime("%d %b %Y %H:%M:%S")

if str(target_pcap).endswith(".pcap"):
    p1 = subprocess.run(["ndpiReader", "-i", str(target_pcap), "-K", "json", "-k", f"{date}.json"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) 
    ingest_file(f"{date}.json")

    if os.path.exists(f"{date}.json"):
        os.remove(f"{date}.json")
    else:
        print("The file does not exist")

else:
    print("File must be .pcap")
    raise SystemExit(1)

