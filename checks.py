import json
import requests

def getToken(data):#TODO add a timeout and try catch to all requests
    url = "https://api.thetvdb.com/login"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    if (checkStatus(response, True)):
        parsed_token = json.loads(response.content)
        token = parsed_token["token"]
        return token
    else:
        return ""

def checkStatus(response, v):
    if (response.status_code != 200):
        if (v == True):
            print("An error occurred.")
            print("HTTP Code: " + str(response.status_code))
            print("Response : " + str(response.content))
        return False
    else:
        return True
