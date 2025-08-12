import subprocess
import os
import shutil
import re
from colorama import init, Fore, Style

init(autoreset=True)

class cleanDisconnect:
    def __init__(self):
        pass

    def log(self, level, message):
        color = {
            "SUCCESS": Fore.GREEN,
            "ERROR": Fore.RED,
            "WARNING": Fore.YELLOW,
            "CHECK": Fore.CYAN,
            "RESULT": Fore.MAGENTA,
            "FAILURE": Fore.RED
        }.get(level, Fore.WHITE)
        print(f"{color}[{level}]{Style.RESET_ALL} {message}")

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.log("SUCCESS", f"Executed command: {command}\nOutput:\n{result.stdout}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.log("ERROR", f"Failed to execute command: {command}\nError:\n{e.stderr.strip()}")
            return None

    def check_device_connected(self):
        output = self.run_command("adb devices")
        if output:
            lines = output.strip().splitlines()
            devices = [line for line in lines[1:] if "device" in line and not line.startswith("*")]
            if devices:
                self.log("CHECK", f"Connected devices: {devices}")
                return True
            else:
                self.log("WARNING", "No devices detected. Please ensure your device is connected and USB debugging is enabled.")
        return False

    def check_root_success(self):
        output = self.run_command("adb root")
        if output and ("adbd is already running as root" in output or "restarting adbd as root" in output):
            self.log("CHECK", "adb root succeeded.")
            return True
        else:
            self.log("ERROR", "adb root failed. Device may not support root or is not unlocked.")
            return False

    def parse_parcel_result(self, output):
        match = re.search(r'Parcel\((?:\s*[\da-fA-F]{8})+\s+\'(.*?)\'\)', output)
        if match:
            hex_values = re.findall(r'[\da-fA-F]{8}', output)
            if hex_values and hex_values[-1] == '00000001':
                return True
            elif hex_values and hex_values[-1] == '00000000':
                return False
        return None

    def disable_bluetooth(self):
        output = self.run_command("adb shell service call bluetooth_manager 8")
        result = self.parse_parcel_result(output) if output else None
        if result is True:
            self.log("RESULT", "Bluetooth disable command succeeded.")
        elif result is False:
            self.log("FAILURE", "Bluetooth disable command failed.")
        else:
            self.log("WARNING", "Unable to determine result of Bluetooth disable command.")

    def enable_bluetooth(self):
        output = self.run_command("adb shell service call bluetooth_manager 6")
        result = self.parse_parcel_result(output) if output else None
        if result is True:
            self.log("RESULT", "Bluetooth enable command succeeded.")
        elif result is False:
            self.log("FAILURE", "Bluetooth enable command failed.")
        else:
            self.log("WARNING", "Unable to determine result of Bluetooth enable command.")


    def launch_muzio_player(self):
        self.run_command("adb shell monkey -p com.shaiban.audioplayer.mplayer -c android.intent.category.LAUNCHER 1")

    def toggle_play_pause(self):
        self.run_command("adb shell input keyevent KEYCODE_MEDIA_PLAY_PAUSE")
