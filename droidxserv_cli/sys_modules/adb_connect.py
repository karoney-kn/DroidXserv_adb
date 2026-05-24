import os
import sys
import json
import socket
import time
import subprocess
import nmap
import adbutils
import subprocess
from datetime import datetime
from pathlib import Path
from sys_modules import utils,color

ADB_LOG_FILE = Path("./config/sys_logs/adb_syslog.txt")
scanned_devices = Path("./config/json_files/net_devs.json")
#-------------------------------------------------------------------------#

####################### ADB Connection Section ############################

#-------------------------------------------------------------------------#
indent = " " * 4

def adb_connect_main():

    while True:
        menu=f"""    
        [{color.CYAN}99.{color.ORANGE} Clear screen                                      {color.CYAN}0.{color.ORANGE} Exit{color.WHITE}]
        {color.WHITE}[scan | connect | disconnect | devices | xdroid | clear | exit] \n
        {color.YELLOW}[Main Menu]{color.WHITE} Enter selection {color.GREEN}>>>{color.WHITE} """
        input_menu = utils.sf_spacing(menu)
        option = input(input_menu).lower()
        match option:
            case "0"|"exit":
                print(f'\n{indent}[Info] Exiting ADB Server.....\n\n', end='')
                time.sleep(1)
                break

            case "1"|"scan":
                network_scan()
            case "2"|"connect":
                xconnect()
            case "3"|"disconnect":
                main_disconnect()
            case "4"|"devices":
                main_list_devices()
            case other:
                print(f"\n{indent}{color.RED}[X] Invalid selection\n{indent}{color.YELLOW}Please enter a valid option on menu above\n")
                time.sleep(3)

#-------------------------------------------------------------------------#

####################### ADB Connection Section ############################

#-------------------------------------------------------------------------#

def xconnect():
    try:
        phone_ip = get_adb_android_ip("-d")
        start_debugging_server()
        if phone_ip is None:
            return
        connect_to_wireless(phone_ip)
    except:
        connect()

def write_log(message: str):
    ADB_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ADB_LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{timestamp}] {message}\n")

def run_adb_command(command: list[str]):
    write_log(f"EXECUTING: {' '.join(command)}")
    result = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    for line in result.stdout.splitlines():
        line = line.rstrip()
        if line:
            write_log(line)

    write_log(f"COMMAND FINISHED WITH CODE {result.returncode}")

    return result.returncode


#------------------------ Auto IP Selection ------------------------------#


def check_if_ip(possible_ip: str) -> bool:
    utils.clear_screen()
    print(utils.droid_connect_banner)
    ip_parts = possible_ip.split(".")
    try:
        [int(part) for part in ip_parts]
        if len(ip_parts) == 4:
            return True
    except:
        time.sleep(0.8)
        print(f"{indent}{color.CYAN}[Info]{color.WHITE} Auto Connect >> {color.RED}Failed ! {color.WHITE}>> No USB Connection\n")
        time.sleep(1.2)
        print(f"{indent}{color.GREEN}<< Going User input mode ")
        time.sleep(2.4)
    return False


def get_adb_android_ip(connection_type_flag: str | None = None):
    ip_args = ["adb"]
    if connection_type_flag is not None:
        ip_args += [connection_type_flag]
    ip_args += ["shell", "ip", "route"]
    ret = subprocess.run(ip_args, capture_output=True)  # only uses usb
    if "device unauthorized" in ret.stderr.decode():
        print("try pairing the device first")
        return
    possible_ip = ret.stdout.decode().strip().split(" ")[-1]
    is_ip = check_if_ip(possible_ip)
    if is_ip == True:
        return possible_ip
    else:
        raise ValueError

def connect_to_wireless(ip: str, port: str | int = "5555"):
    utils.clear_screen()
    print(utils.droid_connect_banner)
    port = str(port)
    if ip is None:
        return
    print(f"\n{indent}{color.CYAN}[Info]  {color.GREEN} Device Found >> {color.YELLOW}{ip}\n")
    run_adb_command(["adb", "kill-server"])
    run_adb_command(["adb", "start-server"])
    print(f'{indent}{color.CYAN}[Info] {color.YELLOW}Restarting adb server ......\n')
    time.sleep(0.8)
    print(f"{indent}{color.CYAN}[Info]{color.ORANGE} Connecting.....\n{color.WHITE}")
    time.sleep(1.2)
    run_adb_command(["adb", "connect", f"{ip}:{port}"])
    auto_con_devices = adbutils.adb.device_list()
    for d in auto_con_devices:
        auto_con_dev = d.serial
        if auto_con_dev.count(".") == 3:
            utils.display_main_menu()
            print(f"{indent}{color.ORANGE}[{color.GREEN}✔{color.ORANGE}] {color.WHITE}Connection Successfull\n")
            print(f'{indent}{color.CYAN}[Info]{color.ORANGE} Connected to{color.WHITE} {ip}{color.ORANGE} on port{color.WHITE} {port}{color.WHITE}\n')
            write_log(f"SUCCESSFULLY CONNECTED TO {ip}:{port}")
        else:
            utils.display_main_menu()
            print(f"{indent}{color.WHITE}[{color.RED}X{color.WHITE}]{color.ORANGE} Connection Failed{color.WHITE}")
            write_log(f"FAILED TO CONNECT TO {ip}:{port}")




def start_debugging_server():
    try:
        result = run_adb_command(["adb", "-d", "tcpip", "5555"],capture_output=True,text=True,check=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"COMMAND FAILED, maybe try pairing? Error: {e.stderr.strip()}")

#------------------------ User IP Selection ----------------------------------#


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def scan_network():
    net_devs_ip = {}
    count = 0
    print(f"\n{indent}{color.CYAN}[Info]{color.ORANGE} Scanning network ......{color.WHITE}\n")
    time.sleep(1.2)
    try:
        ip = get_ip_address()
        ip += "/24"
        scanner = nmap.PortScanner()
        scanner.scan(hosts=ip, arguments="-sn")
    
        for host in scanner.all_hosts():

            if scanner[host]["status"]["state"] == "up":

                try:
                    if len(scanner[host]["vendor"]) == 0:
                        socket.gethostbyaddr(host)[0]
                    else:
                        scanner[host]['vendor']
                        socket.gethostbyaddr(host)[0]
                except:
                    scanner[host]['vendor']
                count = count+1
                while True:
                    if count < 10:
                        net_devs_ip[count] = host
                        with open(scanned_devices, 'w') as f:
                            json.dump(net_devs_ip, f, indent=count)
                    break
    except:

        net_devs_ip = {"0": "0.0.0.0"}
        with open(scanned_devices, 'w') as f:
            json.dump(net_devs_ip, f)
        raise ConnectionError

    print("\n") 

def network_scanner():
    try:
        scan_network()
    except:
        time.sleep(1.2)
        print(f"\n{indent}{color.RED}Network is unreachable \n")
        time.sleep(1.2)
        try:
            print(f"\n{indent}{color.YELLOW}Retrying ......... \n")
            time.sleep(0.8)
            scan_network()

        except:
            time.sleep(1.2)
            print(f"\n{indent}{color.RED}Network is unreachable \n")
            time.sleep(1.2)
   
            try:
                print(f"\n{indent}{color.YELLOW}Retrying ......... \n")
                time.sleep(0.8)
                scan_network()
            except:
                time.sleep(1.2)
                print(f"\n{indent}{color.RED}Network is unreachable \n")
                time.sleep(1.2)
                print(f"""
                    \n{indent}{color.ORANGE}[Please Check your network connection before retrying]\n 
                    \n{indent}{color.GREEN}<< Going Back to Main Menu  \n
                    """)
                time.sleep(2.4)
                utils.display_main_menu()
                
def network_scan():
    network_scanner()
    utils.display_main_menu()
    with open(scanned_devices, 'r') as dev_ips:
        data = json.load(dev_ips)
        print(f"{indent}{color.WHITE}[{color.GREEN}+{color.WHITE}]{color.WHITE} Scanned Devices{color.WHITE}\n{indent}{'-'*40}\n")
        try:
            for dev_key in data:
                for dev_addr in [data[dev_key]]:
                    if dev_addr == "0.0.0.0":
                        print(f"{indent}{color.WHITE}[No Device Found]\n")
                    else:
                        raise ValueError
        except:
            for dev_key in data:
                for dev_addr in [data[dev_key]]:
                    print(f"{indent}{color.WHITE}[{color.GREEN}{dev_key}{color.WHITE}]{color.WHITE}. {color.YELLOW}{dev_addr}")
            print("\n")


def connect():
    network_scanner()
    utils.clear_screen()
    print(utils.droid_connect_banner)    
    with open(scanned_devices, 'r') as dev_ips:
        data = json.load(dev_ips)
        try:
            for key in data:
                for ip in [data[key]]:
                    if ip == "0.0.0.0":
                        print(f"{indent}{color.WHITE}[{color.GREEN}-{color.WHITE}]{color.WHITE} Scanned Devices{color.WHITE}\n{indent}{'-'*40}\n")
                        print(f"{indent}{indent}{color.WHITE}[No Device Found]\n")
                    else:
                        raise ValueError
        except:
            print(f"{indent}{color.WHITE}[{color.GREEN}+{color.WHITE}]{color.WHITE} Scanned Devices{color.WHITE}\n{indent}{'-'*40}\n")
            for key in data:
                for ip in [data[key]]:
                    print(f"{indent}{color.WHITE}[{color.GREEN}{key}{color.WHITE}]{color.WHITE}. {color.YELLOW}{ip}")
            print("\n")
            ip_input=input(f"{indent}{color.YELLOW}[IP-select]{color.WHITE} Enter selection {color.GREEN}>>>{color.WHITE}").lower()
            match ip_input:
                case ip_input:
                    try:
                        utils.clear_screen()
                        print(utils.droid_connect_banner) 
                        if data[ip_input].count(".") == 3:
                            print(f"{indent}{color.CYAN}[Info]{color.GREEN} Selected Device >> {color.YELLOW}{data[ip_input]}\n")
                            run_adb_command(["adb", "kill-server"])
                            run_adb_command(["adb", "start-server"])
                            print(f'{indent}{color.CYAN}[Info]{color.YELLOW} Restarting adb server ......\n')
                            time.sleep(0.8)
                            print(f'{indent}{color.CYAN}[Info]{color.ORANGE} Connecting.....\n')
                            time.sleep(1.2)
                            run_adb_command(["adb", "connect", f"{data[ip_input]}:{5555}"]) 
                            con_devices = adbutils.adb.device_list()
                            if len(con_devices) != 0: 
                                utils.clear_screen() 
                                time.sleep(0.8)
                                utils.display_main_menu()
                                print(f"\n{indent}{color.ORANGE}[{color.GREEN}✔{color.ORANGE}] {color.WHITE}Connection Successfull\n")
                                print(f'{indent}{color.CYAN}[Info]{color.ORANGE} Connected to{color.WHITE} {data[ip_input]}{color.ORANGE} on port{color.WHITE} 5555{color.WHITE}\n\n')
                            else:
                                utils.display_main_menu()
                                print(f"{indent}{color.WHITE}[{color.RED}X{color.WHITE}]{color.ORANGE} Connection Failed\n{color.WHITE}\n")  
                        else:
                            time.sleep(0.8)
                            print(f"\n{indent}{color.RED}Invalid IP Address\n{indent}{color.GREEN}<< Going back to Main Menu{color.WHITE}")
                    except:
                        if ip_input == '':
                            utils.display_main_menu()
                            time.sleep(0.8)
                            print(f"\n{indent}{color.ORANGE}Null Input | No selection made\n{indent}{color.GREEN}<< Going back to Main Menu{color.WHITE}")
                        else:
                            time.sleep(0.8)
                            utils.display_main_menu()
                            print(f"{indent}{color.WHITE}[{color.ORANGE}X{color.WHITE}]{color.ORANGE}{indent}Device IP Not Found\n{color.GREEN}{indent}<< Going back to Main Menu{color.WHITE}")


def list_devices():
    print(f"\n{indent}{color.CYAN}[Info]{color.ORANGE} Scanning for connected devices.....{color.WHITE}")
    time.sleep(1.2)
    adb_device_scanner()

def main_list_devices():
    utils.clear_screen()
    print(utils.droid_connect_banner)    
    print(f"\n{indent}{color.CYAN}[Info]{color.ORANGE} Scanning for connected devices.....{color.WHITE}")
    time.sleep(1.2)
    utils.display_main_menu()
    adb_device_scanner()
    

def adb_device_scanner():

    con_devices_list = adbutils.adb.device_list()
    if len(con_devices_list) == 0:
        print(f"\n{indent}{color.WHITE}[{color.GREEN}-{color.WHITE}]{color.WHITE} Connected Devices{color.WHITE}\n{indent}{'-'*40}\n")
        print(f"{indent}{indent}{color.WHITE}[No Device Found]\n")
    else:

        for d in con_devices_list:
            con_dev = d.serial
            net_device_info =f"""
            {color.YELLOW}Device            :{color.WHITE} {d.prop.device}
            {color.YELLOW}Serial ip:port    :{color.CYAN} {d.serial}
            {color.YELLOW}Device Model      :{color.WHITE} {d.prop.model}
            {color.YELLOW}Device Name       :{color.WHITE} {d.prop.name}
            """
            net_device_display = utils.sf_spacing(net_device_info)
            if con_dev.count(".") != 3:
                print(f"{indent}{color.WHITE}[{color.GREEN}+{color.WHITE}]{color.ORANGE} ADB USB Connection{color.WHITE}\n{indent}{'-'*40}")
                print(net_device_display)
            elif con_dev.count(".") == 3:
                print(f"\n{indent}{color.WHITE}[{color.GREEN}+{color.WHITE}]{color.ORANGE} ADB WiFi Connection {color.WHITE}\n{indent}{'-'*40}")
                print(net_device_display)

def disconnect():
    con_devices = adbutils.adb.device_list()    
    if len(con_devices) == 0:
        print(f"\n{indent}{color.WHITE}[No Device Connected]\n")
    else:
        try:
            run_adb_command(["adb", "disconnect"], capture_output=True)
            print(f'\n{indent}{color.CYAN}[Info]{color.YELLOW} Disconnecting ......\n')
            time.sleep(1.2)
            print(f"{indent}{color.CYAN}[Info]{color.WHITE} All Devices/Emulators Disconnected\n")
        except:
            print(f'\n{indent}{color.CYAN}[Info]{color.YELLOW}Error occured while trying to disconnect\n')


def main_disconnect():
    try:
        run_adb_command(["adb", "disconnect"], capture_output=True)
        utils.display_main_menu()        
        print(f'{indent}{color.CYAN}[Info]{color.YELLOW} Disconnecting ......\n')
        time.sleep(1.2)
        print(f"{indent}{color.CYAN}[Info]{color.WHITE} All Devices/Emulators Disconnected\n")
    except:
        print(e)
        utils.display_main_menu()
        print(f"{indent}{color.CYAN}[Info]{color.YELLOW}Error occured while trying to disconnect\n")  
