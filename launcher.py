import os                   # TODO: change the order of all import statements to 1. standard library
from login import *         # TODO: 2. related 3rd party
from actions import *       # TODO: 3. local application. with blank lines between and remove wilcard symbols
from search import search

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
    print("4. Refresh API Token")
    print("5. Install Requirements")
    print("6. Check for updates\n")
    print("0. Exit\n")

    choice = user_choice()

    if choice == "1":
        search()
        wait()
    elif choice == "2":
        clear_screen()
        clearFolders()
        wait()
    elif choice == "3":
        clear_screen()
        clearLogin()
        login()
        wait()
    elif choice == "4":
        clear_screen()
        refreshToken()
        wait()
    elif choice == "5":
        print("install requirements")
        break
    elif choice == "6":
        update()
        wait()
    elif choice == "0":
        exit()
