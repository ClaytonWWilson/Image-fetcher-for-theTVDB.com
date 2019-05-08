import json
import os.path
import datetime

import dateutil.parser

from actions import refreshToken
from checks import checkTimestamp
from checks import getToken

class APIConnector:
    def __init__(self):
        with open("login.json", "r") as f:
            self.login = json.loads(f)
            self.auth_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + login["TOKEN"]
            }

    def reload_login(self):
        with open("login.json", "r") as f:
            self.login = json.loads(f)
            self.auth_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + login["TOKEN"]
            }

    def send_http_req(api_path):
        return requests.get(api_path, headers=self.auth_headers)


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
