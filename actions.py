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

# TODO add counters for number of images downloaded and deleted

def wait():
    input("Press enter to continue.")

def clearScreen():
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
                save_time = dateutil.parser.parse(login["TIMESTAMP"])
                cur_time = datetime.datetime.now().replace(tzinfo=None)  # TODO use UTC time?
                json_data.close()

                LOGIN_DATA = {
                    "apikey": login["API_KEY"],
                    "userkey": login["USER_KEY"],
                    "username": login["USER_NAME"]
                }

                if checkTimestamp(save_time, cur_time):
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
                        clearScreen()
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

def download(series):
    # Create downloads folder
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    
    # Remove previously downloaded content for this series if it exists
    if os.path.exists(os.path.join("downloads", series.folder_name)):
        shutil.rmtree(os.path.join("downloads", series.folder_name))

    # Create series folder
    os.makedirs(os.path.join("downloads", series.folder_name))

    api_path = "https://api.thetvdb.com/series/" + series.id

    api_con = APIConnector()
    res = api_con.send_http_req(api_path)

    with open("out.json", "w") as out:
        out.write(json.dumps(json.loads(res.content)))


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
            createFolder(folder)
    print("Deleted {} images.\n".format(del_count))

def createFolder(folder):  # TODO remove this
    os.makedirs(folder)


def searchImages(id_num, keyType, authHeaders):  # This is getting a list of file info for images in json format
    query_url = "https://api.thetvdb.com/series/{}/images/query{}".format(str(id_num), keyType)
    response = requests.get(query_url, headers=authHeaders)
    if (checkStatus(response, True)):
        return response
    else:
        quit()

def downloadImages(image_type, respObj, id_num):  # TODO some images arent grabbed through the api. save the image number and make a try catch to get any missing images
    parse_resp_obj = json.loads(respObj.content)

    save_name_list = download(image_type, parse_resp_obj)

    searchRemainder(image_type, save_name_list, id_num)

def searchRemainder(image_type, save_name_list, id_num):#Finds any images missing from the api call in getImages
    numbers = []
    print("Checking for missing images...")  # TODO implement this method
    if (image_type is "banner"):  # TODO check upper and lower bounds
        print("this is a banner")
        #TODO deal with banners
    else:
        for name in save_name_list:
            if (name.rfind("-") != -1):
                hyphen_index = name.rfind("-")
                hyphen_suffix = name[hyphen_index + 1:]
                file_num = hyphen_suffix.replace(".jpg", "")
                numbers.append(int(file_num))
            else:
                print("I couldn't find a hyphen in: {}".format(name))  # Error checking
        numbers.sort
        missing_list = findMissing(numbers)
        min_num = min(numbers)
        max_num = max(numbers)

        tryMissing(missing_list, min_num, max_num, id_num, image_type)

def findMissing(numbers):
    start, end = numbers[0], numbers[-1]
    return sorted(set(range(start, end + 1)).difference(numbers))

def tryMissing(missing_nums, min_num, max_num, id_num, image_type):
    if (image_type is "fanart"):
        start_directory = "fanart/original/"
    elif (image_type is "poster"):
        start_directory = "posters/"

    for num in missing_nums:
        filename = "{}{}-{}.jpg".format(start_directory, str(id_num), str(num))
        # filename = "%s%s-%d.jpg" % start_directory, id_num, missing_nums[num]
        # try:
        print("Trying... {}".format(filename))
        dl_url = "https://www.thetvdb.com/banners/{}".format(filename)
        # print("url is: " + dl_url)
        response = requests.get(dl_url)
        # print(response.status_code)
        if (checkStatus(response, True) == True):  # TODO there is an error occurring here when checking fanart
            path = os.path.join("{}\\{}-{}.jpg".format(image_type, str(id_num), str(num)))
            obj = open(path, "wb")
            obj.write(response.content)
            obj.close()
            print("Image found\n")
        else:
            print("Image not found\n")
            # print(response.status_code)

        # except Exception as e:
        #     print("response code: " + str(response.status_code))
        #     print("Check: " + dl_url)
        #     print(e)

    # while min_num > 1:  # Checking lower bounds
    #     print("check lower")

# def download(image_type, parse_resp_obj):
#     counter = 0
#     save_name_list = []
#     for image_obj in parse_resp_obj["data"]:
#         filename = parse_resp_obj["data"][counter]["filename"]  # TODO the download method should start here, move everything else up to downloadImages
#         counter = counter + 1

#         slash_index = filename.rfind("/")  # This is used to slice the url at the beginning of the filename
#         save_name = filename[slash_index + 1:]  # For example 'https://thetvdb.com/banners/fanart/original/32451-3.jpg' --> '32451.jpg'
#         save_name_list.append(save_name)

#         print("Downloading... {}".format(filename))
#         dl_url = "https://www.thetvdb.com/banners/{}".format(filename)
#         response = requests.get(dl_url)  # TODO getting errors when checking 'new game'. Check to see if those images actually exist

#         if (checkStatus(response, True)):
#             path = os.path.join(image_type + "\\", save_name)
#             obj = open(path, "wb")
#             obj.write(response.content)
#             obj.close()
#         else:
#             quit()
#     return save_name_list

def installReqs():
    if is_pip_installed() == True:
        with open("requirements.txt") as f:
            reqs = f.readlines()
            reqs = [x.strip() for x in reqs]

        for module in reqs:
            print("Installing {}... ".format(module))
            subprocess.call(["pip", "install", module], stdout=subprocess.DEVNULL,
                                                stdin =subprocess.DEVNULL,
                                                stderr=subprocess.DEVNULL)
        print("Done!\n")
    else:
        print("You need to install pip.")

def is_pip_installed():
    try:
        subprocess.call(["pip", "--version"], stdout=subprocess.DEVNULL,
                                                stdin =subprocess.DEVNULL,
                                                stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        return False
    else:
        return True

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
              "https://github.com/ClaytonWWilson/Scraper-for-theTVDB.com")
        return
    if code == 0:
        print("\nUpdating complete.\n")
    else:
        print("\nThere was an error while updating. This may be caused by edits "
              "you have made to the code.")
