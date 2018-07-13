import os.path
import json
import datetime

import requests
import urllib.parse
import dateutil

from actions import clearFolders
from actions import clear_screen
from actions import downloadImages
from actions import refreshToken
from actions import searchImages
from checks import checkTimestamp
from checks import checkStatus


def search():
    try:
        with open("login.json") as json_data:  # TODO add a check for a login that is damaged/modified
            login = json.load(json_data)
            json_data.close()
            if login["TIMESTAMP"] == "":
                print("There was an error checking your login. Try logging in again with 'Login/Change login'.")
                return None
            else:
                saveTime = dateutil.parser.parse(login["TIMESTAMP"])
                curTime = datetime.datetime.now().replace(tzinfo=None)  # TODO use UTC time?
                if checkTimestamp(saveTime, curTime) == False:
                    refreshToken()
    except Exception as ex:
        print(ex)
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

    keyword = input("Enter series to search: ")  # Getting the search name and fixing
    sKeyword = urllib.parse.quote(keyword)       # the url parse mistakes

    sKeyword = sKeyword.replace("%21", "!")      # TODO find a better way of doing this
    sKeyword = sKeyword.replace("%2A", "*")
    sKeyword = sKeyword.replace("%28", "(")
    sKeyword = sKeyword.replace("%29", ")")
    sKeyword = sKeyword.replace("%27", "'")
    sKeyword = sKeyword.replace("/", "%2F")
    sKeyword = sKeyword.replace("%7E", "~")

    searchUrl = "https://api.thetvdb.com/search/series?name={}".format(sKeyword)
    response = requests.get(searchUrl, headers=authHeaders)

    if (checkStatus(response, True) == False):
        return None

    searchResults = json.loads(response.content)

    title = -1
    print()
    clear_screen()
    while title < 0 or title > len(searchResults["data"]) - 1:  # Looping until the user chooses
        print("Results:")                                       # a series from the printed list
        count = 1                                               # or they input '0' to cancel
        for result in searchResults["data"]:
            print("\n{})\nSeries Name: {}".format(str(count), str(result["seriesName"])))
            print()
            desc = result["overview"]
            desc = str(desc).replace("\r\n\r\n", " ")  # Removing format characters
            print("Description: \n{}".format(desc))
            print()
            count = count + 1
        print()
        title = int(input("Choose one by number or '0' to exit: ")) - 1  # Subtracting 1 so that the
        print()                                                          # index can start from 0
        if title < -1 or title > len(searchResults["data"]) - 1:
            print("Error: Choose the number of an item listed. Or '0' to exit.")

        if (title == -1):  # If the user inputs 0
            return None

        print()

    idNum = searchResults["data"][title]["id"]               # Setting up the request urls
    fanart = searchImages(idNum, FAN_KEY_TYPE, authHeaders)  # for banners, fanart, and posters
    poster = searchImages(idNum, POS_KEY_TYPE, authHeaders)
    banner = searchImages(idNum, BAN_KEY_TYPE, authHeaders)

    clearFolders()
    downloadImages("fanart", fanart, idNum)  # TODO find a better way to pass these variables. Constructor?
    downloadImages("poster", poster, idNum)
    downloadImages("banner", banner, idNum)
    print("\nAll downloads finished!\n")
    return None
