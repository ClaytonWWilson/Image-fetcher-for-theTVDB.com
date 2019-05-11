import json
import os
import re
import requests



class APIConnector:
    def __init__(self):
        with open("login.json", "r") as f:
            self.login = json.load(f)
            self.auth_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + self.login["TOKEN"]
            }

    def reload_login(self):
        with open("login.json", "r") as f:
            self.login = json.load(f)
            self.auth_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + self.login["TOKEN"]
            }

    def send_http_req(self, api_path):
        return requests.get(api_path, headers=self.auth_headers)

def clearFolders():  # TODO implement this
    folders = ["banner", "fanart", "poster"]
    del_count = 0
    for folder in folders:
        if os.path.exists(folder):
            image_list = os.listdir(folder)
            if len(image_list) != 0:
                print("Clearing " + folder + "/")
                for x in image_list:  # TODO check if folder is empty
                    print("Deleting {}/{}".format(folder, x))
                    del_path = os.path.join(folder + "\\" + x)
                    os.remove(del_path)
                    del_count += 1
                print()
            else:
                print("'{}' is already empty".format(folder))
        else:
            os.makedirs(folder)
    print("Deleted {} images.\n".format(del_count))

def clearScreen():
    IS_WINDOWS = os.name == "nt"
    if IS_WINDOWS:
        os.system("cls")
    else:
        os.system("clear")

# Clears out all illegal filename characters from the string
def create_file_name(string):
    string = string.strip()
    string = re.sub(r'(?u)[^-\w. ]', '', string)
    return string
