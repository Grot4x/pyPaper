#!/usr/bin/env python3
import requests
import os
import json
import shutil
from time import gmtime, strftime

CONFIG_PATH = "/.pyPaper.conf"

DEFAULT_CONFIG = {}
DEFAULT_CONFIG["BASE_PATH"] = "/pyPaper"
DEFAULT_CONFIG["MAX_COUNT"] = 10
DEFAULT_CONFIG["CURRENT_COUNT"] = 0
DEFAULT_CONFIG["RESOLUTION"] = "1920x1080"  # 1920x1080 1336x768 1680x1050
DEFAULT_CONFIG["LOG_FILE"] = "/.pyPaper.log"


def moveFile(old, new):
    """
    Move file to new generic name
    """
    newdir = DEFAULT_CONFIG["BASE_PATH"]+"/"+new
    try:
        os.rename(old, new)
    except IOError as e:
        print("Woops that should not have happend!")


def newImage():
    """
    Download Image from unsplash write url to log file and save file to disk
    """
    newname = DEFAULT_CONFIG["BASE_PATH"]+"/"+str(DEFAULT_CONFIG["CURRENT_COUNT"])+".jpg"
    url = "https://source.unsplash.com/random/" + DEFAULT_CONFIG["RESOLUTION"]
    r = requests.get(url, stream=True)
    now = strftime("%d.%m.%Y - %H:%M:%S", gmtime())
    with open(DEFAULT_CONFIG["LOG_FILE"], 'a') as log:
        log.write(now+": "+r.url+"\n")

    if r.status_code == 200:
        with open(newname, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                print(DEFAULT_CONFIG["CURRENT_COUNT"])
                DEFAULT_CONFIG["CURRENT_COUNT"] = ((DEFAULT_CONFIG["CURRENT_COUNT"] + 1)
                                                   % (DEFAULT_CONFIG["MAX_COUNT"] + 1))


def main():
    # Load or create config and log file
    global DEFAULT_CONFIG
    if not os.path.exists(CONFIG_PATH):
        f = open(CONFIG_PATH, 'w')
        f.write(json.dumps(DEFAULT_CONFIG, indent=4))
    else:
        f = open(CONFIG_PATH, 'r')
        DEFAULT_CONFIG = json.loads(f.read())
    if not os.path.exists(DEFAULT_CONFIG["LOG_FILE"]):
        f = open(CONFIG_PATH, 'w').close()
    # load a new Image
    newImage()
    # write config
    f = open(CONFIG_PATH, 'w')
    f.write(json.dumps(DEFAULT_CONFIG, indent=4))
    image = "file://"+DEFAULT_CONFIG["BASE_PATH"]+"/"+str(DEFAULT_CONFIG["CURRENT_COUNT"]-1)+".jpg"
    # try to set wallpaper
    if os.name == 'posix':
        print("Detected posix system going to set wallpaper")
        command = "gsettings set org.gnome.desktop.background picture-uri %s" % (image)
        os.system(command)
    # if os.name == 'nt':
    #     print("Detected Windows going to set wallpaper")
    #     SPI_SETDESKWALLPAPER = 20
    #     ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, image, 0)


if __name__ == '__main__':
    main()
