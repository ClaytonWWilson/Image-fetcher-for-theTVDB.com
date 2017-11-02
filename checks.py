import json
import requests
import datetime

def getToken(data):#TODO add a timeout and try catch to all requests
    url = "https://api.thetvdb.com/login"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
    except requests.exceptions.ConnectionError as e:
        print("An error occurred. Please check your internet and try again.")
        quit()

    if (checkStatus(response, True)):
        parsed_token = json.loads(response.content)
        token = parsed_token["token"]
        return token
    else:
        return ""

def checkStatus(response, v):
    if (response.status_code != 200):
        if (v == True):
            print("\nAn error occurred.")
            print("HTTP Code: " + str(response.status_code))
            error = json.loads(response.content)
            print("Response : " + error["Error"])
        return False
    else:
        return True

def checkTimestamp(saveTime, curTime):  # Returns true if the token is still valid
    if curTime - saveTime < datetime.timedelta(0, 86100, 0):
        return True
    else:
        return False
