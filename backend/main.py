from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import whisper
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading AI Model...")
model = whisper.load_model("small")

@app.get("/generate")
def get_lyrics(url: str):
    # 1. THE DOWNLOADER SETTINGS
    options = {
        'format': 'bestaudio/best',
        'outtmpl': 'song_to_transcribe', # saves the file as 'song_to_transcribe.mp3'
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'keepvideo': False,
    }

    # 2. START THE DOWNLOAD
    print(f"Downloading from: {url}")
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

    # 3. START THE AI TRANSCRIPTION
    print("AI is now transcribing... please wait.")
    # Point the AI to downloaded file
    result = model.transcribe("song_to_transcribe.mp3", initial_prompt="These are song lyrics with verse and chorus.")

    # 4. CLEAN UP THE TEXT
    lyrics_with_breaks = ""
    for segment in result['segments']:
        lyrics_with_breaks += segment['text'].strip() + "\n"

    # 5. SEND IT BACK TO THE WEBSITE
    print("Done! Sending lyrics to the website.")
    return {"lyrics": lyrics_with_breaks}