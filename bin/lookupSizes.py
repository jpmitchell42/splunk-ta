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


#for c in service.kvstore:
 #   print(c.name)


def objectFromRow(row, fieldNames):
    pass
    masterDictionary = {}
    zipped = zip(fieldNames,row)
    for field, value in zipped:
        #print("value:{}, key:{}".format(v,k))
        masterDictionary[field] = value

    #print(masterDictionary)
    return masterDictionary
    #for val, name in zip(row, fieldNames):
        #print(val, name)


def readOneCSV(csvPath, kvName, keyString):
    with open(csvPath) as csv_file:
        f_reader = csv.reader(csv_file, delimiter=',')
        temp_dictionary = {}        
        row_count = sum(1 for row in csv_file)
        csv_file.seek(0)
        firstLine = True
        fieldNames = None
        rowNumber = 2
        if row_count > 1:
#            print("past row count check")
            lookupReference = getRespectiveTableDictionary(kvName)
            lookupTable = lookupReference[1]
            for row in f_reader:
                #print("in f_reader")
                #print(row)
                if not firstLine:
                    obj = objectFromRow(row, fieldNames)
             #       temp_dictionary.update({rowNumber:obj})              
                    if obj not in lookupReference[0].items():
                        print("adding obj:{}".format(obj))
                        lookupTable.data.insert(json.dumps(obj))
                    rowNumber = rowNumber + 1                    
                    #print(obj)
                    #print(keyString)
                    #print(obj[keyString])
                    #dwkv.data.insert(json.dumps(r))
                else:
                    firstLine = False
                    fieldNames = row
            #print(temp_dictionary)


def getRespectiveTableDictionary(lookupName):
    #print(lookupName)
    masterDictionary = {}
    kvo = service.kvstore[lookupName]
    table = kvo.data.query()
    #print(type(table))
    print(len(table))
    return len(table)

    
for lookup, csvPath in csvDictionary.items():    
    print("lookupname:{} lookupkey:{}, location:{}".format(lookup[0], lookup[1],csvPath))
    #print("reading csv")
    getRespectiveTableDictionary(lookup[0])

for lookup, csvPath in devDictionary.items():    
    print("lookupname:{} lookupkey:{}, location:{}".format(lookup[0], lookup[1],csvPath))
    #print("reading csv")
    getRespectiveTableDictionary(lookup[0])

#readOneCSV()
#will it update the KVstore 
# kvstore is held in MongoDB

#1. Update KVstore via rest on dev instance
#2. Combine CSVs to one kvstore
#3. Connect to DW-Splunk-dev
