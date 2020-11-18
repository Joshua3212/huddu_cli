
from datetime import date
import time
import requests
import json
import os
import time
import paramiko
application = os.environ['APPLICATION']
username = os.environ["USERNAME"]
avatar_url = os.environ["AVATAR_URL"]

#application = "259722649429078348886562251714181589713"
#username = "heyhey"
#avatar_url = "a"

url = "http://192.168.0.21:8000/api/applications/"+application+"/detail/"

payload = 'data='
headers = {
    'Authorization': 'token 228eb0c7b1c08682d3598b1f0d6fd1b4f9a4b474',
}

response = requests.request("GET", url, headers=headers, data=payload)

ip = response.json()["internal_ip"]

output = ""

url = "http://192.168.0.21:8000/api/applications/"+application+"/data/"

headers = {
    'Authorization': 'token 228eb0c7b1c08682d3598b1f0d6fd1b4f9a4b474',
}

response = requests.request("GET", url, headers=headers)
data = json.loads(response.json()["data"])

cmd_list = ["echo '==> started deployment process'", "rm -r /data/files", "echo '==> cloning " + data["repository"]+"'", "git clone --single-branch --branch " + data["github_branch"] + " " + data["repository"] +
            " /data/files", "cat /data/files/launcher", "echo '==> installing packages'", "bash /data/deploy/packages.sh", "echo '==> build successful'"]
output = ""
launchers = ""

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect(ip, 22, "root", ".Sommer1", banner_timeout=200)

    for command in cmd_list:
        stdin, stdout, stderr = ssh.exec_command(command)
        outlines = stdout.readlines()
        resp = ''.join(outlines)
        if command == "cat /data/files/launcher":
            launchers = resp
        else:
            output = output + resp

    """
    launchers
    """

    launchers = launchers.split("\n")
    launchers.pop()

    oldLaunchers = data["launchers"]
    data["launchers"] = []
    # try:
    for i in launchers:
        try:
            def getOld():
                for a in oldLaunchers:
                    oldLauncher = a
                    if oldLauncher["launcher"] == i:
                        return oldLauncher
            oldLauncher = getOld()
            if oldLauncher["pid"]:
                old_pid = oldLauncher["pid"]
                old_status = oldLauncher["enabled"]
                data["launchers"].append(
                    {"launcher": i, "enabled": old_status, "pid": old_pid})
        except:
            data["launchers"].append(
                {"launcher": i, "enabled": False})

    """
    activity
    """
    try:
        data["activity"].append(
            {"date": str(date.today()), "status": "successful", "output": output, "action": "Building ", "user": username, "avatar_url": avatar_url})
    except:
        data["activity"] = []
        data["activity"].append(
            {"date": str(date.today()), "status": "successful", "output": output, "action": "Building ", "user": username, "avatar_url": avatar_url})
except:
    """
    activity
    """
    try:
        data["activity"].append(
            {"date": str(date.today()), "status": "failed", "output": "==> Connection was closed unexpectedly \n==> Please try again in a few seconds", "action": "Building ", "user": username, "avatar_url": avatar_url})
    except:
        data["activity"] = []
        data["activity"].append(
            {"date": str(date.today()), "status": "failed", "output": "==> Connection was closed unexpectedly \n==> Please try again in a few seconds", "action": "Building ", "user": username, "avatar_url": avatar_url})

url = "http://192.168.0.21:8000/api/applications/"+application+"/data/"

payload = {
    "data": json.dumps(data)
}
headers = {
    'Authorization': 'token 228eb0c7b1c08682d3598b1f0d6fd1b4f9a4b474',
}

response = requests.request("POST", url, headers=headers, data=payload)

data = response.json()
