from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

import speech_recognition as sr
import ffmpy3
import json
import os


def append_zero_time(time: float|int) -> str:
    if time < 10:
        time = f'0{time}'

    return str(time)


def time_filter(time: float|int) -> str:
    hours = int(time // 3600)
    minute = int(time // 60 % 60)
    seconds = int(time % 60)
    microseconds = str(round(time % 60 % 1, 3)).replace("0.", "")
    microseconds += '0' if len(microseconds) < 3 else ''

    hours = append_zero_time(hours)
    minute = append_zero_time(minute)
    seconds = append_zero_time(seconds)


    return f"{hours}:{minute}:{seconds}:{microseconds}"


def clear_folders(path: str):
    for file in os.listdir(path):
       os.remove(path+file)


def save_subs(name:str, data:dict):
    with open(f'{os.getenv("SUBS_PATH")}/{name}.vtt', 'w', encoding='UTF-8') as f:
        f.write("WEBVTT")

    for key in data.keys():
        text = f"\n\n{key}\n{time_filter(data[key]['time_start'])} --> {time_filter(data[key]['time_end'])}\n{data[key]['text']}"
        
        with open(f'{os.getenv("SUBS_PATH")}/{name}.vtt', 'a', encoding='UTF-8') as f:
            f.write(text)


def save_json(name:str, text:dict):
    with open(f'{os.getenv("JSON_PATH")}/{name}.json', 'w', encoding='UTF-8') as f:
        json.dump(text, f)


def detect_speech(file: str): 
    song = AudioSegment.from_wav(file)
    
    timestamp_list = detect_nonsilent(song, 500, song.dBFS*1.3, 1)
    text = {}

    for i in range(len(timestamp_list)):
        if i != len(timestamp_list)-1:
            text[i] = {
                "time_start": timestamp_list[i][0]/1000,
                "time_end": timestamp_list[i+1][0]/1000,
                "duration": timestamp_list[i+1][0]/1000 - timestamp_list[i][0]/1000,
                "text": audio_to_text_google(file, offset_start=timestamp_list[i][0]/1000, offset_end=timestamp_list[i+1][0]/1000)
            }
        else:
            text[i] = {
                "time_start": timestamp_list[i][0]/1000,
                "time_end": timestamp_list[i][1]/1000,
                "duration": timestamp_list[i][1]/1000 - timestamp_list[i][0]/1000,
                "text": audio_to_text_google(file, offset_start=timestamp_list[i][0]/1000, offset_end=None)
            }

    return text


def audio_to_text_google(path: str, offset_start: float|None=None, offset_end: float|None=0,  language:str = 'en-US') -> str:
    recog = sr.Recognizer()

    duration = offset_end - offset_start if offset_end else None

    if isinstance(duration, float|int) and duration < 1:
        duration = 1
    try:

        with sr.AudioFile(path) as audio_file:
            audio_content = recog.record(audio_file, offset=offset_start, duration=duration)

        return recog.recognize_google(audio_content, language=language)

    except:
        pass


def main():

    clear_folders(audio_path)
    clear_folders(os.getenv("SUBS_PATH"))
    clear_folders(os.getenv("JSON_PATH"))

    video_list = [file for file in os.listdir(video_path) if file.endswith(".mp4")]
    
    for video in video_list:
        ff = ffmpy3.FFmpeg (
            executable=os.getenv("FFMPEG_PATH"),
            inputs={f'{video_path}{video}': None},
            outputs={f'{audio_path}{video.rsplit(".",1)[0]}.wav': None}
        )

        ff.run()

        data = detect_speech(f'{audio_path}{video.rsplit(".",1)[0]}.wav')
        save_json(f'{video.rsplit(".",1)[0]}', data)
        save_subs(f'{video.rsplit(".",1)[0]}', data)
    

if __name__ == "__main__":
    try:
        load_dotenv()

        video_path = os.getenv("VIDEO_PATH")
        audio_path = os.getenv("AUDIO_PATH")
        main()
        
    except (KeyboardInterrupt, SystemExit):
        print("[#] Произошла не предвиненная ошибка")
