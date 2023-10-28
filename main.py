import time
import json
import keyboard
import pyautogui
import threading

paths = {1: "left shift", 2: "alt", 3: "ctrl"}
hotkeys = {
    "Hero": "u",

    "DartMonkey": "q",
    "BoomerangMonkey": "w",
    "BombShooter": "e",
    "TackShooter": "r",
    "IceMonkey": "t",
    "GlueGunner": "z",

    "SniperMonkey": "y",
    "MonkeySub": "x",
    "BuccaneerMonkey": "c",
    "MonkeyAce": "v",
    "HeliPilot": "b",
    "MortarMonkey": "n",
    "DartlingGunner": "m",

    "WizardMonkey": "a",
    "SuperMonkey": "s",
    "NinjaMonkey": "d",
    "Alchemist": "f",
    "Druid": "g",

    "BananaFarm": "h",
    "SpikeFactory": "j",
    "MonkeyVillage": "k",
    "MonkeyEngineer": "l",
    "BeastHandler": "i",
}
towers = []

events = {
    "candy": "images/candy.png",
    "totem": "",
    "easter": "",
    "rockets": "",
    "christmas": "",
}
current_event = "candy"

map_coords = {
    1: {"posX": 270, "posY": 120},
    2: {"posX": 750, "posY": 120},
    3: {"posX": 1220, "posY": 120},
    4: {"posX": 270, "posY": 480},
    5: {"posX": 750, "posY": 480},
    6: {"posX": 1220, "posY": 480}
}
map_width = 450
map_height = 350

def click(x, y):
    pyautogui.moveTo(x, y, duration=0.2)
    pyautogui.click(x, y)

def press(key):
    keyboard.press_and_release(key)

def getTowerById(tower_id):
    for tower in towers:
        if tower["id"] == tower_id:
            result = tower
            break

    return result

def getData(map_file):
    path = "maps/" + map_file + ".json"
    with open(path, 'r') as json_datei:
        data = json.load(json_datei)
    
    i = 0

    for tower in data[0]:
        tower["upgrades"] = "0-0-0"
        tower["index"] = i
        tower["placed"] = False
        tower["hotkey"] = hotkeys[tower["tower"]]

        i += 1

    return data[0], data[1]

def changeStatus(targetStatus):
    global status
    if targetStatus == "slow" and status != "slow":
        press("space")
        time.sleep(.1)
    
    if targetStatus == "fast" and status != "fast":
        press("space")
        time.sleep(.1)

    if targetStatus == "fast" and status == "stop":
        press("space")
        time.sleep(.1)

    status = targetStatus

def placeTower(tower_id):
    tower = getTowerById(tower_id)
    press(tower["hotkey"])
    time.sleep(.5)
    click(tower["posX"], tower["posY"])

    towers[tower["index"]]["placed"] = True

def upgradeTower(tower_id, targeted_upgrades):
    tower = getTowerById(tower_id)
    
    target_split = targeted_upgrades.split("-")
    target_upgrades = [int(splits) for splits in target_split]

    current_split = tower["upgrades"].split("-")
    current_upgrades = [int(splits) for splits in current_split]

    upgrades_p1 = target_upgrades[0] - current_upgrades[0]
    upgrades_p2 = target_upgrades[1] - current_upgrades[1]
    upgrades_p3 = target_upgrades[2] - current_upgrades[2]

    click(tower["posX"], tower["posY"])
    time.sleep(0.05)

    for i in range(upgrades_p1):
        press(paths[1])
        time.sleep(0.2)
    for i in range(upgrades_p2):
        press(paths[2])
        time.sleep(0.2)
    for i in range(upgrades_p3):
        press(paths[3])
        time.sleep(0.2)
    
    towers[tower["index"]]["upgrades"] = targeted_upgrades

    if tower["tower"] == "Druid" and target_upgrades[1] == 3:
        press("tab")
        time.sleep(0.2)

    press("esc")

def targetTower(tower_id, count):
    tower = getTowerById(tower_id)

    click(tower["posX"], tower["posY"])

    for i in range(count):
        press("tab")
        time.sleep(0.2)
    
    press("esc")

def sellTower(tower_id):
    tower = getTowerById(tower_id)

    click(tower["posX"], tower["posY"])
    time.sleep(0.2)
    press("backspace")

def playback(map):
    global towers
    global status

    towers, steps = getData(map)
    time.sleep(1)

    for step in steps:

        print(step)

        if step["action"] == "start":
            changeStatus("fast")
        
        if step["action"] == "place":
            placeTower(step["id"])
        
        if step["action"] == "wait":
            time.sleep(step["time"])
        
        if step["action"] == "upgrade":
            upgradeTower(step["id"], step["upgrades"])
        
        if step["action"] == "target":
            targetTower(step["id"], step["count"])

        if step["action"] == "sell":
            sellTower(step["id"])
        
        if status == "defeat":
            print("DEFEAT")
            break

        if status == "victory":
            print("VICTORY")
            break
    
        time.sleep(.2)

def selectExpert():
    click(1360, 1080)
    time.sleep(.5)

def getMap():
    image = events[current_event]

    if pyautogui.pixelMatchesColor(858, 1072, (109, 235, 0), tolerance=10):
        click(858, 1072)
        time.sleep(0.5)

    if pyautogui.pixelMatchesColor(1165, 840, (62, 155, 248), tolerance=10):
        page = 1
    else:
        page = 2
    
    if page == 2:
        selectExpert()

    if pyautogui.locateOnScreen(image, region=(270, 120, 450, 350), grayscale=True, confidence=0.8) != None:
        map = "dark_dungeons"
        position = 1
        time.sleep(0.5)
    elif pyautogui.locateOnScreen(image, region=(750, 120, 450, 350), grayscale=True, confidence=0.8) != None:
        map = "sanctuary"
        position = 2
        time.sleep(0.5)
    elif pyautogui.locateOnScreen(image, region=(1220, 120, 450, 350), grayscale=True, confidence=0.8) != None:
        map = "ravine"
        position = 3
        time.sleep(0.5)
    elif pyautogui.locateOnScreen(image, region=(270, 480, 450, 350), grayscale=True, confidence=0.8) != None:
        map = "flooded_valley"
        position = 4
        time.sleep(0.5)
    elif pyautogui.locateOnScreen(image, region=(750, 480, 450, 350), grayscale=True, confidence=0.8) != None:
        map = "infernal"
        position = 5
        time.sleep(0.5)
    elif pyautogui.locateOnScreen(image, region=(1220, 480, 450, 350), grayscale=True, confidence=0.8) != None:
        map = "bloody_puddles"
        position = 6
        time.sleep(0.5)
    else:
        selectExpert()

        if pyautogui.locateOnScreen(image, region=(270, 120, 450, 350), grayscale=True, confidence=0.8) != None:
            map = "workshop"
            position = 1
            time.sleep(0.5)
        elif pyautogui.locateOnScreen(image, region=(750, 120, 450, 350), grayscale=True, confidence=0.8) != None:
            map = "quad"
            position = 2
            time.sleep(0.5)
        elif pyautogui.locateOnScreen(image, region=(1220, 120, 450, 350), grayscale=True, confidence=0.8) != None:
            map = "dark_castle"
            position = 3
            time.sleep(0.5)
        elif pyautogui.locateOnScreen(image, region=(270, 480, 450, 350), grayscale=True, confidence=0.8) != None:
            map = "muddy_puddles"
            position = 4
            time.sleep(0.5)
        elif pyautogui.locateOnScreen(image, region=(750, 480, 450, 350), grayscale=True, confidence=0.8) != None:
            map = "ouch"
            position = 5
            time.sleep(0.5)
        else:
            map = "ERROR"
            time.sleep(0.5)
    return map, position

def selectMode(difficulty):
    if difficulty == "easy":
        click(580, 460)
    if difficulty == "medium":
        click(915, 460)
    if difficulty == "hard":
        click(1310, 460)
    
    time.sleep(0.5)

    click(585, 650)

def selectMap(position):
    map_x = map_coords[position]["posX"]
    map_y = map_coords[position]["posY"]

    click_x = map_x + map_width / 2
    click_y = map_y + map_height / 2

    click(click_x, click_y)
    time.sleep(.5)
    selectMode("easy")
    time.sleep(5)

def checkForEnd():
    global status
    while True:
        if pyautogui.locateOnScreen("images/victory.png", region=(600, 130, 700, 160), grayscale=True, confidence=0.8):
            status = "victory"
            break;
    
        if pyautogui.locateOnScreen("images/game_over.png", region=(600, 200, 700, 350), grayscale=True, confidence=0.8):
            status = "defeat"
            break;

    print(status)

    if status == "victory":
        print("SPIEL BEENDET")
        time.sleep(1)
        click(1009, 1010)
        time.sleep(1)
        click(690, 940)
        time.sleep(3)
    
    if status == "defeat":
        print("GAME OVER")
        time.sleep(1)
        click(583, 895)
        time.sleep(3)

time.sleep(2)
click(583, 895)
time.sleep(3)

for i in range(100):
    status = "stop"

    print(f"SPIEL {i+1}")

    map, position = getMap()
    selectMap(position)

    print(f"MAP {map}")

    playback_thread = threading.Thread(target=playback, args=(map,))
    checkForEnd_thread = threading.Thread(target=checkForEnd)
    
    playback_thread.start()
    checkForEnd_thread.start()

    playback_thread.join()
    checkForEnd_thread.join()

    print("neues spiel wird gestartet")
    
    time.sleep(3)