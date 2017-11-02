import requests
import shutil
import json
import datetime
import dateutil
import os
from checks import checkTimestamp

def refreshToken():
    print("Not implemented yet")
    if os.path.exists("login.json"):
        try:
            with open("login.json") as json_data:
                login = json.load(json_data)
                saveTime = dateutil.parser.parse(login["TIMESTAMP"])
                curTime = datetime.datetime.now().replace(tzinfo=None)# TODO use UTC time?
                json_data.close()
                if checkTimestamp(saveTime, curTime):
                    While True:
                        print("The current token is still valid. Do you still want to grab a different one")
                        choice = input("(y/n) ")
                        if choice is "n":
                            break
                        elif choice is "y":
                            token = getToken() # TODO finish setting this up. Make it occur if the if statement above fails
        except Exception as e:
            print("You need to log in first. Select Login/Change login.\n")  # TODO make a set of constants for error codes
    else:
        print("You need to log in first. Select Login/Change login.\n")

def clearLogin():
    try:
        os.remove("login.json")
    except Exception as e:
        pass

def clearFolders():# TODO implement this
    folders = ["banner", "fanart", "poster"]
    for folder in folders:
        if os.path.exists(folder):
            imageList = os.listdir(folder)
            if len(imageList) != 0:
                for x in imageList: # TODO check if folder is empty
                    print("Deleting " + x)
                    delPath = os.path.join(folder + "\\" + x)
                    os.remove(delPath)
                print(folder + " cleared\n")
            else:
                print(folder + " is already empty")
        else:
            createFolder(folder)
    print("")

def createFolder(folder):
    os.makedirs(folder)


def getImages(idNum, keyType, authHeaders):
    imageUrl = "https://api.thetvdb.com/series/" + str(idNum) + "/images/query" + keyType
    response = requests.get(imageUrl, headers=authHeaders)
    if (checkStatus(response, True)):
        return response
    else:
        quit()

def downloadImages(imageType, respObj, idNum):# TODO some images arent grabbed through the api. save the image number and make a try catch to get any missing images
    if (os.path.exists(imageType)):#TODO add try catch here
        print("\nClearing /%s/" % imageType)
        shutil.rmtree(imageType)
    os.makedirs(imageType)

    parsed_respObj = json.loads(respObj.content)

    saveNameList = download(imageType, parsed_respObj)

    searchRemainder(imageType, saveNameList, idNum)

def download(imageType, parsed_respObj):
    counter = 0
    saveNameList = []
    for imageObj in parsed_respObj["data"]:
        fileName = parsed_respObj["data"][counter]["fileName"]#TODO the download method should start here, move everything else up to downloadImages
        counter = counter + 1

        slashIndex = fileName.rfind("/")
        saveName = fileName[slashIndex + 1:]

        saveNameList.append(saveName)

        print("Downloading... " + fileName)
        dlUrl = "https://www.thetvdb.com/banners/" + fileName
        response = requests.get(dlUrl)# TODO getting errors when checking 'new game'. Check to see if those images actually exist

        if (checkStatus(response, True)):
            path = os.path.join(imageType + "\\", saveName)
            obj = open(path, "wb")
            obj.write(response.content)
            obj.close()
        else:
            quit()
    return saveNameList
