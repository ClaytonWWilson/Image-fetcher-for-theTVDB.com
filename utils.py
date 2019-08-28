import json
import os
import re
import requests
import shutil


# Handles all communication to the API
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

# Simple progress bar for long file download operations
class ProgressBar:
    def __init__(self, size, counter=None):
        self.size = int(size)

        # Creating the bar array which will be the visual representation of the progress bar
        self.bar_array = []
        for i in range(0, 21):
            bar = ''
            bar += '['
            j = -1
            for j in range(0, i):
                bar += '='
            for k in range(j, 19):
                bar += ' '
            bar += ']'
            self.bar_array.append(bar)

        if counter is None:
            self.counter = 0
        else:
            self.counter = int(counter)
            if self.counter < 0 or self.counter > self.size:
                raise IndexError("ProgressBar counter out of bounds.")

    def increment(self):
        self.counter += 1
        if (self.counter > self.size):
            raise IndexError("ProgressBar counter out of bounds.")

    def get_percent(self):
        return int((self.counter / self.size) * 100)

    def to_string(self):
        return self.bar_array[int((self.counter / self.size) * 20)]

    def print(self):
        print(self.to_string())



# Recursively counts the number of folders and files in the download folder.
# It's used for displaying stats on how much is in the "downloads" folder
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

def clear_screen():
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
