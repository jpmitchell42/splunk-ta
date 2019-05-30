import requests, json, csv, urllib3
import splunklib.client as client

from config import config as c, csvDictionary, devDictionary
PORT = c['port']
HOST = c['host']
APP = c['app']
OWNER = c['owner']

USERNAME = c['username']
PASSWORD = c['password']


service = client.connect(
    host=HOST,
    port=PORT,
    username=USERNAME,
    password=PASSWORD,
    app=APP,
    owner=OWNER
)



def getRespectiveTableDictionary(lookupName):
    masterDictionary = {}
    kvo = service.kvstore[lookupName]
    table = kvo.data.query()
    # print(len(table))
    return len(table)

    
for lookup, csvPath in csvDictionary.items():    
    lengthTable = getRespectiveTableDictionary(lookup[0])
    print("lookupname:{} lookupkey:{}, location:{}\nEntries:{}".format(lookup[0], lookup[1],csvPath, lengthTable))
    

for lookup, csvPath in devDictionary.items():    
    lengthTable = getRespectiveTableDictionary(lookup[0])
    print("lookupname:{} lookupkey:{}, location:{}\nEntries:{}".format(lookup[0], lookup[1],csvPath, lengthTable))


#readOneCSV()
#will it update the KVstore 
# kvstore is held in MongoDB

#1. Update KVstore via rest on dev instance
#2. Combine CSVs to one kvstore
#3. Connect to DW-Splunk-dev
