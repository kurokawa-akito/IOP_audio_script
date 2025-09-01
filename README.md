# IOP_audio_script
**Python 3.6 or higher.**  
```bash
pip install -r requirements.txt
```
## getSourceLinkKey.py
### Overview
This Python script automates the process of extracting Bluetooth link keys from an Android device using ADB (Android Debug Bridge). It performs a series of checks and operations to ensure successful retrieval of Bluetooth configuration data and extracts relevant information from bt_config.cong, such as MAC addresses of peer devices, link key and BLE LTK(if the device supports LEA).
### Features
- ✅ Checks if ADB is installed and available in the system path.
- ✅ Verifies if an Android device is connected and accessible via ADB.
- ✅ Attempts to gain root access on the connected device.
- ✅ Searches for the `bt_config.conf` file in multiple possible locations on the device.
- ✅ Pulls the configuration file to the local machine.
- ✅ Extracts active Bluetooth MAC addresses from the device.
- ✅ Parses the configuration file to retrieve link keys and other relevant data.
### Requirements
- Python 3.6 or higher (Python 3.12 is recommended)
- ADB installed and added to system PATH
- `colorama` Python package  
Install dependencies using pip:  
```bash
pip install colorama
```

## sourceCleanDisconnect.py
To be done
