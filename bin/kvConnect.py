import requests, json, csv, os
from splunklib import client
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



def objectFromRow(row, fieldNames):
    pass
    masterDictionary = {}
    zipped = zip(fieldNames,row)
    for field, value in zipped:
        masterDictionary[field] = value

    return masterDictionary


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
            lookupReference = getRespectiveTableDictionary(kvName)
            lookupTable = lookupReference[1]
            for row in f_reader:
                
                if not firstLine:
                    obj = objectFromRow(row, fieldNames)
                    sObj = str(obj)
                    addIfDoesntExist(sObj, obj, lookupReference[0].keys(), lookupTable)
                else:
                    firstLine = False
                    fieldNames = row 
                    del fieldNames[-1]



def removeLinesNotPresent(csvPath, kvName, keyString):
    csvList = []
    with open(csvPath) as csv_file:
        row_count = sum(1 for row in csv_file)
        csv_file.seek(0)
        firstRow = True 
        if row_count <= 1:
            return
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            print(row)
            if not firstRow:
                obj = objectFromRow(row, fieldNames)
                sObj = str(obj)
                csvList.append(sObj)
            else:
                fieldNames = row
                firstRow = False
                del fieldNames[-1]
        print("CSV length before delete:{}".format(len(csvList)))
    
    # make csv dictionary
    lookup = getRespectiveTableDictionary(kvName)
    # print(lookup[0])
    lookUpKeys = lookup[0].keys()
    kvt = lookup[1]
    devDelete = True
    for k in lookUpKeys:
        # print("k:{}".format(k))
        if k not in csvList:
            print("deleting:{}*".format(k))
            kDelete = k.replace('\'','\"')
            #kvt.data.delete(k) 
            # print(kDelete)
            # print(key)
            # print(type(kDelete))
            # print(type(json.dumps(kDelete)))
            kvt.data.delete(kDelete) 
                

def addIfDoesntExist(sObj, obj, lookupKeys, table):
    # print(lookupKeys)
    # for j in range(len(lookupKeys)):
    #     print("luk:{}".format(lookupKeys[j]))
    #     print("csv:{}".format(sObj))
    if sObj not in lookupKeys:
        print("adding obj:\n{}".format(obj))
        dumped = json.dumps(obj)
        print("csv value dumped:{}".format(dumped))
        # print(type(obj))
        # print(type(json.dumps(obj)))
        table.data.insert(json.dumps(obj))

def getRespectiveTableDictionary(lookupName):
    masterDictionary = {}
    kvo = service.kvstore[lookupName]
    table = kvo.data.query()
    # print("kvo:\n\n\n")
    # print(table)
    # print(type(table))

    for r in table:
        try:
            nokey = r.pop('_key')
            __ = r.pop('_user')
        except:
            print("exception on:{}".format(keyEncoded))
            
        # print("r:{}".format(r))
        valueEncoded = {k: unicode(v).encode("utf-8") for k,v in r.iteritems()}
        # print("first:{}".format(valueEncoded))
        keyEncoded = {unicode(k).encode("utf-8"): v for k,v in valueEncoded.iteritems()}
        # print("second:{}".format(keyEncoded))
        # print(str(keyEncoded))
        # print(r.encode('utf-8'))

        withDouble = str(keyEncoded).replace('\'','\"')
        # print("retreiving kv TOKV:{}".format(withDouble))
        masterDictionary[str(keyEncoded)] = None
    return (masterDictionary, kvo)


def mainHandler():    
    for lookup, csvPath in devDictionary.items():    
        print("lookupname:{} lookupkey:{}, location:{}".format(lookup[0], lookup[1],csvPath))
        readOneCSV(csvPath, lookup[0], lookup[1])
        removeLinesNotPresent(csvPath, lookup[0], lookup[1])

mainHandler()
#readOneCSV()
#will it update the KVstore 
# kvstore is held in MongoDB

#1. Update KVstore via rest on dev instance
#2. Combine CSVs to one kvstorex`x
#3. onnect to DW-Splunk-dev

