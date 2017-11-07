import os
import subprocess
import shutil
import json
import datetime

import requests
import dateutil

from checks import checkTimestamp
from checks import checkStatus
from checks import getToken

def wait():
    input("Press enter to continue.")

def clear_screen():
    IS_WINDOWS = os.name == "nt"
    if IS_WINDOWS:
        os.system("cls")
    else:
        os.system("clear")

def refreshToken():
    if os.path.exists("login.json"):
        try:
            with open("login.json") as json_data:
                login = json.load(json_data)
                saveTime = dateutil.parser.parse(login["TIMESTAMP"])
                curTime = datetime.datetime.now().replace(tzinfo=None)  # TODO use UTC time?
                json_data.close()

                LOGIN_DATA = {
                    "apikey": login["API_KEY"],
                    "userkey": login["USER_KEY"],
                    "username": login["USER_NAME"]
                }

                if checkTimestamp(saveTime, curTime):
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
        except Exception as e:
            print("You need to log in first. Select Login/Change login.\n")  # TODO make a set of constants for error codes
    else:
        print("You need to log in first. Select Login/Change login.\n")

def clearLogin():
    try:
        os.remove("login.json")
    except Exception as e:
        pass

def clearFolders():  # TODO implement this
    folders = ["banner", "fanart", "poster"]
    for folder in folders:
        if os.path.exists(folder):
            imageList = os.listdir(folder)
            if len(imageList) != 0:
                for x in imageList:  # TODO check if folder is empty
                    print("Deleting " + x)
                    delPath = os.path.join(folder + "\\" + x)
                    os.remove(delPath)
                print(folder + " cleared\n")
            else:
                print("'" + folder + "'" + " is already empty")
        else:
            createFolder(folder)
    print("")

def createFolder(folder):
    os.makedirs(folder)


def searchImages(idNum, keyType, authHeaders):  # This is getting a list of file info for images in json format
    queryUrl = "https://api.thetvdb.com/series/" + str(idNum) + "/images/query" + keyType
    response = requests.get(queryUrl, headers=authHeaders)
    if (checkStatus(response, True)):
        return response
    else:
        quit()

def downloadImages(imageType, respObj, idNum):  # TODO some images arent grabbed through the api. save the image number and make a try catch to get any missing images
    parsed_respObj = json.loads(respObj.content)

    saveNameList = download(imageType, parsed_respObj)

    searchRemainder(imageType, saveNameList, idNum)

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

def download(imageType, parsed_respObj):
    counter = 0
    saveNameList = []
    for imageObj in parsed_respObj["data"]:
        fileName = parsed_respObj["data"][counter]["fileName"]  # TODO the download method should start here, move everything else up to downloadImages
        counter = counter + 1

        slashIndex = fileName.rfind("/")  # This is used to slice the url at the beginning of the filename
        saveName = fileName[slashIndex + 1:]  # For example 'https://thetvdb.com/banners/fanart/original/32451-3.jpg' --> '32451.jpg'
        saveNameList.append(saveName)

        print("Downloading... " + fileName)
        dlUrl = "https://www.thetvdb.com/banners/" + fileName
        response = requests.get(dlUrl)  # TODO getting errors when checking 'new game'. Check to see if those images actually exist

        if (checkStatus(response, True)):
            path = os.path.join(imageType + "\\", saveName)
            obj = open(path, "wb")
            obj.write(response.content)
            obj.close()
        else:
            quit()
    return saveNameList

  # The following code is from Red-DiscordBot
  # https://github.com/Cog-Creators/Red-DiscordBot
def is_git_installed():
    try:
        subprocess.call(["git", "--version"], stdout=subprocess.DEVNULL,
                                                stdin =subprocess.DEVNULL,
                                                stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        return False
    else:
        return True

def update():
    try:
        code = subprocess.call(("git", "pull", "--ff-only"))
    except FileNotFoundError:
        print("\nError: Git not found. It's either not installed or you did "
              "not clone this using git. Install instructions are on the GitHub: "
              "https://github.com/ClaytonWWilson/Image-fetcher-for-theTVDB.com")
        return
    if code == 0:
        print("\nThe program has been updated.\n")
    else:
        print("\nThere was an error while updating. This may be caused by edits "
              "you have made to the code.")
