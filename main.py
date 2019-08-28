import os
import shutil
import requests
import datetime
import dateutil
from bs4 import BeautifulSoup
import json
import subprocess
import sys

from utils import APIConnector
from utils import create_file_name
from utils import ProgressBar


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

    print("Downloading data for " + series.name)

    api_con = APIConnector()

    # Download series text data to info.json
    api_path = "https://api.thetvdb.com/series/{}".format(series.id)
    res = api_con.send_http_req(api_path)
    
    info_path = os.path.join("downloads", series.folder_name, "info.json")

    with open(info_path, 'wb') as f:
        f.write(res.content)
    


    # Make a folder for actors
    actors_folder_path = os.path.join("downloads", series.folder_name, "actors")
    os.makedirs(actors_folder_path)

    # Download actors to actors.json
    api_path = "https://api.thetvdb.com/series/{}/actors".format(series.id)
    res = api_con.send_http_req(api_path)

    actors_path = os.path.join("downloads", series.folder_name, "actors", "actors.json")

    with open(actors_path, 'wb') as f:
        f.write(res.content)

    # Make folder for actor profile images
    actors_profile_folder_path = os.path.join("downloads", series.folder_name, "actors", "profiles")
    os.makedirs(actors_profile_folder_path)

    # Count the number of actor profile pictures that will be downloaded
    amount = 0
    for actor in json.loads(res.content)["data"]:
        amount += 1

    # Create a progress bar
    progress_bar = ProgressBar(amount)

    # Download each actor's profile picture and save it as their name
    for actor in json.loads(res.content)["data"]:
        # Print progress bar to the screen
        sys.stdout.write("\rDownloading Actors...  {}  {}% {}".format(progress_bar.to_string(), progress_bar.get_percent(), str(actor["id"]) + ".jpg"))
        sys.stdout.flush()
        
        
        name = create_file_name(actor["name"])

        # Check if there is an image for the actor
        if actor["image"] != "":
            # print("downloading " + actor["image"])
            img_res = requests.get("https://www.thetvdb.com/banners/" + actor["image"])
            with open(os.path.join(actors_profile_folder_path, name + '_' + str(actor["id"]) + ".jpg"), 'wb') as f:
                f.write(img_res.content)
        else:
            # Use a default image if one does not exist on theTVDB.com
            shutil.copyfile(os.path.join("resources", "default_person.jpg"), os.path.join(actors_profile_folder_path, name + '_' + str(actor["id"]) + ".jpg"))
        
        progress_bar.increment()

    # Print that the operation is done
    sys.stdout.write("\rDownloading Actors...  {}  {}% {}".format(progress_bar.to_string(), progress_bar.get_percent(), "Done.                    "))
    sys.stdout.flush()
    print()



    # Make a folder for episodes
    episodes_folder_path = os.path.join("downloads", series.folder_name, "episodes")
    os.makedirs(episodes_folder_path)


    # Get number of seasons
    api_path = "https://api.thetvdb.com/series/{}/episodes/summary".format(series.id)
    res = api_con.send_http_req(api_path)
    seasons = json.loads(res.content)["data"]["airedSeasons"]

    # Create a folder for each season
    for season in seasons:
        season_folder_path = os.path.join(episodes_folder_path, "Season " + season)
        os.makedirs(season_folder_path)

    # Download episode info to episodes.json
    api_path = "https://api.thetvdb.com/series/{}/episodes".format(series.id)
    res = api_con.send_http_req(api_path)
    with open(os.path.join(episodes_folder_path, "episodes.json"), 'wb') as f:
        f.write(res.content)

    # Count the number of episode pictures and data that will be downloaded
    amount = 0
    for episode in json.loads(res.content)["data"]:
        amount += 1

    progress_bar = ProgressBar(amount * 2)

    # Seperate episode data into individual json files for each episode and download episode thumbnails
    for episode in json.loads(res.content)["data"]:
        episode_path = os.path.join(episodes_folder_path, "Season " + str(episode["airedSeason"]), "Episode {} - {}".format(str(episode["airedEpisodeNumber"]), episode["episodeName"]))
        img_res = requests.get("https://www.thetvdb.com/banners/" + episode["filename"])
        with open(episode_path + ".json", 'w') as f:
            # Update progress bar and display it in the terminal
            sys.stdout.write("\rDownloading Episodes...  {}  {}% {}".format(progress_bar.to_string(), progress_bar.get_percent(), "Episode {} - {}".format(str(episode["airedEpisodeNumber"]), episode["episodeName"] + ".json                    ")))
            sys.stdout.flush()
            f.write(json.dumps(episode))
            progress_bar.increment()
        with open(episode_path + ".jpg", 'wb') as f:
            # Update progress bar and display it in the terminal
            sys.stdout.write("\rDownloading Episodes...  {}  {}% {}".format(progress_bar.to_string(), progress_bar.get_percent(), "Episode {} - {}".format(str(episode["airedEpisodeNumber"]), episode["episodeName"] + ".jpg                    ")))
            sys.stdout.flush()
            f.write(img_res.content)
            progress_bar.increment()

    sys.stdout.write("\rDownloading Episodes...  {}  {}% {}".format(progress_bar.to_string(), progress_bar.get_percent(), "Done.                    "))    
    sys.stdout.flush()
    print()


    # Make a folder for images
    images_folder_path = os.path.join("downloads", series.folder_name, "images")
    os.makedirs(images_folder_path)

    # Make a folder for each image type
    banners_folder_path = os.path.join(images_folder_path, "banners")
    os.makedirs(banners_folder_path)
    fanart_folder_path = os.path.join(images_folder_path, "fanart")
    os.makedirs(fanart_folder_path)
    posters_folder_path = os.path.join(images_folder_path, "posters")
    os.makedirs(posters_folder_path)

    # The API doesn't like to send links to all of the images hosted on the website,
    # so the best option to get every images is to scrape the website directly

    # Download banners
    banners_page = requests.get("{}/artwork/banners".format(series.url))
    banners_soup = BeautifulSoup(banners_page.content, "html.parser")

    # Make a progress bar for the banners
    amount = 0
    for image in banners_soup.find_all("img", attrs={"class": "media-object img-responsive"}):
        amount += 1

    progress_bar = ProgressBar(amount)


    counter = 0
    for image in banners_soup.find_all("img", attrs={"class":"media-object img-responsive"}):
        sys.stdout.write("\rDownloading Banners...  {}  {}% {}".format(progress_bar.to_string(), progress_bar.get_percent(), "{:03d}.jpg".format(counter)))
        sys.stdout.flush()

        image_res = requests.get(image["src"])
        with open(os.path.join(banners_folder_path, "{:03d}.jpg".format(counter)), 'wb') as f:
            f.write(image_res.content)
        counter+=1
        progress_bar.increment()

    sys.stdout.write("\rDownloading Banners...  {}  {}% {}".format(progress_bar.to_string(), progress_bar.get_percent(), "Done.                    "))
    sys.stdout.flush()
    print()


    # Download fanart
    fanart_page = requests.get("{}/artwork/fanart".format(series.url))
    fanart_soup = BeautifulSoup(fanart_page.content, "html.parser")

    # Make a progress bar for the fanart
    amount = 0
    for image in fanart_soup.find_all("img", attrs={"class": "media-object img-responsive"}):
        amount += 1

    progress_bar = ProgressBar(amount)


    counter = 0
    for image in fanart_soup.find_all("img", attrs={"class":"media-object img-responsive"}):
        sys.stdout.write("\rDownloading Fanart...  {}  {}% {}".format(progress_bar.to_string(), progress_bar.get_percent(), "{:03d}.jpg".format(counter)))
        sys.stdout.flush()
        image_res = requests.get(image["src"])
        with open(os.path.join(fanart_folder_path, "{:03d}.jpg".format(counter)), 'wb') as f:
            f.write(image_res.content)
        counter+=1
        progress_bar.increment()
    
    sys.stdout.write("\rDownloading Fanart...  {}  {}% {}".format(progress_bar.to_string(), progress_bar.get_percent(), "Done.                    "))
    sys.stdout.flush()
    print()
    
    # Download posters
    posters_page = requests.get("{}/artwork/poster".format(series.url))
    posters_soup = BeautifulSoup(posters_page.content, "html.parser")

    # Make a progress bar for the posters
    amount = 0
    for image in posters_soup.find_all("img", attrs={"class": "media-object img-responsive"}):
        amount += 1

    progress_bar = ProgressBar(amount)

    counter = 0
    for image in posters_soup.find_all("img", attrs={"class":"media-object img-responsive"}):
        sys.stdout.write("\rDownloading Posters...  {}  {}% {}".format(progress_bar.to_string(), progress_bar.get_percent(), "{:03d}.jpg".format(counter)))
        sys.stdout.flush()
        image_res = requests.get(image["src"])
        with open(os.path.join(posters_folder_path, "{:03d}.jpg".format(counter)), 'wb') as f:
            f.write(image_res.content)
        counter+=1
        progress_bar.increment()

    sys.stdout.write("\rDownloading Posters...  {}  {}% {}".format(progress_bar.to_string(), progress_bar.get_percent(), "Done.                    "))
    sys.stdout.flush()
    print()

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
