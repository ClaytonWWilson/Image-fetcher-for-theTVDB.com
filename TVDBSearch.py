import requests
import json
import urllib.parse
import os.path
import shutil
# import login

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

def searchRemainder(imageType, saveNameList, idNum):#Finds any images missing from the api call in getImages
    numbers = []
    print("Checking for missing images...")#TODO implement this method
    if (imageType is "banner"):
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
    # print("min: %d" % int(min(numbers)))
    # print("max: %d" % int(max(numbers)))
    # quit()

def findMissing(numbers):#TODO test this
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

# TODO load login data here

FAN_KEY_TYPE = "?keyType=fanart"# TODO check upper and lower bounds
POS_KEY_TYPE = "?keyType=poster"
BAN_KEY_TYPE = "?keyType=series"

token = getToken(url, data, headers)# TODO uppercase these


authHeaders = {# TODO uppercase this
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer " + token
}


#search
keyword = input("Enter series to search: ")

sKeyword = urllib.parse.quote(keyword)

#fixing things that urllib.parse missed, there is probably a better way to do this
sKeyword = sKeyword.replace("%21", "!")
sKeyword = sKeyword.replace("%2A", "*")
sKeyword = sKeyword.replace("%28", "(")
sKeyword = sKeyword.replace("%29", ")")
sKeyword = sKeyword.replace("%27", "'")
sKeyword = sKeyword.replace("/", "%2F")
sKeyword = sKeyword.replace("%7E", "~")


searchUrl = "https://api.thetvdb.com/search/series?name=" + sKeyword#TODO put this in a function

response = requests.get(searchUrl, headers=authHeaders)

if (checkStatus(response, True) == False):
    quit()

searchResults = json.loads(response.content)
title = -1
print()
while title < 0 or title > len(searchResults["data"]) - 1:
    print("Results:")
    count = 1
    for result in searchResults["data"]:
        print("\n%s)\nSeries Name: " % str(count), str(result["seriesName"]))
        print()
        desc = result["overview"]
        desc = str(desc).replace("\r\n\r\n", " ")
        print("Description: \n%s" % desc)
        print()
        count = count + 1
    print()
    title = int(input("Choose one by number or '0' to exit: ")) - 1
    print()
    if title < -1 or title > len(searchResults["data"]) - 1:
        print("Error: Choose the number of an item listed. Or '0' to exit.")

    if (title == -1):
        quit()

    print()
idNum = searchResults["data"][title]["id"]

fanart = getImages(idNum, FAN_KEY_TYPE, authHeaders)

poster = getImages(idNum, POS_KEY_TYPE, authHeaders)

banner = getImages(idNum, BAN_KEY_TYPE, authHeaders)


downloadImages("fanart", fanart, idNum)#TODO find a better way to pass this variable

downloadImages("poster", poster, idNum)

downloadImages("banner", banner, idNum)
