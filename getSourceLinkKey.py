import subprocess
import os
import shutil
import re
from colorama import init, Fore, Style

init(autoreset=True)

class ADBAutomation:
    def __init__(self):
        self.default_path = "/data/misc/bluedroid/bt_config.conf"
        self.alternative_paths = [
            "/data/vendor/bluedroid/bt_config.conf",
            "/data/misc/bluetooth/bt_config.conf",
            "/data/misc/bluetoothd/bt_config.conf"
        ]
        self.local_filename = "bt_config.conf"
        self.active_mac_suffixes = set()

    def log(self, level, message):
        color = {
            "SUCCESS": Fore.GREEN,
            "ERROR": Fore.RED,
            "WARNING": Fore.YELLOW,
            "CHECK": Fore.CYAN,
            "RESULT": Fore.MAGENTA,
            "FAILURE": Fore.RED,
            "FOUND": Fore.BLUE
        }.get(level, Fore.WHITE)
        print(f"{color}[{level}]{Style.RESET_ALL} {message}")

    def check_adb_installed(self):
        if not shutil.which("adb"):
            self.log("ERROR", "'adb' command not found. Please install Android Platform Tools and set up your environment.")
            return False
        return True

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

    def file_exists(self, path):
        output = self.run_command(f"adb shell ls {path}")
        return output and "No such file or directory" not in output

    def pull_bt_config(self):
        paths_to_try = [self.default_path] + self.alternative_paths
        for path in paths_to_try:
            self.log("CHECK", f"Trying path: {path}")
            if self.file_exists(path):
                self.log("FOUND", f"File exists at: {path}")
                result = self.run_command(f"adb pull {path}")
                if self.check_local_file():
                    return True
                else:
                    self.log("WARNING", "adb pull executed but file is invalid. Trying next path...")
        self.log("FAILURE", "bt_config.conf not found or pull failed.")
        return False

    def check_local_file(self):
        if os.path.exists(self.local_filename) and os.path.getsize(self.local_filename) > 0:
            self.log("SUCCESS", f"File '{self.local_filename}' successfully pulled. Size: {os.path.getsize(self.local_filename)} bytes.")
            return True
        else:
            self.log("FAILURE", f"File '{self.local_filename}' does not exist or is empty.")
            return False

    # def get_active_device_mac(self):
        # output = self.run_command("adb shell dumpsys bluetooth_manager | adb shell grep -i mActiveDevice")
        # if output:
        #     mac_matches = re.findall(r"\b([0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5})\b", output)
        #     if mac_matches:
        #         suffixes = {":".join(mac.split(":")[-2:]).lower() for mac in mac_matches}
        #         self.active_mac_suffixes = suffixes
        #         self.log("CHECK", f"Detected active Bluetooth MAC suffixes: {', '.join(suffixes)}")
        #         return True
        # self.log("FAILURE", "No active Bluetooth device MAC address found.")
        # return False
    def get_active_device_mac(self):
        output = self.run_command("adb shell dumpsys bluetooth_manager | adb shell grep -i mActiveDevice")
        # output = '  mActiveDevice: XX:XX:XX:XX:5B:9C\n  mActiveDevice: XX:XX:XX:XX:5B:9C\n'
        if output:
            cleaned_output = output.replace('\r', '').replace('\n', ' ') # move"\r"and"\n"
            self.log("DEBUG", f"Cleaned output: {cleaned_output}")

            mac_matches = re.findall(r"([0-9A-Za-z]{2}(?::[0-9A-Za-z]{2}){5})", cleaned_output)
            if mac_matches:
                suffixes = {":".join(mac.split(":")[-2:]).lower() for mac in mac_matches}
                self.active_mac_suffixes = suffixes
                self.log("CHECK", f"Detected active Bluetooth MAC suffixes: {', '.join(suffixes)}")
                return True
            else:
                self.log("DEBUG", "No MAC addresses matched in cleaned output.")
        else:
            self.log("DEBUG", "No output from adb command.")
            
        self.log("FAILURE", "No active Bluetooth device MAC address found.")
        return False

    def extract_link_key(self):
        if not os.path.exists(self.local_filename):
            self.log("ERROR", f"Local file '{self.local_filename}' not found.")
            return

        with open(self.local_filename, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.strip():
            self.log("ERROR", "bt_config.conf is empty.")
            return

        blocks = content.strip().split("\n\n")
        local_mac = None
        found = False

        for block in blocks:
            lines = block.strip().splitlines()
            if not lines:
                continue

            header = lines[0].strip()
            if header == "[Adapter]":
                for line in lines[1:]:
                    if line.startswith("Address = "):
                        local_mac = line.split("=", 1)[1].strip()
                        break
            elif re.match(r"\[[0-9A-Fa-f:]{17}\]", header):
                remote_mac = header.strip("[]").lower()
                suffix = ":".join(remote_mac.split(":")[-2:])
                if suffix in self.active_mac_suffixes:
                    name = None
                    link_key = None
                    le_key_lenc = None
                    for line in lines[1:]:
                        if line.startswith("Name = "):
                            name = line.split("=", 1)[1].strip()
                        elif line.startswith("LinkKey = "):
                            link_key = line.split("=", 1)[1].strip()
                        elif line.startswith("LE_KEY_LENC = "):
                            le_key_lenc = line.split("=", 1)[1].strip()

                    self.log("RESULT", f"Local MAC Address : {local_mac}")
                    self.log("RESULT", f"Remote MAC Address: {remote_mac}")
                    self.log("RESULT", f"Device Name       : {name}")
                    self.log("RESULT", f"LinkKey           : {link_key}")

                    if le_key_lenc:
                        trimmed = le_key_lenc[:-8] if len(le_key_lenc) >= 8 else le_key_lenc
                        self.log("RESULT", f"LE_KEY_LENC (trimmed): {trimmed}")
                    else:
                        self.log("RESULT", "LE_KEY_LENC not found.")

                    found = True

        if not found:
            self.log("FAILURE", "No LinkKey found matching any MAC suffix.")

    def execute_all(self):
        if not self.check_adb_installed():
            return
        if self.check_device_connected():
            if self.check_root_success():
                if self.get_active_device_mac():
                    if self.pull_bt_config():
                        self.extract_link_key()

if __name__ == "__main__":
    adb_tool = ADBAutomation()
    adb_tool.execute_all()
