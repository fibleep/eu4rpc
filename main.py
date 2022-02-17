import os
import time

import psutil
from pypresence import Presence

# Checking for eu4.exe in processes...
for proc in psutil.process_iter():
    if proc.name() == "eu4.exe":
        print("EU4 detected with PID: " + str(proc.pid))
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']
savefile_path = os.environ['USERPROFILE'] + "\\Documents\\Paradox Interactive\\Europa Universalis IV\\save games\\"
startepoch = time.time()
flag = True
# connection with discord app to extract uploaded flags and update rich presence
RPC = Presence('909907437946044416')
RPC.connect()
RPC.update(state="Loading...",
           large_text="Europa Universalis IV", large_image="eu4logolarge",
           start=startepoch)
try:
    os.listdir(savefile_path)
except:
    print('using alternate savefile path...')
    savefile_path = os.environ[
                        'USERPROFILE'] + "\\OneDrive\\Documents\\Paradox Interactive\\Europa Universalis IV\\save games\\"
save_list = os.listdir(savefile_path)
try:
    savefile_name = save_list[0]
    date_max = os.stat(savefile_path + save_list[0])
    date_max = date_max.st_mtime
except:
    print('Error! No save files found')
    savefile_name = 'no saves found'
counter = 0
# main loop to check for save updates and update rich presence
while True:
    for sav in save_list:
        date = os.stat(savefile_path + sav)
        if date.st_mtime > date_max:
            savefile_name = sav
            if not flag:
                print('Newer save found!')
            flag = True
            date_max = date.st_mtime

    print("Using data from:", savefile_name)
    if flag:
        print("Changes found, updating...")
        i = 1
        f = open(savefile_path + savefile_name, "r")
        try:
            contents = f.read()
            f.close()
            listconts = contents.split()
            listconts2 = contents.splitlines()
            isMultiplayer = 1
            try:
                listconts.index("multiplayer=yes")
            except:
                isMultiplayer = 0
            x = listconts.index("EU4txt")
            # decoding the save file
            country_name = listconts2[x + 4][24:-1]
            country_name_rev = listconts2[x + 12][24:-1]
            country_tag = listconts[x + 3][8:-1]
            current_month = months[int(float(listconts[x + 1][10:][:-1][:-1])) - 1]
            current_year = listconts[x + 1][5:9]
            country_rank_num = listconts[listconts.index("human=yes") + 3][16:]

            if isMultiplayer == 1:
                state = "Multiplayer"
            else:
                state = "Singleplayer"

            if int(country_rank_num) == 1:
                country_rank = "Duchy"
            elif int(country_rank_num) == 2:
                country_rank = "Kingdom"
            else:
                country_rank = "Empire"

            stateMessage = ""

            if 'Revolutionary' in listconts2[x + 12][24:-1]:
                details = f"{country_name_rev}"
            else:
                details = f"{country_rank} of {country_name}"

            if counter == 0:
                stateMessage = f"{current_month} of {current_year}"
                counter = counter + 1
            else:
                stateMessage = f"Playing in {state}"
                counter = 0

            RPC.update(state=f"{stateMessage}",
                       details=details,
                       large_text=country_tag, large_image=f"{country_tag.lower()}",
                       start=startepoch)
            flag = False
            print("Updated presence successfully")
        except:
            RPC.update(state="Playing in Iron Man",
                       details='Singleplayer',
                       large_text='Europa Universalis IV', large_image='eu4logo',
                       start=startepoch)
    print("Checking for changes...")
    time.sleep(20)
