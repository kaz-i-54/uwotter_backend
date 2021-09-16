from pydub import effects, AudioSegments

def match_target_amplitude(sound, target_dBFS):
    """振幅の平均をtarget_dBFSに合わせる関数"""
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def multi_mixing(raw_voice_list):
    """音声を合成する関数 wav形式以外はエラーとなる"""
    sound = AudioSegment.empty
    for raw_audio in raw_voice_list:
        try:
            sound_tmp = AudioSegment(data=raw_audio,
                                    sample_width=2,
                                    frame_rate=44100,
                                    channels=2)
            
            normalized_sound_tmp = match_target_amplitude(sound_tmp, -20.0)
            if normalized_sound_tmp.duration_seconds < sound.duration_seconds:
                sound = sound.overlay(normalized_sound_tmp, position=0)
            else:
                sound = normalized_sound_tmp.overlay(sound, position=0)
    
    return match_target_amplitude(sound)


def multi_mixing(raw_voice_list):
    """音声を合成する関数 wav形式以外はエラーとなる"""
    sound = AudioSegment.empty()
    
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
        except:
            print("data comming into multi_mixing is not wav format")
    return sound