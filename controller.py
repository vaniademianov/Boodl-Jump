import websocket
import serial 
import os 
import threading, queue 
from res.resource_manager import resource_manager as rm 
from environment import classifier
import pygame 
from other.utils import Utilz
from other.cons import *
import keyboard 
import time 

class NewInformator(threading.Thread):
    def __init__(self, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.daemon = True

    def run(self):
        self.do_thing()

    def do_thing(self):

        while True:
            pos1 = "520 518"
            try:
                if keyboard.is_pressed('w'):
                    pos1 = "520 0"
                elif keyboard.is_pressed('a'):
                    pos1 = "0 518"
                elif keyboard.is_pressed('s'):
                    pos1 = "520 1023"
                elif keyboard.is_pressed('d'):
                    pos1 = "1023 518"
                if keyboard.is_pressed('left shift'):
                    pos1 += " 0"
                else:
                    pos1 += " 1"
            except:
                pass

            pos2 = "520 518"
            try:
                if keyboard.is_pressed('up'):
                    pos2 = "520 0"
                elif keyboard.is_pressed('left'):
                    pos2 = "0 518"
                elif keyboard.is_pressed('down'):
                    pos2 = "520 1023"
                elif keyboard.is_pressed('right'):
                    pos2 = "1023 518"
                if keyboard.is_pressed('right shift'):
                    pos2 += " 0"
                else:
                    pos2 += " 1"
            except:
                pass
            btns = ''
            try:
                btns += '1: 0 ' if keyboard.is_pressed('z') else '1: 1 '
                btns += '2: 0 ' if keyboard.is_pressed('x') else '2: 1 '
                btns += '3: 0 ' if keyboard.is_pressed('c') else '3: 1 '
                btns += '4: 0 ' if keyboard.is_pressed('v') else '4: 1 '
                btns += '5: 0 ' if keyboard.is_pressed('b') else '5: 1 '
                btns += '6: 0' if keyboard.is_pressed('n') else '6: 1'
            except:
                pass
            self.queue.put(' '.join([pos1, btns, pos2]))
            time.sleep(0.2)
class SerialInformator(threading.Thread):
    def __init__(self, queue,serial, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.daemon = True
        self.serial = serial 
        self.lock = threading.Lock()
    def run(self):
        self.do_thing()

    def do_thing(self):
        while True:
            with self.lock:
                rl = serial.readline()
                sl = str(rl)
                if "\\n" in sl:
                    try:
                        self.queue.put(str(rl, encoding="utf-8"))
                    except UnicodeDecodeError:
                        pass

class WsInformator:
    def afterInit(self, ws):
        self.ws = ws 
        ws_thread = threading.Thread(target=self.rf)
        ws_thread.daemon = True
        ws_thread.start()
        

    def __init__(self,queue,parent) -> None:
        self.parent = parent
        self.queue = queue

    def on_open(self, ws):
        print("Connected to WebSocket server successfully")

    def on_message(self, ws, message):
        # print(message)
        if not b"0x" in message:
            try:
                self.queue.put(message.decode("utf8"))
            except UnicodeDecodeError:
                print("Error decoding message from WebSocket server")

    
    def on_error(self, ws, error):
        print("WebSocket errored:", error)
        self.parent.switch_controller_type()
        self.ws.keep_running = False
        self.ws.close()
    def on_close(self, ws,t,d):
        print("Disconnected from WebSocket server, make sure you plugged in your controller correctly")
        self.parent.switch_controller_type()
        self.ws.keep_running = False
        # self.ws.close()
    def rf(self):
        self.ws.run_forever(skip_utf8_validation=True)    
        print("FINISH")
class Controller: 
    def __init__(self) -> None:
        self.q = queue.Queue()
        self.ws_controller_address = "ws://esp8266.local:81"
        self.controller_type = ""
        self.ws = None
        self.COM_PORT = "COM6"
        self.state = 0
        self.time_from_start = 0
        self.COM_0_COM_PORT = "COM9"
        self.is_classifier_available = False 
        self.can_try_to_connect_simulator = False 
        self.Informator = None 
        self.Classifier = None
    def controller_calibration(self): 
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT),)
        pygame.display.set_caption("Let's calibrate your controller!")
        clock = pygame.time.Clock()
        font = rm.get_brownie_s(43)

        run = True 
        while run: 
            clock.tick(FPS)
            self.time_from_start += 1
            screen.fill((220, 60,60))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 
                    exit(2)

            lc = font.render("Let's calibrate your controller!", False, (255,255,255))
            screen.blit(lc,  Utilz.convert_center_to_top_left(WIDTH/2, 60, lc.get_width(), lc.get_height()))
            if self.state == 0 or self.state == 1:
                print("Y")
                if self.time_from_start == 1: 
                    self.switch_controller_type() 
                text = font.render("Make sure that it's plugged in...",False, (255,255,255))
                pos = Utilz.convert_center_to_top_left(WIDTH/2, 150, text.get_width(), text.get_height())
                text2 = font.render("Trying controller type of " +self.controller_type +"...",False, (255,255,255))
                pos2 = Utilz.convert_center_to_top_left(WIDTH/2, 230, text2.get_width(), text2.get_height())                 
                
                if self.time_from_start >= FPS*10:
                    text = font.render("Trying yet again...",False, (255,255,255))
                    prev_st = self.state
                    self.state = 1
                    pos = Utilz.convert_center_to_top_left(WIDTH/2, 150, text.get_width(), text.get_height())
                    self.can_try_to_connect_simulator = True 
                    if prev_st == 0:
                        self.controller_type = ""
                        self.switch_controller_type()
                screen.blit(text, pos)
                screen.blit(text2, pos2)
            
            pygame.display.flip()
    def tick(self): 
        pass 
    def classify_joystick(self, joystick_number) -> str: 
        pass 
    def read_button_state(self, button_number) -> bool: 
        pass 
    def switch_controller_type(self):
        if not self.controller_type: 
            print("Trying RG")
            self.controller_type = "rg"
            self.try_connecting_rg()
        elif self.controller_type == "rg":
            print("Trying old RG")
            self.controller_type = "oldrg"
            self.try_connecting_old_rg()
        elif self.controller_type == "oldrg" and self.can_try_to_connect_simulator: 
            self.controller_type = "oldsim"
            print("Trying old sim")
            self.try_connecting_old_sim()
        elif self.controller_type == "oldsim" and self.can_try_to_connect_simulator:
            self.controller_type = "sim"
            print("Trying sim")
            self.try_connecting_new_sim()
        else: 
            print("Failed to load with " + self.controller_type+ ". Exiting.")
            exit(1)
    def try_connecting_new_sim(self): 
        self.Informator = NewInformator(self.q)
        self.Informator.start()
    def try_connecting_old_sim(self): 
        if not os.path.exists("C:\Program Files (x86)\com0com\setupc.exe"):
            self.switch_controller_type()
            return
        import simulator
        self.try_connecting_old_rg(self.COM_0_COM_PORT)
        

    def try_connecting_old_rg(self, port = None):
        if not port: 
            port = self.COM_PORT 
        try: 
            self.serial = serial.Serial(self.COM_PORT)
            self.Informator = SerialInformator(self.q, self.serial)
            self.Informator.start()
            return True 
        except: 
            print("Failed to open serial. Trying other simulator.")
            self.switch_controller_type()
            return False 
    def try_connecting_rg(self):
        self.Informator = WsInformator(self.q, self)
        self.ws = websocket.WebSocketApp(self.ws_controller_address, on_open=self.Informator.on_open, on_message=self.Informator.on_message, on_error=self.Informator.on_error, on_close=self.Informator.on_close,)
        self.Informator.afterInit(self.ws)
 