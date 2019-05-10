import os.path
import json
import datetime

import dateutil
import re
import requests
import urllib.parse

from utils import clearFolders
from utils import clearScreen
from utils import create_file_name
from authentication import checkTimestamp
from authentication import checkStatus
from authentication import refreshToken

class Series:
    def __init__(self, folder_name, id, url):
        self.folder_name = folder_name
        self.id = str(id)
        self.url = url
    

def search():
    try:
        with open("login.json") as json_data:  # TODO add a check for a login that is damaged/modified
            login = json.load(json_data)
            json_data.close()
            if login["TIMESTAMP"] == "":
                print("There was an error checking your login. Try logging in again with 'Login/Change login'.")
                return None
            else:
                save_time = dateutil.parser.parse(login["TIMESTAMP"])
                cur_time = datetime.datetime.now().replace(tzinfo=None)  # TODO use UTC time?
                if checkTimestamp(save_time, cur_time) == False:
                    refreshToken()
    except Exception as ex:
        # print(ex)
        print("There was an error checking your login. Try logging in again with 'Login/Change login'.")
        return None

    # All login checks pass and search starts
    FAN_KEY_TYPE = "?keyType=fanart"  # These are used in the search strings
    POS_KEY_TYPE = "?keyType=poster"
    BAN_KEY_TYPE = "?keyType=series"

    authHeaders = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + login["TOKEN"]
    }

    keyword = input("Enter series name to search: ")  # Getting the search name and fixing
    s_keyword = urllib.parse.quote(keyword)      # the url parse mistakes

    s_keyword = s_keyword.replace("%21", "!")    # TODO find a better way of doing this
    s_keyword = s_keyword.replace("%2A", "*")
    s_keyword = s_keyword.replace("%28", "(")
    s_keyword = s_keyword.replace("%29", ")")
    s_keyword = s_keyword.replace("%27", "'")
    s_keyword = s_keyword.replace("/", "%2F")
    s_keyword = s_keyword.replace("%7E", "~")

    search_url = "https://api.thetvdb.com/search/series?name={}".format(s_keyword)
    response = requests.get(search_url, headers=authHeaders)

    if (checkStatus(response, True) == False):
        return None

    search_results = json.loads(response.content)

    title = -1
    print()
    clearScreen()
    while title < 0 or title > len(search_results["data"]) - 1:  # Looping until the user chooses
        print("Results:")                                        # a series from the printed list
        count = 1                                                # or they input '0' to cancel
        for result in search_results["data"]:
            print("\n{})\nSeries Name: {}".format(str(count), str(result["seriesName"])))
            print()
            desc = result["overview"]
            desc = str(desc).replace("\r\n\r\n", " ")  # Removing format characters
            print("Description: \n{}".format(desc))
            print()
            count = count + 1
        print()
        #TODO this can crash with non integer inputs
        #TODO they should also be able to ctrl-c to cancel search
        title = int(input("Choose one by number or '0' to exit: ")) - 1  # Subtracting 1 so that the
        print()                                                          # index can start from 0
        if title < -1 or title > len(search_results["data"]) - 1:
            print("Error: Choose the number of an item listed. Or '0' to exit.")

        if (title == -1):  # If the user inputs 0
            return None

        print()

    series = Series(create_file_name(search_results["data"][title]["seriesName"]), search_results["data"][title]["id"], "https://www.thetvdb.com/series/" + search_results["data"][title]["slug"])
    return series

    # id_num = search_results["data"][title]["id"]               # Setting up the request urls
    # fanart = searchImages(id_num, FAN_KEY_TYPE, authHeaders)   # for banners, fanart, and posters
    # poster = searchImages(id_num, POS_KEY_TYPE, authHeaders)
    # banner = searchImages(id_num, BAN_KEY_TYPE, authHeaders)

    # clearFolders()
    # downloadImages("fanart", fanart, id_num)  # TODO find a better way to pass these variables. Constructor?
    # downloadImages("poster", poster, id_num)
    # downloadImages("banner", banner, id_num)
    # print("\nAll downloads finished!\n")
    # return None
