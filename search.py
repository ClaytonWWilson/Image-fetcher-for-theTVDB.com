import os.path
import json

import requests
import urllib.parse

from actions import wait



def searchRemainder(imageType, saveNameList, idNum):#Finds any images missing from the api call in getImages
    numbers = []
    print("Checking for missing images...")  # TODO implement this method
    if (imageType is "banner"):  # TODO check upper and lower bounds
        print("this is a banner")
        #TODO deal with banners
    else:
        for name in saveNameList:
            if (name.rfind("-") != -1):
                hyphenIndex = name.rfind("-")
                hyphenSuffix = name[hyphenIndex + 1:]
                value = hyphenSuffix.replace(".jpg", "")
                numbers.append(int(value))
            else:
                print("I couldn't find a hyphen in: %s" % name)#Error checking
        numbers.sort
        missingList = findMissing(numbers)
        minNum = min(numbers)
        maxNum = max(numbers)
        tryMissing(missingList, minNum, maxNum, idNum, imageType)

def findMissing(numbers):  # TODO test this
    start, end = numbers[0], numbers[-1]
    return sorted(set(range(start, end + 1)).difference(numbers))

def tryMissing(missingNums, min, max, idNum, imageType):
    if (imageType is "fanart"):
        startDirectory = "fanart/original/"
    elif (imageType is "poster"):
        startDirectory = "posters/"

    for num in missingNums:
        fileName = startDirectory + str(idNum) + "-" + str(num) + ".jpg"
        # fileName = "%s%s-%d.jpg" % startDirectory, idNum, missingNums[num]
        print("This is missing: " + fileName)
        try:
            print("Trying... " + fileName)
            dlUrl = "https://www.thetvdb.com/banners/" + fileName
            response = requests.get(dlUrl)
            if (checkStatus(response, False) == True):
                path = os.path.join(imageType + "\\" + str(idNum) + str(num) + ".jpg")
                obj = open(path, "wb")
                obj.write(response.content)
                obj.close()

        except Exception as e:
            print("repsonse code: " + str(response.status_code))
            print("Check: " + dlUrl)
            print(fileName + " doesn't exist")

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
                    print("Your token has expired. Get a new one by choosing Refresh Token.")
                    return None
    except:
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

    searchUrl = "https://api.thetvdb.com/search/series?name=" + sKeyword
    response = requests.get(searchUrl, headers=authHeaders)

    if (checkStatus(response, True) == False):
        return None

    searchResults = json.loads(response.content)

    title = -1
    print()
    while title < 0 or title > len(searchResults["data"]) - 1:  # Looping until the user chooses
        print("Results:")                                       # a series from the printed list
        count = 1                                               # or they input '0' to cancel
        for result in searchResults["data"]:
            print("\n%s)\nSeries Name: " % str(count), str(result["seriesName"]))
            print()
            desc = result["overview"]
            desc = str(desc).replace("\r\n\r\n", " ")  # Removing format characters
            print("Description: \n%s" % desc)
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

    downloadImages("fanart", fanart, idNum)  # TODO find a better way to pass these variables. Constructor?
    downloadImages("poster", poster, idNum)
    downloadImages("banner", banner, idNum)
    print("All downloads finished!")
    return None
