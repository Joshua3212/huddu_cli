import requests
import json
import calendar
from datetime import datetime
from access import *
# needs a space
ADMIN_TOKEN = " ed8e22f70e8e83cee82c8aafe3c5910cccfebd67"
HOST = "http://127.0.0.1:8000"
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

    # django backend application
    for i in response.json()["data"]:
        name = i["name"]
        vmid = i['vmid']

        url = HOST + '/api/applications/detail/' + name + '/'
        headers = {
            'Authorization': "Token" + ADMIN_TOKEN,
        }
        response = requests.request("GET", url, headers=headers)

        # get duedate for every application
        if response.status_code == 200:
            response = response.json()
            duedate_str = response['duedate']
            duedate = datetime.strptime(
                duedate_str, '%Y-%m-%d %H:%M:%S')
            price = response['price']
            user = response['user']
            date = datetime.today()

            if duedate <= date:
                # get current amount
                url = HOST + '/api/payment/amount/' + str(user) + '/'
                old_amount = requests.request(
                    "GET", url, headers=headers, data=payload).json()['amount']

                # shut down vm if required

                if 2 * int(old_amount) - int(price) <= 0:
                    # name = application id
                    ticket = get_access_token(ip)
                    csrf_token = get_csrf_token(ip)
                    url = ip + "/api2/json/nodes/"+node+"/qemu/"+vmid+"/status/stop"
                    headers = {
                        'CSRFPreventionToken': csrf_token,
                    }
                    cookies = {
                        'PVEAuthCookie': ticket
                    }

                    requests.request(
                        "POST", url, headers=headers, data=payload, cookies=cookies, verify=False).json()

                # change amount
                headers = {
                    'Authorization': 'Token' + ADMIN_TOKEN
                }
                payload = {
                    'amount': int(old_amount) - int(price)
                }
                url = HOST + '/api/payment/amount/' + str(user) + '/'
                response = requests.request(
                    "POST", url, headers=headers, data=payload)
                # update duedate => date + 1month
                # date + one month
                currentdate = datetime.today()
                month = currentdate.month - 1 + 1
                year = currentdate.year + month // 12
                month = month % 12 + 1
                day = min(currentdate.day,
                          calendar.monthrange(year, month)[1])
                # min sec and hour stay equal
                next_month = datetime(
                    year, month, day, currentdate.hour, currentdate.minute, currentdate.second)
                url = HOST + '/api/applications/duedate/' + name + '/'
                headers = {
                    'Authorization': "Token" + ADMIN_TOKEN,
                }
                payload = {
                    'duedate': next_month
                }
                response = requests.request(
                    "POST", url, data=payload, headers=headers)


for node in getNodes():
    node = node
    application = getApplications(node=node)
