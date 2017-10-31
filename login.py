import json
import os.path
import checks

def login():
    if (os.path.exists("login.json") == False):
        obj = open("login.json")
        # obj.write()
        obj.close()

    login = {
    "API_KEY": "",
    "USER_KEY": "",
    "USER_NAME": "",
    "TOKEN": "",
    "TIMESTAMP": ""
    }

    with open("login.json") as json_data:
        # login = json.load(json_data)

        tmp_api_key = login["API_KEY"]
        tmp_user_key = login["USER_KEY"]
        tmp_user_name = login["USER_NAME"]

        while tmp_api_key is "":
            tmp_api_key = input("Please enter your api key: ")
        while tmp_user_key is "":
            tmp_user_key = input("Please enter your user key: ")
        while tmp_user_name is "":
            tmp_user_name = input("Please enter your username: ")

        # TODO check token here
    login["API_KEY"] = tmp_api_key
    login["USER_KEY"] = tmp_user_key
    login["USER_NAME"] = tmp_user_name
    obj = open("login.json", "w")
    obj.write(json.dumps(login))
    obj.close()


# TODO try to get token, if token fails, ask for login info again, if it passes save login details to login.py and save token with timestamp.
# TODO at startup, check token for validity and remove it if it is expired
