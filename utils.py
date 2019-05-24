import json
import os
import re
import requests
import shutil



class APIConnector:
    def __init__(self):
        with open("login.json", "r") as f:
            self.login = json.load(f)
            self.auth_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + self.login["TOKEN"]
            }

    def reload_login(self):
        with open("login.json", "r") as f:
            self.login = json.load(f)
            self.auth_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + self.login["TOKEN"]
            }

    def send_http_req(self, api_path):
        return requests.get(api_path, headers=self.auth_headers)

# recursively counts the number of folders and files in the download folder
stats = [-1, 0] # [folders, files] Start at -1 to ignore the "downloads" folder itself
def stat_downloads(path):
    if os.path.isfile(path):
        stats[1] += 1
        return stats
    else:
        stats[0] += 1
        for file_entry in os.listdir(path):
            stat_downloads(os.path.join(path, file_entry))
        return stats

# The following function is from https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
def get_dir_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def clear_downloads():
    if os.path.exists("downloads"):
        series_count = 0
        for series in os.listdir("downloads"):
            series_count += 1

        counts = stat_downloads("downloads")
        total_size = get_dir_size(start_path="downloads")
        shutil.rmtree("downloads")

        # Convert total_size in bytes to a human-readable format
        sizes = ["B", "KB", "MB", "GB", "TB"]
        size_index = 0

        while total_size > 1024:
            total_size /= 1024
            size_index += 1
        
        total_size_str = "{:.2f} {}".format(total_size, sizes[size_index])

        print("Deleted {} series, {} folders, and {} files totaling {}".format(series_count, counts[0], counts[1], total_size_str))
    else:
        print("There isn't anything to delete.")
    
    # folders = ["banner", "fanart", "poster"]
    # del_count = 0
    # for folder in folders:
    #     if os.path.exists(folder):
    #         image_list = os.listdir(folder)
    #         if len(image_list) != 0:
    #             print("Clearing " + folder + "/")
    #             for x in image_list:  # TODO check if folder is empty
    #                 print("Deleting {}/{}".format(folder, x))
    #                 del_path = os.path.join(folder + "\\" + x)
    #                 os.remove(del_path)
    #                 del_count += 1
    #             print()
    #         else:
    #             print("'{}' is already empty".format(folder))
    #     else:
    #         os.makedirs(folder)
    # print("Deleted {} images.\n".format(del_count))

def clearScreen():
    IS_WINDOWS = os.name == "nt"
    if IS_WINDOWS:
        os.system("cls")
    else:
        os.system("clear")

# Clears out all illegal filename characters from the string
def create_file_name(string):
    string = string.strip()
    string = re.sub(r'(?u)[^-\w. ]', '', string)
    return string
