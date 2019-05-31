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


def runTests():
    print("testing")
    #place tests here

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



    



