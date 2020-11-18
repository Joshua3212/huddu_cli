import paramiko
import time
import requests
import json
import os
import time
from datetime import date
application = os.environ['APPLICATION']
languagePackage = os.environ["LANGUAGEPACKAGE"]
username = os.environ["USERNAME"]
avatar_url = os.environ["AVATAR_URL"]
action = os.environ["ACTION"]


#application = "259722649429078348886562251714181589713"
#languagePackage = "https://github.com/huddu-resources/nodejs-language-package.git"
#username = "some@mail.com"
#avatar_url = "someUrl.com"
#action = "remove"


url = "http://192.168.0.21:8000/api/applications/"+application+"/detail/"

payload = 'data='
headers = {
    'Authorization': 'token 228eb0c7b1c08682d3598b1f0d6fd1b4f9a4b474',
}

response = requests.request("GET", url, headers=headers, data=payload)

ip = response.json()["internal_ip"]

url = "http://192.168.0.21:8000/api/applications/"+application+"/data/"

headers = {
    'Authorization': 'token 228eb0c7b1c08682d3598b1f0d6fd1b4f9a4b474',
}

response = requests.request("GET", url, headers=headers)
data = json.loads(response.json()["data"])

if action == "add":
    cmd_list = ["rm -r  /data/'Language Packages'/'" + languagePackage[19:-4].replace("/", "%") + "'", "git clone " + languagePackage +
                " /data/'Language Packages'/'" + languagePackage[19:-4].replace("/", "%") + "'", "bash /data/'Language Packages'/'" + languagePackage[19:-4].replace("/", "%") + "'/install.sh", "bash /data/'Language Packages'/'" + languagePackage[19:-4].replace("/", "%") + "'/build.sh"]
else:
    cmd_list = ["bash /data/'Language Packages'/'" + languagePackage[19:-4].replace("/", "%") + "'/uninstall.sh", "rm -r  /data/'Language Packages'/'" +
                languagePackage[19:-4].replace("/", "%") + "'"]

output = ""

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, "root", ".Sommer1", banner_timeout=200)

    for command in cmd_list:
        stdin, stdout, stderr = ssh.exec_command(command)
        outlines = stdout.readlines()
        resp = ''.join(outlines)
        output = output + resp

    """
    activity
    """

    if action == "add":
        try:
            data["activity"].append(
                {"date": str(date.today()), "status": "successful", "action": f"Added Language Package: {languagePackage[19:-4]} ", "user": username, "avatar_url": avatar_url, "output": output})
        except:
            data["activity"] = []
            data["activity"].append(
                {"date": str(date.today()), "status": "successful", "action": f"Added Language Package: {languagePackage[19:-4]} ", "user": username, "avatar_url": avatar_url, "output": output})
    else:
        try:
            data["activity"].append(
                {"date": str(date.today()), "status": "successful", "action": f"Removed Language Package: {languagePackage[19:-4]} ", "user": username, "avatar_url": avatar_url, "output": output})
        except:
            data["activity"] = []
            data["activity"].append(
                {"date": str(date.today()), "status": "successful", "action": f"Removed Language Package: {languagePackage[19:-4]} ", "user": username, "avatar_url": avatar_url, "output": output})

except:
    if action == "add":
        try:
            data["activity"].append(
                {"date": str(date.today()), "status": "failed", "output": "==> Connection was closed unexpectedly \n==> Please try again in a few seconds", "action": f"Added Language Package: {languagePackage[19:-4]} ", "user": username, "avatar_url": avatar_url, "output": output})
        except:
            data["activity"] = []
            data["activity"].append(
                {"date": str(date.today()), "status": "failed", "output": "==> Connection was closed unexpectedly \n==> Please try again in a few seconds", "action": f"Added Language Package: {languagePackage[19:-4]} ", "user": username, "avatar_url": avatar_url, "output": output})
    else:
        try:
            data["activity"].append(
                {"date": str(date.today()), "status": "failed", "output": "==> Connection was closed unexpectedly \n==> Please try again in a few seconds", "action": f"Removed Language Package: {languagePackage[19:-4]} ", "user": username, "avatar_url": avatar_url, "output": output})
        except:
            data["activity"] = []
            data["activity"].append(
                {"date": str(date.today()), "status": "failed", "output": "==> Connection was closed unexpectedly \n==> Please try again in a few seconds", "action": f"Removed Language Package: {languagePackage[19:-4]} ", "user": username, "avatar_url": avatar_url, "output": output})

"""
Updating launcher pid
"""

url = "http://192.168.0.21:8000/api/applications/"+application+"/data/"

payload = {
    "data": json.dumps(data)
}
headers = {
    'Authorization': 'token 228eb0c7b1c08682d3598b1f0d6fd1b4f9a4b474',
}

response = requests.request("POST", url, headers=headers, data=payload)
