from authentication import login
from main import download
from main import wait
from utils import clearFolders
from utils import clearScreen
from search import search

# TODO fix naming convention for all variables and functions

while True:
    clearScreen()
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

    if choice == "1":  # TODO catch KeyboardInterrupt at search
        series = search()
        if series != None:
            download(series)
        wait()
    elif choice == "2":
        clearScreen()
        clearFolders()
        wait()
    elif choice == "3":  # TODO add a printout that tells the user who is currently logged in
        clearScreen()
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

