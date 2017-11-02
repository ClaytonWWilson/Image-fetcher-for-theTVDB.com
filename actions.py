import requests
import shutil
import json
import os

def refreshToken():
    print("Not implemented yet")

def clearLogin():
    try:
        os.remove("login.json")
    except Exception as e:
        pass

def clearFolders():# TODO implement this
    if os.path.exists("banner"):
        print("cleared")
    else:
        print("empty")

    if os.path.exists("fanart"):
        print("cleared")
    else:
        print("empty")

    if os.path.exists("poster"):
        print("cleared")
    else:
        print("empty")


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
