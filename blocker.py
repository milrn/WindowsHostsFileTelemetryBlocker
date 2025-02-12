import urllib.request
from datetime import datetime
import ctypes
today = datetime.now()
#check if script is running as administrator
def is_running_elevated():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"An error occured while checking user privileges: {e}")
        print("")
        print("------------------------------------------------------------------------------------------------")
        exit()
hagezi = 'https://raw.githubusercontent.com/hagezi/dns-blocklists/main/domains/native.winoffice.txt'
hosts_file_path = r"C:\Windows\System32\drivers\etc\hosts"
print("------------------------------------------------------------------------------------------------")
print("")
print("Microsoft Windows 11 Hosts File Telemetry Blocker (Windows 11) - By milrn")
print("")
print("------------------------------------------------------------------------------------------------")
print("")
#only runs if the user is running the script as an administrator
if is_running_elevated() == True:
    def mainmenu():
        print("1. Install update from hagezi (auto-updated list)")
        print("2. Add domains manually")
        print("3. Remove domains manually")
        print("4. Exit")
        option = input("")
        print("")
        print("------------------------------------------------------------------------------------------------")
        print("")
        run(option)
    def run(option):
        #download updated host list from hagezi's github repository
        if option == "1":
            try:
                urllib.request.urlretrieve(hagezi, "hageziblocklist.txt")
                print("Update downloaded successfully.")
            except Exception as e:
                print(f"Failed to download update: {e}.")
                print("")
                print("------------------------------------------------------------------------------------------------")
                print("")
                mainmenu()
            print("")
            print("Installing...")
            print("")
            try:
                #add a update log to the hosts file
                hasUpdate = False
                with open(hosts_file_path, 'a') as hosts:
                    hosts.write(f'# Update Date: {today.strftime("%Y-%m-%d")}\n')
                    hosts.write(f'# Update From: hagezi\n')
                #adds the new host blocks that do not exist yet
                for line in open("hageziblocklist.txt"):
                    if "#" not in line:
                        isExist = False
                        for existingline in open(hosts_file_path, "r"):
                            if line == existingline[existingline.find(" ")+1:].strip() + "\n" and existingline.startswith("#") == False:
                                isExist = True
                        if isExist == False:
                            with open(hosts_file_path, 'a') as hosts:
                                hosts.write(f'0.0.0.0 {line}')
                                print(f"URL Blocked: {line}")
                                hasUpdate = True
                #completion message
                if hasUpdate == True:
                    with open(hosts_file_path, 'a') as hosts:
                        hosts.write(f'# Done.\n')
                else:
                    with open(hosts_file_path, 'a') as hosts:
                        hosts.write(f'# Latest Update Already Installed.\n')

                print("")
                if hasUpdate == True:
                    print("Done.")
                else:
                    print("Latest Update Already Installed.")
                print("")
                print("------------------------------------------------------------------------------------------------")
                print("")
                mainmenu()
            except Exception as e:
                print("------------------------------------------------------------------------------------------------")
                print("")
                print(f"Failed to Update Hosts File: {e}.")
                print("")
                print("------------------------------------------------------------------------------------------------")
                print("")
                mainmenu()
        #manually add block entries to host file
        elif option == "2":
            print("")
            links = []
            link = None
            while link != "-i":
                link = input("Add domain (-i to start install): ")
                links.append(link)
                print("")
            print("Installing...")
            print("")
            try:
                #add update log to hosts file
                hasUpdate = False
                with open(hosts_file_path, 'a') as hosts:
                    hosts.write(f'# Update Date: {today.strftime("%Y-%m-%d")}\n')
                    hosts.write(f'# Update From: You\n')
                #adds hosts to blocklist if they don't already exist
                for line in links:
                    if "#" not in line and line != "-i":
                        isExist = False
                        for existingline in open(hosts_file_path):
                            if line == existingline[existingline.find(" ")+1:].strip() and existingline.startswith("#") == False:
                                isExist = True
                        if isExist == False:
                            with open(hosts_file_path, 'a') as hosts:
                                hosts.write(f'0.0.0.0 {line}\n')
                                print(f"URL Blocked: {line}")
                                hasUpdate = True
                #completion message
                if hasUpdate == True:
                    with open(hosts_file_path, 'a') as hosts:
                        hosts.write(f'# Done.\n')
                else:
                    with open(hosts_file_path, 'a') as hosts:
                        hosts.write(f'# All Entries Already Exist.\n')

                print("")
                if hasUpdate == True:
                    print("Done.")
                else:
                    print("All Entries Already Exist.")
                print("")
                print("------------------------------------------------------------------------------------------------")
                print("")
                mainmenu()
            except Exception as e:
                print("------------------------------------------------------------------------------------------------")
                print("")
                print(f"Failed to Update Hosts File: {e}.")
                print("")
                print("------------------------------------------------------------------------------------------------")
                print("")
                mainmenu()
        #manually remove block entries from hosts file
        elif option == "3":
            print("")
            links = []
            link = None
            while link != "-u":
                link = input("Add domain to Remove (-u to start uninstall): ")
                links.append(link)
                print("")
            print("Uninstalling...")
            print("")
            #if the host exists --> commented out of the file
            try:
                hasUpdate = False
                for line in links:
                    if "#" not in line and line != "-u":
                        isExist = False
                        for existingline in open(hosts_file_path):
                            if line == existingline[existingline.find(" ")+1:].strip() and existingline.startswith("#") == False:
                                isExist = True
                        if isExist == True:
                            with open(hosts_file_path, 'r') as hosts:
                                fullfile = hosts.readlines()
                            with open(hosts_file_path, 'w') as hosts:
                                for eachline in fullfile:
                                    if line != eachline[eachline.find(" ")+1:].strip():
                                        hosts.write(eachline)
                                    else:
                                        print(f"URL Uninstalled: {line}")
                                        hosts.write(f"# Uninstalled: {line}\n")
                                        hasUpdate = True
                print("")
                #completion message
                if hasUpdate == True:
                    print("Done.")
                else:
                    print("Entries Do Not Exist.")
                print("")
                print("------------------------------------------------------------------------------------------------")
                print("")
                mainmenu()
            except Exception as e:
                print("------------------------------------------------------------------------------------------------")
                print("")
                print(f"Failed to Update Hosts File: {e}.")
                print("")
                print("------------------------------------------------------------------------------------------------")
                print("")
                mainmenu()
        #exit program
        elif option == "4":
            exit()
        else:
            mainmenu()
    #starts the tool
    mainmenu()
else:
    print("You need to run this script as administrator.")
    print("")
    print("------------------------------------------------------------------------------------------------")
    exit()
