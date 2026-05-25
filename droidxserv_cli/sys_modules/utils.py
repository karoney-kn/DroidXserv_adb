import os
import sys
import random
import subprocess
import platform
from sys_modules import color

#-------------------------------------------------------------------------#

################################ ToolKit Section ##############################

#-------------------------------------------------------------------------#



class banner:



    main_menu = f"""

    {color.ORANGE}[Menu]

    {color.WHITE}1. scan            -{color.GREEN} Scan Network for Devices             
    {color.WHITE}2. connect         -{color.GREEN} Connect a Device                             
    {color.WHITE}3. disconnect      -{color.GREEN} Disconnect All Devices           
    {color.WHITE}4. devices         -{color.GREEN} List Connected Devices
    {color.WHITE}5. xdroid          -{color.GREEN} Android adb command center{color.WHITE}


    {color.ORANGE}Usage:{color.WHITE} enter the number or type the name on the menu display
    {color.ORANGE}example:{color.WHITE} enter 1 or type scan - to scan devices on the network                                    
    """

    android_adb_command_menu = f"""

    {color.ORANGE}[Menu]

    {color.WHITE}1. scrcpy_noaudio       -{color.GREEN} Mirror the device using screencopy - no audio 
    {color.WHITE}2. scrcpy               -{color.GREEN} Mirror the device using screencopy
    {color.WHITE}3. scrcpy_anon          -{color.GREEN} Mirror the device using screencopy - anon    
    {color.WHITE}4. screensr             -{color.GREEN} Screen Shot/Recorder
    {color.WHITE}5. syscom               -{color.GREEN} Android system Commands {color.WHITE}          


    {color.ORANGE}Usage:{color.WHITE} enter the number or type the name on the menu display
    {color.ORANGE}example:{color.WHITE} enter 1 or type scrcpy - to use screencopy

    """

    screensr_menu = f"""

    {color.ORANGE}[Menu]

    {color.WHITE}1. screenshot      -{color.GREEN} Screen Shot menu
    {color.WHITE}2. recordscreen    -{color.GREEN} Screen Recorder Menu{color.WHITE}


    {color.ORANGE}Usage:{color.WHITE} enter the number or type the name on the menu display
    {color.ORANGE}example:{color.WHITE} enter 1 or type screenshot - for screenshot menu                                    
    """ 
    audio_menu = f"""
    {color.ORANGE}[Menu]

    {color.WHITE}1. r-audio-m       -{color.GREEN} Record Audio{color.YELLOW}(Mic)
    {color.WHITE}2. r-audio-d       -{color.GREEN} Record Audio{color.YELLOW}(Device)
    {color.WHITE}3. s-audio-m       -{color.GREEN} Sream Audio{color.YELLOW}(Mic)
    {color.WHITE}4. s-audio-d       -{color.GREEN} Sream Audio{color.YELLOW}(Device){color.WHITE}


    {color.ORANGE}Usage:{color.WHITE} enter the number or type the name on the menu display
    {color.ORANGE}example:{color.WHITE} enter 3 or type s-audio-m - to stream audio via mic                                    
    """ 

    sys_action_menu = f"""
    {color.ORANGE}[Menu]

    {color.WHITE}1. shell           -{color.GREEN} android shell                  
    {color.WHITE}2. lock            -{color.GREEN} Lock device                               
    {color.WHITE}3. unlock          -{color.GREEN} Unlock Devices                   
    {color.WHITE}4. rebootmenu      -{color.GREEN} Reboot Menu                
    {color.WHITE}5. device-info     -{color.GREEN} Device info 
    {color.WHITE}6. battery-info    -{color.GREEN} Battery info
    {color.WHITE}7. power-off       -{color.GREEN} Power off {color.WHITE}


    {color.ORANGE}Usage:{color.WHITE} enter the number or type the name on the menu display
    {color.ORANGE}example:{color.WHITE} enter 2 or type lock - to lock the device/emulator                                   
    """ 

    reboot_menu = f"""
    {color.ORANGE}[Menu]

    {color.WHITE}1. s-reboot        -{color.GREEN} System reboot                  
    {color.WHITE}2. a-reboot        -{color.GREEN} Advanced reboot{color.WHITE}                              
    """ 
    android_screenshot_menu = f"""
    {color.ORANGE}[Menu]

    {color.WHITE}1. s-shot          -{color.GREEN} Normal Screen shot                               
    {color.WHITE}2. anon-s-shot     -{color.GREEN} Anonymous screenshot


    {color.ORANGE}Usage:{color.WHITE} enter the number or type the name on the menu display
    {color.ORANGE}example:{color.WHITE} enter 1 or type s-shot - to take screenshot                                     
    """

    android_screenrecord_menu = f"""
    {color.ORANGE}[Menu]

    {color.WHITE}1. s-record          -{color.GREEN} Normal screen recorder                              
    {color.WHITE}2. anon-s-record     -{color.GREEN} Anonymous screen recorder{color.WHITE}


    {color.ORANGE}Usage:{color.WHITE} enter the number or type the name on the menu display
    {color.ORANGE}example:{color.WHITE} enter 1 or type s-record - to record screen                                     
    """



    droidxserv_start = f"""

    █▀▄ █▀█ █▀█ █ █▀▄    
    █▄▀ █▀▄ █▄█ █ █▄▀ \033[33m</ToolKit >

    ┌══════════════════════════════════════════════════════════┐
    █                                                          █
    █    |X serv       >>>>                                    █
    █                                                          █
    └══════════════════════════════════════════════════════════┘

    \033[37m[X] Multipurpose ADB Toolkit  [X]
    \033[97m     
    """

    droid_toolkit = f"""

    ▄▀█ █▄░█ █▀▄ █▀█ █▀█ █ █▀▄    
    █▀█ █░▀█ █▄▀ █▀▄ █▄█ █ █▄▀ \033[33m</ToolKit >


                    █▀▄▀█ ▄▀█ █ █▄░█ ░ █▀▄▀█
                [X] █ ▀ █ █▀█ █ █░▀█ ▀ █ ▀ █enu

    ┌══════════════════════════════════════════════════════════┐
    █                                                          █
    █    |Main Menu    >>>>                                    █
    █                                                          █
    └══════════════════════════════════════════════════════════┘

    \033[37m[X] Multipurpose ADB Toolkit  [X]
    \033[36m[✔] DroidXserv \033[92m [✔] Version 1.0 [✔]
    \033[91m[!] Disclaimer [!]\033[33m For Educational Purpose only
    \033[97m     
    """
    android_adb_command = f"""

    ▄▀█ █▄░█ █▀▄ █▀█ █▀█ █ █▀▄    
    █▀█ █░▀█ █▄▀ █▀▄ █▄█ █ █▄▀ \033[33m</ToolKit >


                    █▀ █▀█ █▀▄▀█ ▄▀█ █▄░█ █▀▄
                [X] █▄ █▄█ █ ▀ █ █▀█ █░▀█ █▄▀ Center

    ┌══════════════════════════════════════════════════════════┐
    █                                                          █
    █    |ADB Command Center    >>>>                           █
    █                                                          █
    └══════════════════════════════════════════════════════════┘

    \033[37m[X] Multipurpose ADB Toolkit  [X]
    \033[36m[✔] DroidXserv \033[92m [✔] Version 1.0 [✔]
    \033[91m[!] Disclaimer [!]\033[33m For Educational Purpose only
    \033[97m     
    """


    android_reboot = f"""

    ▄▀█ █▄░█ █▀▄ █▀█ █▀█ █ █▀▄    
    █▀█ █░▀█ █▄▀ █▀▄ █▄█ █ █▄▀ \033[33m</ToolKit >


                        █▀ ░ ▄▀█ ░ █▀█
                [X]     ▄█ ▀ █▀█ ▀ █▀▄

    ┌══════════════════════════════════════════════════════════┐
    █                                                          █
    █    |System/Advanced Reboot    >>>>                       █
    █                                                          █
    └══════════════════════════════════════════════════════════┘

    \033[37m[X] Multipurpose ADB Toolkit  [X]
    \033[36m[✔] DroidXserv \033[92m [✔] Version 1.0 [✔]
    \033[91m[!] Disclaimer [!]\033[33m For Educational Purpose only
    \033[97m     
    """



    android_connect = f"""

    ▄▀█ █▄░█ █▀▄ █▀█ █▀█ █ █▀▄    
    █▀█ █░▀█ █▄▀ █▀▄ █▄█ █ █▄▀ \033[33m</ToolKit >


                        █▀ █▀█ █▄░█ █▄░█
                [X]     █▄ █▄█ █░▀█ █░▀█ect

    ┌══════════════════════════════════════════════════════════┐
    █                                                          █
    █    |ADB Wireless Connect    >>>>                         █
    █                                                          █
    └══════════════════════════════════════════════════════════┘

    \033[37m[X] Multipurpose ADB Toolkit  [X]
    \033[36m[✔] DroidXserv \033[92m [✔] Version 1.0 [✔]
    \033[91m[!] Disclaimer [!]\033[33m For Educational Purpose only
    \033[97m     
    """

    android_devlist = f"""

    ▄▀█ █▄░█ █▀▄ █▀█ █▀█ █ █▀▄    
    █▀█ █░▀█ █▄▀ █▀▄ █▄█ █ █▄▀ \033[33m</ToolKit >


                    █▀▄░░ ░ █░ █ █▀ ▀█▀
                [X] █▄▀ev ▀ █▄ █ ▄█ ░█░

    ┌══════════════════════════════════════════════════════════┐
    █                                                          █
    █    |Connected USB/Wireless Device List    >>>>           █
    █                                                          █
    └══════════════════════════════════════════════════════════┘

    \033[37m[X] Multipurpose ADB Toolkit  [X]
    \033[36m[✔] DroidXserv \033[92m [✔] Version 1.0 [✔]
    \033[91m[!] Disclaimer [!]\033[33m For Educational Purpose only
    \033[97m     
    """



    android_scrcpy = f"""

    ▄▀█ █▄░█ █▀▄ █▀█ █▀█ █ █▀▄    
    █▀█ █░▀█ █▄▀ █▀▄ █▄█ █ █▄▀ \033[33m</ToolKit >


            █▀ █▀ █▀█ █▀ █▀█ █ █
            ▄█ █▄ █▀▄ █▄ █▀▀ █▀
    """

    android_sys = f"""

    ▄▀█ █▄░█ █▀▄ █▀█ █▀█ █ █▀▄    
    █▀█ █░▀█ █▄▀ █▀▄ █▄█ █ █▄▀ \033[33m</ToolKit >


                        █▀ █ █ █▀
                [X]     ▄█ █▀  ▄█tem

    ┌══════════════════════════════════════════════════════════┐
    █                                                          █
    █    |ADB System Commands    >>>>                          █
    █                                                          █
    └══════════════════════════════════════════════════════════┘

    \033[37m[X] Multipurpose ADB Toolkit  [X]
    \033[36m[✔] DroidXserv \033[92m [✔] Version 1.0 [✔]
    \033[91m[!] Disclaimer [!]\033[33m For Educational Purpose only
    \033[97m     
    """
    android_nav = f"""

    ▄▀█ █▄░█ █▀▄ █▀█ █▀█ █ █▀▄    
    █▀█ █░▀█ █▄▀ █▀▄ █▄█ █ █▄▀ \033[33m</ToolKit >


                        █▄░█ ▄▀█ █  █
                        █░▀█ █▀█ ▀▄▀ igation

    ┌══════════════════════════════════════════════════════════┐
    █                                                          █
    █    |Scrcpy ADB Navigation    >>>>                        █
    █                                                          █
    └══════════════════════════════════════════════════════════┘

    \033[37m[X] Multipurpose ADB Toolkit  [X]
    \033[36m[✔] DroidXserv \033[92m [✔] Version 1.0 [✔]
    \033[91m[!] Disclaimer [!]\033[33m For Educational Purpose only
    \033[97m     
    """
    android_screensr = f"""

    ▄▀█ █▄░█ █▀▄ █▀█ █▀█ █ █▀▄    
    █▀█ █░▀█ █▄▀ █▀▄ █▄█ █ █▄▀ \033[33m</ToolKit >


                        █▀ █▀ █▀█ ░ █▀ ░ █▀█
                [X]     ▄█ █▄ █▀▄ ▀ ▄█ ▀ █▀▄


    ┌══════════════════════════════════════════════════════════┐
    █                                                          █
    █    |ADB Screen Shot/Record    >>>>                       █
    █                                                          █
    └══════════════════════════════════════════════════════════┘

    \033[37m[X] Multipurpose ADB Toolkit  [X]
    \033[36m[✔] DroidXserv \033[92m [✔] Version 1.0 [✔]
    \033[91m[!] Disclaimer [!]\033[33m For Educational Purpose only
    \033[97m     
    """
    android_screenshot = f"""

    ▄▀█ █▄░█ █▀▄ █▀█ █▀█ █ █▀▄    
    █▀█ █░▀█ █▄▀ █▀▄ █▄█ █ █▄▀ \033[33m</ToolKit >


                        █▀ █▀ █▀█ ░ █▀
                [X]     ▄█ █▄ █▀▄ ▀ ▄█hot

    ┌══════════════════════════════════════════════════════════┐
    █                                                          █
    █    |Screen Shot    >>>>                                  █
    █                                                          █
    └══════════════════════════════════════════════════════════┘

    \033[37m[X] Multipurpose ADB Toolkit  [X]
    \033[36m[✔] DroidXserv \033[92m [✔] Version 1.0 [✔]
    \033[91m[!] Disclaimer [!]\033[33m For Educational Purpose only
    \033[97m     
    """
    android_screenrecorder = f"""

    ▄▀█ █▄░█ █▀▄ █▀█ █▀█ █ █▀▄    
    █▀█ █░▀█ █▄▀ █▀▄ █▄█ █ █▄▀ \033[33m</ToolKit >


                        █▀ █▀ █▀█ ░ █▀█
                [X]     ▄█ █▄ █▀▄ ▀ █▀▄ecorder

    ┌══════════════════════════════════════════════════════════┐
    █                                                          █
    █    |Screen Recorder    >>>>                              █
    █                                                          █
    └══════════════════════════════════════════════════════════┘

    \033[37m[X] Multipurpose ADB Toolkit  [X]
    \033[36m[✔] DroidXserv \033[92m [✔] Version 1.0 [✔]
    \033[91m[!] Disclaimer [!]\033[33m For Educational Purpose only
    \033[97m     
    """
    android_audio_kit = f"""

    ▄▀█ █▄░█ █▀▄ █▀█ █▀█ █ █▀▄    
    █▀█ █░▀█ █▄▀ █▀▄ █▄█ █ █▄▀ \033[33m</ToolKit >


                    ▄▀█ █ █ █▀▄ █ █▀█
            [X]     █▀█ █▄█ █▄▀ █ █▄█ Kit

    ┌══════════════════════════════════════════════════════════┐
    █                                                          █
    █    |Audio Recorder    >>>>                               █
    █                                                          █
    └══════════════════════════════════════════════════════════┘

    \033[37m[X] Multipurpose ADB Toolkit  [X]
    \033[36m[✔] DroidXserv \033[92m [✔] Version 1.0 [✔]
    \033[91m[!] Disclaimer [!]\033[33m For Educational Purpose only
    \033[97m     
    """
    android_audio_recorder = f"""

    ▄▀█ █▄░█ █▀▄ █▀█ █▀█ █ █▀▄    
    █▀█ █░▀█ █▄▀ █▀▄ █▄█ █ █▄▀ \033[33m</ToolKit >


                ▄▀█ █ █ █▀▄ █ █▀█ ░ █▀█
            [X] █▀█ █▄█ █▄▀ █ █▄█ ▀ █▀▄ecorder

    ┌══════════════════════════════════════════════════════════┐
    █                                                          █
    █    |Audio Recorder    >>>>                               █
    █                                                          █
    └══════════════════════════════════════════════════════════┘

    \033[37m[X] Multipurpose ADB Toolkit  [X]
    \033[36m[✔] DroidXserv \033[92m [✔] Version 1.0 [✔]
    \033[91m[!] Disclaimer [!]\033[33m For Educational Purpose only
    \033[97m     
    """
    android_audio_stream = f"""

    ▄▀█ █▄░█ █▀▄ █▀█ █▀█ █ █▀▄    
    █▀█ █░▀█ █▄▀ █▀▄ █▄█ █ █▄▀ \033[33m</ToolKit >


                ▄▀█ █ █ █▀▄ █ █▀█ ░ █▀
            [X] █▀█ █▄█ █▄▀ █ █▄█ ▀ ▄█tream

    ┌══════════════════════════════════════════════════════════┐
    █                                                          █
    █    |Audio Stream    >>>>                                 █
    █                                                          █
    └══════════════════════════════════════════════════════════┘

    \033[37m[X] Multipurpose ADB Toolkit  [X]
    \033[36m[✔] DroidXserv \033[92m [✔] Version 1.0 [✔]
    \033[91m[!] Disclaimer [!]\033[33m For Educational Purpose only
    \033[97m     
    """


#-------------------------------------------------------------------------#

################################ ToolKit Section ##############################

#-------------------------------------------------------------------------#
indent = " " * 4
def sf_spacing(content: str):
    tabbed_content = f'\n{indent}'.join(line.lstrip() for line in content.splitlines())
    return tabbed_content


starting_droidxserv = random.choice(color.color_list) + banner.droidxserv_start
main_banner = random.choice(color.color_list) + banner.droid_toolkit
droid_adb_command = random.choice(color.color_list) + banner.android_adb_command
droidx_connect_banner = random.choice(color.color_list) + banner.android_connect
droid_devlist_banner = random.choice(color.color_list) + banner.android_devlist
droidx_scrcpy_banner = random.choice(color.color_list) + banner.android_scrcpy
droid_sys_banner = random.choice(color.color_list) + banner.android_sys
droid_nav_banner = random.choice(color.color_list) + banner.android_nav
droid_screensr_banner = random.choice(color.color_list) + banner.android_screensr
droid_screenshot_banner = random.choice(color.color_list) + banner.android_screenshot
droid_screenrecorder_banner = random.choice(color.color_list) + banner.android_screenrecorder
droid_reboot_banner = random.choice(color.color_list) + banner.android_reboot
droid_audio_kit = random.choice(color.color_list) + banner.android_audio_kit
droid_audio_recorder = random.choice(color.color_list) + banner.android_audio_recorder
droid_audio_stream = random.choice(color.color_list) + banner.android_audio_stream



def clear_screen():
    os_name = platform.system().lower()
    if os_name == "windows":
        command = ["cls"]
    else:
        command = ["clear"]
    subprocess.run(command, shell=False)


"""Displays banner and menu"""
def banner_display(menu_item:str):
    clear_screen()
    print(menu_item)

def droid_scrcpy_banner():
    clear_screen()
    print(droidx_scrcpy_banner)

def starting_droidxserv_banner():
    clear_screen()
    print(starting_droidxserv)

def droid_connect_banner():

    clear_screen()
    print(droidx_connect_banner)

def screensr_menu():

    clear_screen()
    print(droid_screensr_banner,banner.screensr_menu)
def droid_adb_command_menu():
    clear_screen()
    print(droid_adb_command,banner.android_adb_command_menu)

def droid_sys_menu():

    clear_screen()
    print(droid_sys_banner,banner.sys_action_menu)

def droid_screenshot_menu():
    clear_screen()
    print(droid_screenshot_banner,banner.android_screenshot_menu)

def droid_screenrecorder_menu():
    clear_screen()
    print(droid_screenrecorder_banner,banner.android_screenrecord_menu)

def droid_reboot_menu():
    """Displays banner and menu"""
    clear_screen()
    print(droid_reboot_banner,banner.reboot_menu)

def display_main_menu():
    """Displays banner and menu"""
    clear_screen()
    print(main_banner,banner.main_menu)


def clear_screen_main():
    """Clears the screen and display menu"""
    clear_screen()
    display_main_menu()
