# IOP_audio_script
**Python 3.12 is recommended to install.**
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

## toneSplitter.py
### Overview
This Python script provides tools for analyzing and segmenting WAV audio files. It includes waveform visualization and two methods for silence-based segmentation using `librosa` and `pydub`. Each detected audio segment is saved as a separate WAV file.  

⚠️ **Note:** `pydub` is recommended to use.  
⚠️ **Note:** Although `librosa` offers fast segmentation, it may alter the audio quality due to internal processing and resampling. Therefore, it is **not recommended** for splitting audio files when preserving original sound quality is important.
### Features
- 📈 Visualize waveform of the audio file using `librosa.display`
- ✂️ Split audio into segments based on silence:
  - `librosaSplitter`: Fast segmentation using `librosa.effects.split`, but may alter audio quality
  - `pydubSplitter`: Slower segmentation using `pydub.silence.split_on_silence`, preserves original audio quality
### Requirements
- Python 3.6 or higher (Python 3.12 recommended)
- Required Python packages:
  - `numpy`
  - `matplotlib`
  - `librosa`
  - `soundfile`
  - `pydub`

Install dependencies using pip:  

```bash
pip install numpy matplotlib librosa soundfile pydub
```
## sourceCleanDisconnect.py
To be done
