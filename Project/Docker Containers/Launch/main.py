import paramiko
import time
import requests
import json
import os
import time
from datetime import date
application = os.environ['APPLICATION']
launcher = os.environ['LAUNCHER']
username = os.environ["USERNAME"]
avatar_url = os.environ["AVATAR_URL"]
action = os.environ["ACTION"]

#
#application = "259722649429078348886562251714181589713"
#launcher = "python3 aFile.py"
#ip = "92.246.85.69"
#username = "some@mail.com"
#avatar_url = "someUrl.com"
#action = "disable"
#

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

if action == "enable":
    cmd_list = ["bash /data/resources/runLauncher.sh " + launcher]
else:
    for i in data["launchers"]:
        if i["launcher"] == "launch: " + launcher:
            cmd_list = ["kill "+str(i["pid"])[:-1]]
            i["pid"] = ""

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

    if action == "enable":
        try:
            data["activity"].append(
                {"date": str(date.today()), "status": "successful", "action": f"Launching {launcher} ", "user": username, "avatar_url": avatar_url})
        except:
            data["activity"] = []
            data["activity"].append(
                {"date": str(date.today()), "status": "successful", "action": f"Launching {launcher} ", "user": username, "avatar_url": avatar_url})
    else:
        try:
            data["activity"].append(
                {"date": str(date.today()), "status": "successful", "action": f"Disabling {launcher} ", "user": username, "avatar_url": avatar_url})
        except:
            data["activity"] = []
            data["activity"].append(
                {"date": str(date.today()), "status": "successful", "action": f"Disabling {launcher} ", "user": username, "avatar_url": avatar_url})

    """
    Updating launcher pid
    """
    if action == "enable":
        for i in data["launchers"]:
            if i["launcher"] == "launch: " + launcher:
                i["pid"] = output
    else:
        for i in data["launchers"]:
            if i["launcher"] == "launch: " + launcher:
                i["pid"] = ""
except:
    """
    activity
    """
    if action == "enable":
        try:
            data["activity"].append(
                {"date": str(date.today()), "status": "failed", "output": "==> Connection was closed unexpectedly \n==> Please try again in a few seconds", "action": f"Launching {launcher} ", "user": username, "avatar_url": avatar_url})
        except:
            data["activity"] = []
            data["activity"].append(
                {"date": str(date.today()), "status": "failed", "output": "==> Connection was closed unexpectedly \n==> Please try again in a few seconds", "action": f"Launching {launcher} ", "user": username, "avatar_url": avatar_url})
    else:
        try:
            data["activity"].append(
                {"date": str(date.today()), "status": "failed", "output": "==> Connection was closed unexpectedly \n==> Please try again in a few seconds", "action": f"Disabling {launcher} ", "user": username, "avatar_url": avatar_url})
        except:
            data["activity"] = []
            data["activity"].append(
                {"date": str(date.today()), "status": "failed", "output": "==> Connection was closed unexpectedly \n==> Please try again in a few seconds", "action": f"Disabling {launcher} ", "user": username, "avatar_url": avatar_url})


url = "http://192.168.0.21:8000/api/applications/"+application+"/data/"

payload = {
    "data": json.dumps(data)
}
headers = {
    'Authorization': 'token 228eb0c7b1c08682d3598b1f0d6fd1b4f9a4b474',
}

response = requests.request("POST", url, headers=headers, data=payload)
