import json
import os.path
import datetime

import dateutil.parser


def login():
    if os.path.exists("login.json") == False:
        obj = open("login.json", "w")
        obj.write("")
        obj.close()

    login = {
    "API_KEY": "",
    "USER_KEY": "",
    "USER_NAME": "",
    "TOKEN": "",
    "TIMESTAMP": ""
    }

    tmp_api_key = ""
    tmp_user_key = ""
    tmp_user_name = ""

    print("Please enter your Username, Unique ID, and API Key.\n"
          "You can find all of this information while logged in at:\n"
          "https://www.thetvdb.com/member/api\n"
          "Press CTRL+C to cancel.\n")

    try:
        while tmp_user_name is "":
            tmp_user_name = input("Enter your Username: ")
        while tmp_user_key is "":
            tmp_user_key = input("Enter your Unique ID: ")
        while tmp_api_key is "":
            tmp_api_key = input("Enter your API Key: ")
    except KeyboardInterrupt as e:
        print("\n")
        return

    LOGIN_DATA = {
        "apikey": tmp_api_key,
        "userkey": tmp_user_key,
        "username": tmp_user_name
    }

    tmp_token = getToken(LOGIN_DATA)

    if tmp_token is "":
        print("\nAuthentication failed. Please try again.")
    else:
        login["API_KEY"] = tmp_api_key
        login["USER_KEY"] = tmp_user_key
        login["USER_NAME"] = tmp_user_name
        login["TOKEN"] = tmp_token
        login["TIMESTAMP"] = str(datetime.datetime.now().replace(tzinfo=None))
        obj = open("login.json", "w")
        obj.write(json.dumps(login))
        obj.close()
        print("\nLogin successful!\n")

# TODO at startup, check token for validity and remove it if it is expired


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

    if (checkStatus(response, False)):
        parsed_token = json.loads(response.content)
        token = parsed_token["token"]
        return token
    else:
        return ""

def checkStatus(response, v):
    if (response.status_code != 200):
        if (v == True):
            print("\nAn error occurred.")
            print("HTTP Code: {}".format(str(response.status_code)))
            # error = json.loads(response.content)  # TODO move this somewhere else
            # print("Response : " + error["Error"])
        return False
    else:
        return True

# Returns true if the token is still valid
def checkTimestamp(save_time, cur_time):
    if cur_time - save_time < datetime.timedelta(0, 86100, 0):
        return True
    else:
        return False
