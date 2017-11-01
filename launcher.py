import os
def clear_screen():
    IS_WINDOWS = os.name == "nt"
    if IS_WINDOWS:
        os.system("cls")
    else:
        os.system("clear")

def user_choice():
    return input("> ").lower().strip()


while True:
    print("1. Search theTVDB.com")
    print("2. Clear download folders")
    print("3. Change login")
    print("4. Refresh API Token")
    print("5. Install Requirements")
    print("6. Check for updates")
    print("7. Exit")

    choice = user_choice()

    if choice == "1":
        print("Search")
        break
    elif choice == "2":
        print("Clear download")
        break
    elif choice == "3":
        print("Change login")
        break
    elif choice == "4":
        print("Refresh token")
        break
    elif choice == "5":
        print("install requirements")
        break
    elif choice == "6":
        print("update")
        break
    elif choice == "7":
        print("Exit")
