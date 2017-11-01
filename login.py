import json
import os.path
from checks import *
import datetime

def login():
    if os.path.exists("login.json") == False:
        obj = open("login.json")
        # obj.write()
        obj.close()

    if os.stat("login.json").st_size == 0:# Will only ask for credentials if the login file is empty
        login = {
        "API_KEY": "",
        "USER_KEY": "",
        "USER_NAME": "",
        "TOKEN": "",
        "TIMESTAMP": ""
        }

        tmp_api_key = login["API_KEY"]
        tmp_user_key = login["USER_KEY"]
        tmp_user_name = login["USER_NAME"]

        while tmp_api_key is "":
            tmp_api_key = input("Please enter your api key: ")
        while tmp_user_key is "":
            tmp_user_key = input("Please enter your user key: ")
        while tmp_user_name is "":
            tmp_user_name = input("Please enter your username: ")

        LOGIN_DATA = {
            "apikey": tmp_api_key,
            "userkey": tmp_user_key,
            "username": tmp_user_name
        }

        tmp_token = getToken(LOGIN_DATA)
        if tmp_token is "":
            print("Authentication failed. Please try again.")
        else:
            with open("login.json") as json_data:
                login["API_KEY"] = tmp_api_key
                login["USER_KEY"] = tmp_user_key
                login["USER_NAME"] = tmp_user_name
                login["TOKEN"] = tmp_token
                login["TIMESTAMP"] = datetime.datetime.now()
                obj = open("login.json", "w")
                obj.write(json.dumps(login))
                obj.close()
# TODO try to get token, if token fails, ask for login info again, if it passes save login details to login.py and save token with timestamp.
# TODO at startup, check token for validity and remove it if it is expired
