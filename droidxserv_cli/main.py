import os
import time
import subprocess
from sys_modules import utils, adb_connect,color
indent = " " * 4
def start():
    os.makedirs("./config/media-files", exist_ok=True)
    os.makedirs("./config/sys_logs", exist_ok=True)
    os.makedirs("./config/json_files", exist_ok=True)

if __name__ == "__main__":
    utils.starting_droidxserv_banner()
    start()
    print(f'\n{indent}{color.ORANGE}[{color.GREEN}+{color.ORANGE}]{color.WHITE} Starting DroidXserv Server ..... ')
    subprocess.run(['adb', 'start-server'], check=True, capture_output=True, text=True)
    time.sleep(1)
    print(f"{indent}{color.ORANGE}[{color.GREEN}+{color.ORANGE}] {color.GREEN}Ok")
    time.sleep(1)
    print(f'{indent}{color.ORANGE}[{color.GREEN}+{color.ORANGE}]{color.WHITE} Initiating services ....')
    time.sleep(1)
    print(f"{indent}{color.ORANGE}[{color.GREEN}+{color.ORANGE}] {color.GREEN}Ok\n")
    time.sleep(1.8)
    print(f'{indent}{color.ORANGE}[{color.GREEN}🚀{color.ORANGE}]{color.WHITE} Welcome to Android {color.YELLOW} Command Center   {color.ORANGE}\n')
    time.sleep(2)
    utils.clear_screen_main()
    adb_connect.adb_connect_main()
    utils.clear_screen()
