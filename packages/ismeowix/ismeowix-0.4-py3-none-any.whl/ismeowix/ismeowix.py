#!/usr/bin/env python
# ismeowix - Simple library that should generally be called at the beginning of most Meowix Linux Python scripts which checks if the script is running on the intended OS
# Depends on the following, installable with `pacman`: python-distro, python-colorama. If on a non-Arch Linux based OS:
# For Linux, use your distribution-specific package manager, e.g., `apt`, `yum`, or `dnf`.
# For macOS and Windows, use `pip`: `pip install distro colorama`.

import platform # Gets the broader OS type
import sys # In order to exit with an error when necessary
from colorama import Fore, Style # In order to make the errors look nice and colorful

def check(): # Define the function to check the current OS
    if platform.system() != "Linux": # Check if we're running on Linux
        print (Fore.RED + "ERROR: " + Style.RESET_ALL + "Sorry, this program is intended for Meowix Linux only.")
        print ("The operating system currently in use is " + Fore.GREEN + platform.system() + Style.RESET_ALL + ".") # Tell the user what OS they're on
        print ("You might want to install Meowix Linux:")
        print (Fore.BLUE + "https://github.com/Meowix-Linux/Meowix-ISO/releases/latest" + Style.RESET_ALL)
        sys.exit(1) # Exit with an error

    # We don't import the following until we verify we're on Linux, as `distro` is useless on other OSes for obvious reasons
    import distro # Gets the specific Linux distribution

    if distro.id() != "meowix":
        print (Fore.RED + "ERROR: " + Style.RESET_ALL + "Sorry, this program is intended for Meowix Linux only.")
        print ("The Linux distribution currently in use is " + Fore.GREEN + distro.name(pretty=True) + Style.RESET_ALL + ".") # Tell the user what distribution they're on
        print ("You might want to install Meowix Linux:")
        print (Fore.BLUE + "https://github.com/Meowix-Linux/Meowix-ISO/releases/latest" + Style.RESET_ALL)
        sys.exit(1) # Exit with an error

# If we're running directly, call the check() function
if __name__ == "__main__":
    check()
