import json
import os.path
import datetime
import requests
import dateutil.parser

from utils import clear_screen


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
    except KeyboardInterrupt:
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


def getToken(login_data): #TODO add a timeout and try catch to all requests
    url = "https://api.thetvdb.com/login"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    try:
        response = requests.post(url, data=json.dumps(login_data), headers=headers)
    except requests.exceptions.ConnectionError:
        print("An error occurred. Please check your internet and try again.")
        quit()

    if (checkStatus(response, False)):
        parsed_token = json.loads(response.content)
        token = parsed_token["token"]
        return token
    else:
        return ""

def refreshToken():
    if os.path.exists("login.json"):
        try:
            with open("login.json") as json_data:
                login = json.load(json_data)
                save_time = dateutil.parser.parse(login["TIMESTAMP"])
                cur_time = datetime.datetime.now().replace(tzinfo=None)  # TODO use UTC time?
                json_data.close()

                LOGIN_DATA = {
                    "apikey": login["API_KEY"],
                    "userkey": login["USER_KEY"],
                    "username": login["USER_NAME"]
                }

                if check_timestamp(save_time, cur_time):
                    while True:
                        print("Your current token is still valid. Are you sure you want to grab a different one?")
                        choice = input("(y/n) ")
                        if choice is "n":
                            break
                        elif choice is "y":
                            login["TOKEN"] = getToken(LOGIN_DATA)  # TODO find a better way to run this on both paths
                            login["TIMESTAMP"] = str(datetime.datetime.now().replace(tzinfo=None))
                            obj = open("login.json", "w")
                            obj.write(json.dumps(login))
                            obj.close()
                            print("\nNew token acquired!\n")
                            break
                        clear_screen()
                else:
                    login["TOKEN"] = getToken(LOGIN_DATA)
                    login["TIMESTAMP"] = str(datetime.datetime.now().replace(tzinfo=None))
                    obj = open("login.json", "w")
                    obj.write(json.dumps(login))
                    obj.close()
                    print("New token acquired!\n")
        except Exception:
            print("You need to log in first. Select Login/Change login.\n")  # TODO make a set of constants for error codes
    else:
        print("You need to log in first. Select Login/Change login.\n")

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

# Returns true if the token is still valid.
# Tokens expire after 24 hours
def check_timestamp(save_time, cur_time):
    if cur_time - save_time < datetime.timedelta(0, 86100, 0):
        return True
    else:
        return False
