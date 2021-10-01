#!/usr/bin/env python3
#
# follows steps from "Cisco UCS Rack-Mount Servers CIMC XML API Programmer's Guide"
# https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/c/sw/api/b_cimc_api_book/b_cimc_api_book_appendix_0110.html#reference_9DBE7486B7EE4F399398645FEC9333D9__section_9573C816410E4C2197CDBDB78FFF5534
#
__author__ = 'Alex Spirin (asp13.dev@gmail.com)'

import time
import requests
from subprocess import Popen
import xmltodict
import signal
import sys
from getpass import getpass

requests.packages.urllib3.disable_warnings()


def cimc_logout():
    print("\r[INFO] Logging out from " + server + "... ", end = '')
    cimc_xml_aaaLogout = "<aaaLogout cookie='%s' inCookie='%s'></aaaLogout>" % (cimc_session_cookie, cimc_session_cookie)
    r = requests.post(url_api,data=cimc_xml_aaaLogout,verify=False,headers=headers,timeout=http_timeout)
    response_dict = xmltodict.parse(r.text, attr_prefix='')
    if "outStatus" in response_dict["aaaLogout"]:
        print("success")
    elif "errorDescr" in response_dict["aaaLogout"]:
        print("failure")
        print("[ERROR] " + response_dict["aaaLogout"]["errorDescr"])
        print("[DEBUG] " + r.text)
    else:
        print("failure")
        print("[ERROR] 'outStatus' attribute is absent")
        print("[DEBUG] " + r.text + "HTTP code:" + str(r.status_code))
    sys.exit(0)


def signal_handler(sig, frame):
    cimc_logout()



#Setting principal variables
server = input("Enter CIMC IP address: ")
username = input("Enter user: ")
password = getpass("Enter password: ")
url_api = "https://" + server + "/nuova"
headers = {'Content-Type':'application/xml'}
http_timeout = 30


# Step 1. Logging in and retrieving a session cookie
cimc_xml_aaaLogin = "<aaaLogin inName='" + username + "' inPassword='" + password + "'></aaaLogin>"
print("\n[INFO] Checking HTTP response from " + server + "... ", end = '')
r = requests.post(url_api,data=cimc_xml_aaaLogin,verify=False,headers=headers,timeout=http_timeout)
response_dict = xmltodict.parse(r.text, attr_prefix='')
if r.status_code == 200:
    print("success")
else:
    print("failure)
    print("[ERROR] HTTP Status code error")
    print("[DEBUG] " + r.text + "HTTP code: " + str(r.status_code))    
    sys.exit(1)


print("[INFO] Logging into " + server + "... ", end = '')
if "outPriv" in response_dict["aaaLogin"]:
    print("success")
    signal.signal(signal.SIGINT, signal_handler)
elif "errorDescr" in response_dict["aaaLogin"]:
    print("failure")
    print("[ERROR] " + response_dict["aaaLogin"]["errorDescr"])
    print("[DEBUG] " + r.text)    
    sys.exit(1)
else:
    print("failure)
    print("[ERROR] 'outPriv' attribute is absent")
    print("[DEBUG] " + r.text + "HTTP code:" + str(r.status_code))    
    sys.exit(1)

print("[INFO] Looking for session cookie... ", end = '')
if "outCookie" in response_dict["aaaLogin"]:
    print("success")
    cimc_session_cookie = response_dict["aaaLogin"]["outCookie"]
    cimc_session_timeout = int(response_dict["aaaLogin"]["outRefreshPeriod"]) - 487

elif "errorDescr" in response_dict["aaaLogin"]:
    print("failure")
    print("[ERROR] " + response_dict["aaaLogin"]["errorDescr"])
    print("[DEBUG] " + r.text)

else:
    print("failure)
    print("[ERROR] 'outCookie' attribute is absent")
    print("[DEBUG] " + r.text + "HTTP code: " + str(r.status_code))    
    sys.exit(1)


# # Step 2. Generating temporary authentication tokens
cimc_xml_aaaGetComputeAuthTokens = "<aaaGetComputeAuthTokens  cookie='%s' />" % (cimc_session_cookie)
print("[INFO] Requesting temporary authentication tokens...   " , end = '')
r = requests.post(url_api,data=cimc_xml_aaaGetComputeAuthTokens,verify=False,headers=headers,timeout=http_timeout)
response_dict = xmltodict.parse(r.text, attr_prefix='')
if "outTokens" in response_dict["aaaGetComputeAuthTokens"]:
    print("success")
    cimc_auth_cookies = response_dict["aaaGetComputeAuthTokens"]["outTokens"].split(',')

    # Step 3. Forming URL to download the JNLP file using the tokens 
    kvm_url = "https://" + server + "/kvm.jnlp?cimcAddr=" + server + "&tkn1=" + cimc_auth_cookies[0] + "&tkn2=" + cimc_auth_cookies[1]

    # Step 4. Launching the KVM
    # viewer = Popen(["/Applications/OpenWebStart/OpenWebStart javaws.app/Contents/MacOS/JavaApplicationStub", kvm_url])
    print("[INFO] Launching java web start... ", end = '')
    process = Popen(["javaws", kvm_url])
    stdoutdata, stderrdata = process.communicate()
    if process.returncode == 0:
        print("success")
    else:
        print("ERROR: Return code: " + str(process.returncode))
        
    print("[INFO] Counting login session timeout. Press <ctrl-c> for graceful logout... ")

    cst_len = len(str(cimc_session_timeout))
    while cimc_session_timeout > 0 :    
        if len(str(cimc_session_timeout)) < cst_len:
            print('\r'+' ' * cst_len, end="")
            cst_len = len(str(cimc_session_timeout))
        print('\r%d'%cimc_session_timeout, end="")
        time.sleep(1)
        cimc_session_timeout -=  1
    
    if cimc_session_timeout == 0:
        print("\r[INFO] Exiting")
        sys.exit(0)

elif "errorDescr" in response_dict["aaaGetComputeAuthTokens"]:
    print("failure")
    print("[ERROR] " + response_dict["aaaGetComputeAuthTokens"]["errorDescr"])
    print("[DEBUG] " + r.text)

else:
    print("failure")
    print("[ERROR] 'outTokens' attribute is absent")
    print("[DEBUG] " + r.text + "HTTP code:" + str(r.status_code))    


# Executing graceful session logout
cimc_logout()
