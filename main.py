import os
import shutil
import requests
import datetime
import dateutil
from bs4 import BeautifulSoup
import json
import subprocess

from utils import APIConnector
from utils import create_file_name


# TODO add counters for number of images downloaded and deleted

def wait():
    input("Press enter to continue.")


# Downloads all data for a series
def download(series):
    # Create downloads folder
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    
    # Remove previously downloaded content for this series if it exists
    if os.path.exists(os.path.join("downloads", series.folder_name)):
        # BUG Sometimes this call will not remove the entire folder, causing crashes to occur with makedirs
        shutil.rmtree(os.path.join("downloads", series.folder_name), ignore_errors=True)

    # Create series folder
    os.makedirs(os.path.join("downloads", series.folder_name), exist_ok=True)

    api_con = APIConnector()

    # # Download series text data to info.json
    # api_path = "https://api.thetvdb.com/series/{}".format(series.id)
    # res = api_con.send_http_req(api_path)
    
    # info_path = os.path.join("downloads", series.folder_name, "info.json")

    # with open(info_path, 'wb') as f:
    #     f.write(res.content)
    
    # # Make a folder for actors
    # actors_folder_path = os.path.join("downloads", series.folder_name, "actors")
    # os.makedirs(actors_folder_path)

    # # Download actors to actors.json
    # api_path = "https://api.thetvdb.com/series/{}/actors".format(series.id)
    # res = api_con.send_http_req(api_path)

    # actors_path = os.path.join("downloads", series.folder_name, "actors", "actors.json")

    # with open(actors_path, 'wb') as f:
    #     f.write(res.content)

    # # Make folder for actor profile images
    # actors_profile_folder_path = os.path.join("downloads", series.folder_name, "actors", "profiles")
    # os.makedirs(actors_profile_folder_path)

    # # Download each actor's profile picture and save it as their name
    # for actor in json.loads(res.content)["data"]:
    #     name = create_file_name(actor["name"])
        
    #     # Check if there is an image for the actor
    #     if actor["image"] != "":
    #         print("downloading " + actor["image"])
    #         img_res = requests.get("https://www.thetvdb.com/banners/" + actor["image"])
    #         with open(os.path.join(actors_profile_folder_path, name + '_' + str(actor["id"]) + ".jpg"), 'wb') as f:
    #             f.write(img_res.content)
    #     else:
    #         # Use a default image if one does not exist on theTVDB.com
    #         shutil.copyfile(os.path.join("resources", "default_person.jpg"), os.path.join(actors_profile_folder_path, name + '_' + str(actor["id"]) + ".jpg"))

    # # Make a folder for episodes
    # episodes_folder_path = os.path.join("downloads", series.folder_name, "episodes")
    # os.makedirs(episodes_folder_path)


    # # Get number of seasons
    # api_path = "https://api.thetvdb.com/series/{}/episodes/summary".format(series.id)
    # res = api_con.send_http_req(api_path)
    # seasons = json.loads(res.content)["data"]["airedSeasons"]

    # # Create a folder for each season
    # for season in seasons:
    #     season_folder_path = os.path.join(episodes_folder_path, "Season " + season)
    #     os.makedirs(season_folder_path)

    # # Download episode info to episodes.json
    # api_path = "https://api.thetvdb.com/series/{}/episodes".format(series.id)
    # res = api_con.send_http_req(api_path)
    # with open(os.path.join(episodes_folder_path, "episodes.json"), 'wb') as f:
    #     f.write(res.content)

    # # Seperate episode data into individual json files for each episode and download episode thumbnails
    # for episode in json.loads(res.content)["data"]:
    #     episode_path = os.path.join(episodes_folder_path, "Season " + str(episode["airedSeason"]), "Episode {} - {}".format(str(episode["airedEpisodeNumber"]), episode["episodeName"]))
    #     img_res = requests.get("https://www.thetvdb.com/banners/" + episode["filename"])
    #     with open(episode_path + ".json", 'w') as f:
    #         f.write(json.dumps(episode))
    #     with open(episode_path + ".jpg", 'wb') as f:
    #         f.write(img_res.content)




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
