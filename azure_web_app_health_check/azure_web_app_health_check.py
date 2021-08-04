#
# documentation:
import requests
import json
import urllib3

# Return codes expected by Nagios
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

#Disable warnings https
urllib3.disable_warnings()

class AzureAppHealthChecks:
    def __init__(self, url, key):
        
        #initial
        self.url = url
        self.key = key
       

    def get_status_data(self):
            
        #Add tags to the URL
        url = self.url
        key = self.key

        # requests doc http://docs.python-requests.org/en/v0.10.7/user/quickstart/#custom-headers
        
        #Add key to URL
        url = url + "/health?key=" + key        

        r = requests.get(url=url, verify=False)
        
        return r.json(), r.status_code
    
    def check_status_data(self):

        #Vars
        retrcode = OK
		
        #Create tuple with json and status code
        azure_health_status = self.get_status_data()
        
        msgdata = ''
        msgerror = 'Healthy'
        retrperfdata = ''
        retrmsg = ''
        
        #Validate Data
        if azure_health_status[0]['status'] != 'Healthy':
            retrcode = CRITICAL
                        
            if retrcode != 0:
                msgerror += 'ERROR - Check your App Health'

        msgerror += msgdata
         
        return retrcode, msgerror
        