
#config for connection settings
config = {
    "port":8089,
    'host':'localhost',
    'app':'gp_ta',
    'owner':'nobody',
    'username':'admin',
    'password':'Watertown001'##PULL FROM 1PASSWORD
}

csvDictionary = {
    ('sompo_load_balancer_vips', 'IPAddr'):'load_balancer_vips.csv',
    ('sompo_assets', 'ip'): 'assets.csv'
}

devDictionary = {
    ('sompo_kv_dev', 'Name') : '/Applications/Splunk/etc/apps/gp_ta/bin/sompo_kv_dev.csv'
}

clientid = ''
clientsecret = ''
