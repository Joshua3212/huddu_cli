import requests
import json
from datetime import datetime, timedelta
from access import *
# needs a space
ADMIN_TOKEN = " ed8e22f70e8e83cee82c8aafe3c5910cccfebd67"
HOST = "http://192.168.0.21:8000"
ip = "https://192.168.0.11:8006"


def getNodes():
    ticket = get_access_token(ip)
    csrf_token = get_csrf_token(ip)
    url = ip + "/api2/json/nodes/"

    payload = {
    }

    headers = {
        'CSRFPreventionToken': csrf_token,
    }
    cookies = {
        'PVEAuthCookie': ticket
    }

    response = requests.request(
        "GET", url, headers=headers, params=payload, cookies=cookies, verify=False).json()

    result = []
    for i in response['data']:
        result.append(i['node'])

    return result


def getApplications(node):
    ticket = get_access_token(ip)
    csrf_token = get_csrf_token(ip)
    url = ip + "/api2/json/nodes/"+node+"/qemu/"
    payload = {
    }
    headers = {
        'CSRFPreventionToken': csrf_token,
    }
    cookies = {
        'PVEAuthCookie': ticket
    }
    response = requests.request(
        "GET", url, headers=headers, params=payload, cookies=cookies, verify=False)

    return response


def getCurrentStatus(vmid, node):

    ticket = get_access_token(ip)
    csrf_token = get_csrf_token(ip)
    url = ip + "/api2/json/nodes/" + node + "/qemu/" + vmid + '/status/current/'

    payload = {

    }

    headers = {
        'CSRFPreventionToken': csrf_token,
    }
    cookies = {
        'PVEAuthCookie': ticket
    }

    response = requests.request(
        "GET", url, headers=headers, data=payload, cookies=cookies, verify=False).json()
    return response['data']['status']


def setStatus(vmid, name):
    """
    Get all the application Graphs
    """
    url = HOST + "/api/graph/detail/" + name + "/"
    headers = {
        'Authorization': "Token" + ADMIN_TOKEN
    }
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        response = response.json()
        old_data = response['data']
        old_data = eval(old_data)
        status = getCurrentStatus(vmid=vmid, node=node)
        if status == "running":
            status_code = 1
        else:
            status_code = 0
        """
        7 days a week => data[0] - data[6]
        """
        day7 = str(datetime.today().date() - timedelta(days=6))
        day6 = str(datetime.today().date() - timedelta(days=5))
        day5 = str(datetime.today().date() - timedelta(days=4))
        day4 = str(datetime.today().date() - timedelta(days=3))
        day3 = str(datetime.today().date() - timedelta(days=2))
        day2 = str(datetime.today().date() - timedelta(days=1))
        day1 = str(datetime.today().date())
        new_data = [
            {"name":  day7, "pv": old_data[1]["pv"]},
            {"name":  day6, "pv": old_data[2]["pv"]},
            {"name":  day5, "pv": old_data[3]["pv"]},
            {"name":  day4, "pv": old_data[4]["pv"]},
            {"name":  day3, "pv": old_data[5]["pv"]},
            {"name":  day2, "pv": old_data[6]["pv"]},
            {"name":  day1, "pv": status_code}
        ]

        url = HOST + "/api/graph/detail/" + name + "/"
        headers = {
            'Authorization': "Token" + ADMIN_TOKEN
        }
        payload = {
            "data": json.dumps(new_data),
            "uuid": name
        }
        response = requests.request(
            "POST", url, data=payload, headers=headers)


for node in getNodes():
    node = node
    application = getApplications(node=node)
    for i in application.json()["data"]:
        name = i["name"]
        vmid = i["vmid"]
        setStatus(vmid=vmid, name=name)
