from colorama import init, Fore, Back
import pyautogui
import keyboard
import time
import json
from itertools import product
init()

class Codes:
    start = f"[{Fore.BLUE} START {Fore.RESET}]"
    ok =    f"[{Fore.GREEN} OK {Fore.RESET}]"
    info  = f"[{Fore.CYAN} INFO {Fore.RESET}]"
    error = f"[ {Back.RED}ERROR{Back.RESET} ]"
    end =   f"[{Fore.MAGENTA} END {Fore.RESET}]"

class Main:
    def __init__(self) -> None:
        self.flag = False
        self.loop_flag = True
    
    def start(self):
        print(f" ---[{Fore.GREEN} Promo Writer {Fore.RESET}]--- by {Fore.RED}KrouZ_CZ{Fore.RESET}\n")

        self.load_settings()
        self.add_hotkey()
        self.load_codes()
        self.add_stop()

        while True:
            for i, code in enumerate(self.codes):
                if not self.loop_flag: return
                
                print(f"{Codes.start} Начинаю перебор строки{Fore.CYAN}: {i+1}{Fore.RESET}")
                self.do_write_code(code)
            if not self.loop:
                break

    def stop(self):
        print(f"{Codes.ok} Экстренное выключение программы")
        self.loop_flag = False

    def add_stop(self):
        print(f"{Codes.info} Добавляю хоткей {Fore.RED}ESC{Fore.RESET} для выхода из программы")
        keyboard.add_hotkey("esc", self.stop)

    def do_write_code(self, code):
        while not self.flag:
            if not self.loop_flag:
                return
            time.sleep(0.1)

        if self.clear_section:
            pyautogui.hotkey('ctrl', 'a')
            keyboard.press_and_release('del')

        pyautogui.write(code, self.type_delay)

        if self.mouse_type:
            pyautogui.click()
        else:
            keyboard.press_and_release('enter')
        
        if self.wait_bind:
            self.flag = False

    def load_codes(self):
        try:
            with open("codes.txt", 'r') as file:
                codes = file.readlines()
        except:
            print(f"{Codes.error} Ошибка загрузки файла, создаю его")
            open("codes.txt", 'w').close()
            raise SystemExit()
        self.codes = []
        [self.codes.extend(self.generate_strings(code)) for code in codes]

        print(f"{Codes.info} Строк успешно загружено: {len(self.codes)}")

    def generate_strings(self, mask):
        characters = []
        for char in mask:
            if char == '#':
                characters.append('0123456789')
            elif char == '*':
                characters.append('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
            elif char == '?':
                characters.append('!@#$%^&*()_-+=<>?/[]{},.:;')
            else:
                characters.append(char)

        combinations = product(*characters)
        generated_strings = [''.join(combination) for combination in combinations]
        return generated_strings

    def add_hotkey(self):
        keyboard.add_hotkey(self.bind, self.switch_flag)
        print(f"{Codes.info} Сделал хоткей на {Fore.RED}{self.bind}{Fore.RESET}")

    def switch_flag(self):
        self.flag = True

    def load_settings(self):
        try:
            with open("settings.json", "r") as file:
                obj = json.load(file)
                print(f"{Codes.ok} Успешно загрузил конфиг")
        except:
            print(f"{Codes.error} Нет конфига, создаю новый")
            self.create_config()
            obj = {}

        self.bind = obj.get("bind", "f8")
        self.mouse_type = obj.get("mouse_type", True)
        self.type_delay = obj.get("type_delay", 0.01)
        self.clear_section = obj.get("clear_section", True)
        self.wait_bind = obj.get("wait_bind", True)
        self.loop = obj.get("loop", False)

    def create_config(self):
        with open("settings.json", "w") as file:
            json.dump(
                {"bind": "f8", 
                 "mouse_type": True, 
                 "type_delay": 0.01, 
                 "clear_section": True, 
                 "wait_bind": True, 
                 "loop": False
                 }, file, ensure_ascii=False, indent=4)

    

if __name__ == "__main__":
    main = Main()

    try:
        main.start()
    except SystemExit:
        pass
    input("Enter to close")