import os

from login import login
from actions import wait
from actions import clear_screen
from actions import clearFolders
from actions import refreshToken
from actions import update
from search import search

# TODO fix naming convention for all variables and functions

def user_choice():
    return input("> ").lower().strip()

while True:
    clear_screen()
    print("=============================\n"
          "Image fetcher for theTVDB.com\n"
          "=============================\n")

    print("1. Search theTVDB.com")
    print("2. Clear download folders")
    print("3. Login/Change login")
    # print("4. Refresh API Token")
    print("4. Install Requirements")
    print("5. Check for updates\n")
    print("0. Exit\n")

    choice = user_choice()

    if choice == "1":
        search()
        wait()
    elif choice == "2":
        clear_screen()
        clearFolders()
        wait()
    elif choice == "3":  # TODO if already logged in, ask 'are you sure?'
        clear_screen()   # TODO wait to clear login and add a ctrl+c option to cancel
        # clearLogin()
        login()
        wait()
    # elif choice == "4":  # TODO need to perform this option automatically
    #     clear_screen()
    #     refreshToken()
    #     wait()
    elif choice == "4":
        print("install requirements not implemented yet")
        wait()
    elif choice == "5":
        update()
        wait()
    elif choice == "0":
        exit()
