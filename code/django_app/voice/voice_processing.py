from pydub import effects, AudioSegment
from scipy.io.wavfile import write
import tempfile
import numpy as np


def match_target_amplitude(sound, target_dBFS):
    """振幅の平均をtarget_dBFSに合わせる関数"""
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def multi_mixing(raw_voice_list):
    """音声を合成する関数 wav形式以外はエラーとなる"""
    """base64でエンコード前のwavのデータを返す"""
    sound = AudioSegment.empty()
    mixed_num = 0

    for raw_audio in raw_voice_list:
        try:
            sound_tmp = AudioSegment(data=raw_audio)
#         sound_tmp = AudioSegment(data=raw_audio,
#                                 sample_width=2,
#                                 frame_rate=44100,
#                                 channels=2)

            normalized_sound_tmp = match_target_amplitude(sound_tmp, -30.0)
            sound_tmp = normalized_sound_tmp
            if sound_tmp.duration_seconds < sound.duration_seconds:
                sound = sound.overlay(sound_tmp, position=0)
            else:
                sound = sound_tmp.overlay(sound, position=0)
            mixed_num += 1
        except:
            print("data comming into multi_mixing is not wav format")

    print(mixed_num, "件の音声データが合成されました")

    data = np.array(sound.get_array_of_samples())
    # wav形式に変換する
    fp = tempfile.TemporaryFile()
    write(fp, rate=84100, data=data)
    fp.seek(0)
    wav_data = fp.read()

    return wav_data
