import serial, pyautogui
import keyboard, time
ser = serial.Serial("COM8")
def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def setter(cords, jb, b1, b2,b3,b4,b5,b6):
    ser.write(bytes(f"{cords[0]} {cords[1]} {jb} 1: {b1} 2: {b2} 3: {b3} 4: {b4} 5: {b5} 6: {b6}\n", encoding="utf-8"))
def cp(key):
    return not keyboard.is_pressed(key)
res = pyautogui.size()
while True:
    pos = pyautogui.position()
    x = round(arduino_map(pos[0], 0, res[0], 0, 1024))
    y = round(arduino_map(pos[1], 0, res[1], 0, 1024))
    setter((x,y), int(cp("1")), int(cp("2")), int(cp("3")), int(cp("4")), int(cp("5")), int(cp("6")), int(cp("7")))
    print("sent")
    time.sleep(0.2)
    
    
