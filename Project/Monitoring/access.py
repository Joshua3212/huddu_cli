import requests
requests.packages.urllib3.disable_warnings()


def get_access_token(ip):
    url = ip + "/api2/json/access/ticket?password=.Sommer1&username=root@pam"

    payload = {}
    headers = {}

    response = requests.request(
        "POST", url, headers=headers, data=payload, verify=False).json()

    return response['data']['ticket']


def get_csrf_token(ip):
    url = ip + "/api2/json/access/ticket?password=.Sommer1&username=root@pam"

    payload = {}
    headers = {}

    response = requests.request(
        "POST", url, headers=headers, data=payload, verify=False).json()

    return response['data']['CSRFPreventionToken']
