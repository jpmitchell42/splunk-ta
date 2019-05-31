
#config for connection settings
config = {
    "port":8089,
    'host':'localhost',
    'app':'',#Put the name of the app
    'owner':'nobody',
    'username':'',#Local Splunk username
    'password':''#Local Splunk Password
}


#Put all dictionaries that you want here. 
#Future fix - get rid of the primary key field
#(lookupname, primary_key): <absolute_path>
csvDictionary = {
    ('sompo_load_balancer_vips', 'IPAddr'):'/Applications/Splunk/etc/apps/gp_ta/bin/load_balancer_vips.csv',
    ('sompo_assets', 'ip'): '/Applications/Splunk/etc/apps/gp_ta/bin/assets.csv'
}

#dictionary used for development
devDictionary = {
    ('sompo_kv_dev', 'Name') : '/Applications/Splunk/etc/apps/gp_ta/bin/sompo_kv_dev.csv'
}


#README setting up the app
# Create local user
# Change config in config.py
# Add absolute paths
# Change inputs.conf
# Change runkv
# enable app