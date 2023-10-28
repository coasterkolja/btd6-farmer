import keyboard
import pyautogui
import json

mausklick_koordinaten = []
filename = "ouch"

with open(f"maps/{filename}.json", 'r') as json_datei:
    data = json.load(json_datei)

def speichere_mausklick_koordinaten(e):
        global data

        x, y = pyautogui.position()
        arrlen = len(mausklick_koordinaten)

        data[0][arrlen]["posX"] = x
        data[0][arrlen]["posY"] = y

        mausklick_koordinaten.append({"posX": x, "posY": y})
        print(f"Mausklick-Koordinaten gespeichert: {x}, {y} Eintrag {arrlen}")

def schreibe_json_datei(e):
    if e.name == 'o':
        with open(f"maps/{filename}.json", 'w') as datei:
            json.dump(data, datei, indent=4)

keyboard.on_press_key('p', speichere_mausklick_koordinaten)
keyboard.on_press_key('o', schreibe_json_datei)

keyboard.wait('esc')
keyboard.unhook_all()