import keyboard
import pyautogui
import json

mausklick_koordinaten = []
map = "test"

with open(f"maps/{map}.json", 'r') as json_datei:
    data = json.load(json_datei)

print(f"MAP: {map}")
print(f"TOWERS TOTAL: {len(data[0])}")

def save_coords():
        global data

        x, y = pyautogui.position()
        arrlen = len(mausklick_koordinaten)

        data[0][arrlen]["posX"] = x
        data[0][arrlen]["posY"] = y

        mausklick_koordinaten.append({"posX": x, "posY": y})
        print(f"X: {x}, Y: {y}")

def write_to_file():
    with open(f"maps/{map}.json", 'w') as datei:
        json.dump(data, datei, indent=4)
    print("Saved Successfully")

for tower in data[0]:
    print(f"Save coords for: {tower['id']}")
    keyboard.wait("p")
    save_coords()

write_to_file()
keyboard.unhook_all()