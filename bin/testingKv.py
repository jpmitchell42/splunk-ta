import requests, json, csv, sys
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



service = client.connect(
    host=HOST,
    port=PORT,
    username=USERNAME,
    password=PASSWORD,
    app=APP,
    owner=OWNER
)


def runTests():
    print("testing")

def addElements(numb):
    import datetime
    d = datetime.datetime.now().strftime("%m-%d %H:%M:%S")
 
    with open("sompo_kv_dev.csv", "a") as dev_csv:
        for i in range(1,int(numb)+1):
            appendString = "col1-{e}-{da},col2-{e}-{da},col3-{e}-{da},col4-{e}-{da}\n".format(da=str(d), e=i)
            dev_csv.write(appendString)
            print(appendString)
try:
    num = sys.argv[1]
    print(num)
    if num == 'test':
        runTests()
    else:
        addElements(num)        
except IndexError:
    print("no arguments provided")
    sys.exit()

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
           # print("past row count check")
            lookupReference = getRespectiveTableDictionary(kvName)
            lookupTable = lookupReference[1]
            for row in f_reader:
                #print("in f_reader")
                #print(row)
                if not firstLine:
                    obj = objectFromRow(row, fieldNames)
                    sObj = str(obj)
                    addIfDoesntExist(sObj, obj, lookupReference[0].keys(), lookupTable)
                else:
                    firstLine = False
                    fieldNames = row 
                    del fieldNames[-1]


def addIfDoesntExist(sObj, obj, lookupKeys, table):
    if sObj not in lookupKeys:
        print("adding obj:\n{}".format(obj))
        table.data.insert(json.dumps(obj))

def getRespectiveTableDictionary(lookupName):
    print(lookupName)
    masterDictionary = {}
    kvo = service.kvstore[lookupName]
    table = kvo.data.query()
    print(type(table))
    print(len(table))
    for r in table:
        print(r)
        nokey = r.pop('_key')
        __ = r.pop('_user')
        #___ = r.pop('wait')
        masterDictionary[str(r)] = None        
        #print(r)
        #print("user: {} wait: {}".format(__,___ ))
        #import sys as _
        #print(masterDictionary)
        #print(table)
        
 #   _.exit()
    return (masterDictionary, kvo)

    



