import os

from login import login
from actions import wait
from actions import clear_screen
from actions import clearFolders
from actions import installReqs
from actions import refreshToken
from actions import update
from search import search

# TODO fix naming convention for all variables and functions

while True:
    clear_screen()
    print("=============================\n"
          "Image fetcher for theTVDB.com\n"
          "=============================\n")

    print("1. Search theTVDB.com")
    print("2. Clear download folders")
    print("3. Login/Change login")
    print("4. Install Requirements")
    print("5. Check for updates\n")
    print("0. Exit\n")

    choice = input("> ").lower().strip()

    if choice == "1":
        search()
        wait()
    elif choice == "2":
        clear_screen()
        clearFolders()
        wait()
    elif choice == "3":  # TODO add a printout that tells the user who is currently logged in
        clear_screen()
        login()
        wait()
    elif choice == "4":
        installReqs()
        wait()
    elif choice == "5":
        update()
        wait()
    elif choice == "0":
        exit()
