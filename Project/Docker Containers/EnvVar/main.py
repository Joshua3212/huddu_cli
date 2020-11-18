import time
import requests
import json
import os
import time
import paramiko
from datetime import date
application = os.environ['APPLICATION']
key = os.environ['KEY']
value = os.environ["VARIABLE"]
ip = os.environ['IP']
username = os.environ["USERNAME"]
avatar_url = os.environ["AVATAR_URL"]
action = os.environ["ACTION"]

#
#application = "259722649429078348886562251714181589713"
#key = "TEST"
#value = "ellow"
#username = "some@mail.com"
#avatar_url = "someUrl.com"
#action = "set"
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
output = ""

if action == "set":
    cmd_list = ["export '"+key+"'='"+value+"'"]
else:
    cmd_list = ["unset "+key]

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 22, "root", ".Sommer1", banner_timeout=200)

    for command in cmd_list:
        stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
        outlines = stdout.readlines()
        resp = ''.join(outlines)
        output = output + resp

    print(output)

    """
    activity
    """

    if action == "set":
        try:
            data["activity"].append(
                {"date": str(date.today()), "status": "successful", "action": f"Adding Environment Variable {key} = {value} ", "user": username, "avatar_url": avatar_url})
        except:
            data["activity"] = []
            data["activity"].append(
                {"date": str(date.today()), "status": "successful", "action": f"Adding Environment Variable {key} = {value} ", "user": username, "avatar_url": avatar_url})
    else:
        try:
            data["activity"].append(
                {"date": str(date.today()), "status": "successful", "action": f"Unsetting Environment Variable {key} = {value} ", "user": username, "avatar_url": avatar_url})
        except:
            data["activity"] = []
            data["activity"].append(
                {"date": str(date.today()), "status": "successful", "action": f"Unsetting Environment Variable {key} = {value} ", "user": username, "avatar_url": avatar_url})

except:
    if action == "set":
        try:
            data["activity"].append(
                {"date": str(date.today()), "status": "failed", "output": "==> Connection was closed unexpectedly \n==> Please try again in a few seconds", "action": f"Adding Environment Variable {key} = {value} ", "user": username, "avatar_url": avatar_url})
        except:
            data["activity"] = []
            data["activity"].append(
                {"date": str(date.today()), "status": "failed", "output": "==> Connection was closed unexpectedly \n==> Please try again in a few seconds", "action": f"Adding Environment Variable {key} = {value} ", "user": username, "avatar_url": avatar_url})
    else:
        try:
            data["activity"].append(
                {"date": str(date.today()), "status": "failed", "output": "==> Connection was closed unexpectedly \n==> Please try again in a few seconds", "action": f"Unsetting Environment Variable {key} = {value} ", "user": username, "avatar_url": avatar_url})
        except:
            data["activity"] = []
            data["activity"].append(
                {"date": str(date.today()), "status": "failed", "output": "==> Connection was closed unexpectedly \n==> Please try again in a few seconds", "action": f"Unsetting Environment Variable {key} = {value} ", "user": username, "avatar_url": avatar_url})


url = "http://192.168.0.21:8000/api/applications/"+application+"/data/"

payload = {
    "data": json.dumps(data)
}
headers = {
    'Authorization': 'token 228eb0c7b1c08682d3598b1f0d6fd1b4f9a4b474',
}

response = requests.request("POST", url, headers=headers, data=payload)
