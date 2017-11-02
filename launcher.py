import os                   # TODO: change the order of all import statements to 1. standard library
from login import *         # TODO: 2. related 3rd party
from actions import *       # TODO: 3. local application with blank lines between

def clear_screen():
    IS_WINDOWS = os.name == "nt"
    if IS_WINDOWS:
        os.system("cls")
    else:
        os.system("clear")

def user_choice():
    return input("> ").lower().strip()

def wait():
    input("Press enter to continue.")

while True:
    clear_screen()
    print("=============================\n"
          "Image fetcher for theTVDB.com\n"
          "=============================\n")

    print("1. Search theTVDB.com")
    print("2. Clear download folders")
    print("3. Change login")
    print("4. Refresh API Token")
    print("5. Install Requirements")
    print("6. Check for updates\n")
    print("0. Exit\n")

    choice = user_choice()

    if choice == "1":
        print("Search")
        break
    elif choice == "2":
        clearFolders()
        wait()
    elif choice == "3":
        clear_screen()
        clearLogin()
        login()
        wait()
    elif choice == "4":
        refreshToken()# TODO implement this
        wait()
    elif choice == "5":
        print("install requirements")
        break
    elif choice == "6":
        print("update")
        break
    elif choice == "0":
        exit()
