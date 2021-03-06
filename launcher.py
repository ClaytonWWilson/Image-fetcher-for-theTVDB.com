from authentication import login
from main import download
from main import wait
from utils import clear_downloads
from utils import clear_screen
from search import search

# TODO fix naming convention for all variables and functions

while True:
    clear_screen()
    print("=============================\n"
          "Image fetcher for theTVDB.com\n"
          "=============================\n")

    print("1. Search theTVDB.com")
    print("2. Clear downloaded data")
    print("3. Login/Change login")
    print("4. Install Requirements")
    print("5. Check for updates\n")
    print("0. Exit\n")

    choice = input("> ").lower().strip()

    if choice == "1":  # TODO catch KeyboardInterrupt at search
        series = search() # BUG Searching for 'one punc' causes a keyerror when reading the 'data' key
        if series != None:
            download(series)
        wait()
    elif choice == "2":
        clear_screen()
        clear_downloads()
        wait()
    elif choice == "3":  # TODO add a printout that tells the user who is currently logged in
        clear_screen()
        login()
        wait()
    elif choice == "4":
        # installReqs()
        print("Not implemented")
        wait()
    elif choice == "5":
        # update()
        print("Not implemented")
        wait()
    elif choice == "0":
        exit()
