## temptrack

Simple temperature tracker based on esp8266+dht22


### Usage
pip install -r requirements.txt

Just upload .ino on your esp(change ssidname and password) and host somwhere main.py with change ip of the esp in code

You can set different cooldown for requests in main.py file

### Usage timeline.py

usage: timeline.py [-h] [-s {1,2}] [-p seconds] [-t tickrate] [-m {1,2}] [-o filename] [-d filename]

Graph generator

optional arguments:

  -h, --help            show this help message and exit
  
  -s {1,2}, --show-graph {1,2}
  
                        1 — show temp and hum graph, 0 — not
                        
  -p seconds, --period seconds
  
                        Period of ticks in seconds
                        
  -t tickrate, --ticks tickrate
  
                        Count of ticks on the graph
                        
  -m {1,2}, --method {1,2}
  
                        Select method for averaging. 1 — by period, 2 — ticks
                        
  -o filename, --output filename
  
                        Filename for graph (jpg or png)
                        
  -d filename, --datafile filename
  
                        Filename for specific datafil

### To do

Start via cli with arguments: count of ticks, output, period✅

Filter for data.txt✅

Average stats for days, weeks, months

Telegram bot

Maybe shared server with stats, optional for everyone
