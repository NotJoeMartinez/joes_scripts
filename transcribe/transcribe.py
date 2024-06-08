import json
import os
import time
import logging
import sys
import json
from webvtt import WebVTT, Caption
from pathlib import Path
from rich.console import Console
from faster_whisper import WhisperModel

logging.getLogger("faster_whisper").setLevel(100)
console = Console()

def main():
    if (len(sys.argv) < 2):
        print("usage: transcribe [argv1]")
        exit()

    target_file = sys.argv[1]
    transcribe_audio(target_file)


def transcribe_audio(audio_file):
    model_size = "tiny.en"
    device = "cpu"
    compute_type = "int8"
    num_workers = 8
    cpu_threads = 4 if device == "cpu" else 0
    model = WhisperModel(model_size, 
                         device=device, 
                         compute_type=compute_type, 
                         num_workers=num_workers)

    ext = str(Path(audio_file).suffix)

    json_path = audio_file.replace(ext, ".json")
    vtt_path = json_path.replace(".json", ".en.vtt")


    if (os.path.exists(json_path)):
        print(f"json path exists: {json_path}")
        foo = input("overwrite? (y/n)")
        if foo.upper() != 'Y':
            exit()
        


    start_time = time.time()
    segments, info = model.transcribe(audio_file, 
                                        beam_size=5, 
                                        condition_on_previous_text=False, 
                                        language="en", 
                                        no_speech_threshold=2, 
                                        repetition_penalty=1.2)

    output  = {
                "text": "",
                "segments": []
            }

    for segment in segments:
        output["text"] += segment.text
        output["segments"].append({
            "id": segment.id,
            "text": segment.text,
            "start": segment.start,
            "end": segment.end,
        })

        print(f"{segment.start:.2f}: {segment.text}")

    end_time = time.time()

    console.print(f"Audio length: {info.duration:.2f}")
    console.print(f"Trascribe time: {end_time - start_time:.2f}")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f)
    
    json_to_vtt(json_path, vtt_path)
    

def json_to_vtt(json_file, vtt_file):
    with open(json_file, 'r') as jf:
        transcript = json.load(jf)

    vtt = WebVTT()
    for item in transcript["segments"]:
        start = seconds_to_timestamp(item['start'])
        end = seconds_to_timestamp(item['end'])
        text = item['text']
        caption = Caption(start, end, text)
        vtt.captions.append(caption)

    vtt.save(vtt_file)


def seconds_to_timestamp(seconds):
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60
    return f"{hours:02}:{minutes:02}:{seconds:06.3f}"

if __name__ == '__main__':
    main()