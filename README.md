# FutureSight

Solution to parse network traffic, monitor and detect vulnerabilites on home network devices


# Usage

Two step solutions:
1) Parse pcap data to backend
2) Run Frontend API to see results

First install all requirements from `requirements.txt`. I suggest to use a python venv

To parse pcap, run `python pcap_to_ndpi.py path/to/.pcap`
The rest of the steps should be taken care of in `ingest_ndpi_results` called from `pcap_to_ndpi`
NOTE: mac_addr, OUI_lookup and nmap scanning are commented out in `ingest_file` func as sample pcaps were used.

To view frontend, run `python run.py` and the pages are viewable at `localhost:8000` 
