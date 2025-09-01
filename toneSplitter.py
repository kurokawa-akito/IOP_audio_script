import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sf
from pydub import AudioSegment
from pydub.silence import split_on_silence


class wavFileAnalysis:
    def __init__(self, audio_path):
        self.audio_path = audio_path

    def draw_waveform(self):
        y, sr = librosa.load(self.audio_path)

        # draw
        plt.figure()
        librosa.display.waveshow(y, sr=sr)
        plt.title('nutcracker waveform')
        plt.show()

# fast, but quality sounds strange
class librosaSplitter:
    def __init__(self, audio_path, top_db=30):
        self.audio_path = audio_path
        self.top_db = top_db

    def librosa_split(self):
        y, sr = librosa.load(self.audio_path, sr=None)

        intervals = librosa.effects.split(y, top_db=self.top_db)

        print(f'dectect {len(intervals)} voices')

        for i, (start, end) in enumerate(intervals):
            segment = y[start:end]
            output_filename = f'tone_segment_{i+1}.wav'
            sf.write(output_filename, segment, sr)
            print(f'saved: {output_filename}')

# slower than librosa, but quality sounds same as original tone
class pydubSplitter:
    def __init__(self, audio_path):
        self.audio_path = audio_path

    def pydub_split(self):
        sound = AudioSegment.from_wav(self.audio_path)

        chunks = split_on_silence(
            sound,
            min_silence_len=1000,      # silent threshold (ms)
            silence_thresh=sound.dBFS - 16,  # silent threshold (dB)
            keep_silence=200           # ms
        )

        for i, chunk in enumerate(chunks):
            out_file = f'pydub_segment_{i+1}.wav'
            chunk.export(out_file, format='wav')
            print(f'save as: {out_file}')

def main():
    # splitter = pydubSplitter('4min_96k_multitone.wav')
    # splitter.pydub_split()

    analyzer = wavFileAnalysis('4min_48k_multitone.wav')
    analyzer.draw_waveform()


if __name__ == "__main__":
    main()
