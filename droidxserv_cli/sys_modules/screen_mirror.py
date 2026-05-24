import os
import sys
import time
import subprocess
import adbutils
import adb_connect

def adb_command_center():

    while True:
        adb_com = input(f"""    
        [99. Clear screen                   0. Back]
        [scrcpy_noaudio | scrcpy | scrcpy_anon | back] \n
        [ADB command] Enter selection >>> """).lower()

        match adb_com:
            
            case "0"|"back"|"cd ..":
                 break
            case "1"|"scrcpy_noaudio":
                screencopy_noaudio()
            case "2"|"scrcpy":
                screencopy()
            case "3"|"scrcpy_anon":
                screencopy_anon()
            case "devices":
                adb_connect.list_devices()
            case other:
                print(f"\n\t[X] Invalid selection\n\tPlease enter a valid option on menu above\n")
                time.sleep(3)


#--------------------------------------------------------------------------#
#--------------------- Screen Copy Section --------------------------------#
#--------------------------------------------------------------------------#



def run_scrcpy(unique_args: list[str],max_fps: int = 60,max_size: int = 1024,bit_rate: str = "2M"):

    sc_commands = [
        "scrcpy",
        f"--max-fps={max_fps}",
        f"--max-size={max_size}",
        f"--video-bit-rate={bit_rate}",
        "--video-codec=h265",
    ]
    sc_commands.extend(unique_args)
    print(f"\n\tRUNNING: {' '.join(sc_commands)}\n")
    try:
        result = subprocess.run(sc_commands, check=True)
        # scrcpy usually writes logs to stderr
        #output = result.stderr
        #process = subprocess.Popen(sc_commands,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        #for line in process.stdout:
        #    print(f"\t{line}", end="")


    except subprocess.CalledProcessError as e:
        print(f"[ERROR] scrcpy failed: {e}")
    finally:
        print("\n\tExited Screen Mirror")


def screencopy_noaudio():
    def screencopy_noaudiokit():
        print(f'\t[Info] Starting scrcpy  No audio ......\n')
        time.sleep(0.5)
        try:
            run_scrcpy(["--no-audio"])
        finally:
            while True:
                close_option = input(f"""    
                [Do you Wish to exit : ]
                [1. Yes 2. No] \n
                [Screensr] Enter selection (Default = Yes)>>>  """).lower()
                match close_option:
                    case ""|"1"|"Y"|"Yes":
                        break
                    case " "|"2"|"N"|"No":
                        run_scrcpy(["--no-audio"])
                    case other:
                         print(f"\n\t[X] Invalid selection\n\tPlease enter a valid option on menu above\n")
                

    con_devices = adbutils.adb.device_list()
    if len(con_devices) == 0:
        print("\n")
        print(f"\n\t[No Device Connected]\n")
        time.sleep(0.8)
        print(f"\n\tChecking for connection ......\n")
        time.sleep(1.2)
        adb_connect.xconnect()
        time.sleep(1.2)
        con_devx = adbutils.adb.device_list()
        if len(con_devx) != 0:
            screencopy_noaudiokit()
    else:
        screencopy_noaudiokit()

def screencopy():
    def screencopykit():        
        print(f'\t[Info] Starting scrcpy Audio Duplicate ......\n')
        time.sleep(0.5)
        try:
            run_scrcpy(["--audio-dup"])
        finally:
            while True:
                close_option = input(f"""    
                [Do you Wish to exit : ]
                [1. Yes 2. No] \n
                [Screensr] Enter selection (Default = Yes)>>>  """).lower()
                match close_option:
                    case ""|"1"|"Y"|"Yes":
                        break
                    case " "|"2"|"N"|"No":
                        run_scrcpy(["--audio-dup"])
                    case other:
                        print(f"\n\t[X] Invalid selection\n\tPlease enter a valid option on menu above\n")


    con_devices = adbutils.adb.device_list()
    if len(con_devices) == 0:
        print("\n")
        print(f"\n\t[No Device Connected]\n")
        time.sleep(0.8)
        print(f"\n\tChecking for connection ......\n")
        time.sleep(1.2)
        adb_connect.xconnect()
        time.sleep(1.2)
        con_devx = adbutils.adb.device_list()
        if len(con_devx) != 0:
            screencopykit()
    else:
        screencopykit()

def screencopy_anon():
    def screencopykit_anon():        
        print(f'\t[Info] Starting scrcpy  Anonymous......\n')
        time.sleep(0.5)
        try:
            run_scrcpy(["--turn-screen-off"])
        finally:
            close_option = input(f"""    
            [Do you Wish to exit : ]
            [1. Yes 2. No] \n
            [Screensr] Enter selection (Default = No)>>>  """).lower()
            match close_option:
                case ""|"1"|"Y"|"Yes":
                    time.sleep(0.25)
                    os.system("adb shell settings put global lock_sound null")
                    time.sleep(0.25)
                    os.system("adb shell input keyevent 26 2>/dev/null")
                    time.sleep(0.25)
                    os.system("adb shell input keyevent 224 2>/dev/null")
                case " "|"2"|"N"|"No":
                    run_scrcpy(["--turn-screen-off"])
                    os.system("adb shell settings put global lock_sound null")
                    time.sleep(0.25)
                    os.system("adb shell input keyevent 26 2>/dev/null")
                    time.sleep(0.95)
                    os.system("adb shell input keyevent 224 2>/dev/null")
                case other:
                    print(f"\n\t[X] Invalid selection\n\tPlease enter a valid option on menu above\n")


        
    con_devices = adbutils.adb.device_list()
    if len(con_devices) == 0:
        print("\n")
        print(f"\n\t[No Device Connected]\n")
        time.sleep(0.8)
        print(f"\n\tChecking for connection ......\n")
        time.sleep(1.2)
        adb_connect.xconnect()
        time.sleep(1.2)
        con_devx = adbutils.adb.device_list()
        if len(con_devx) != 0:
            screencopykit_anon()
    else:
        screencopykit_anon()


adb_command_center()