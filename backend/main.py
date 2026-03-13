from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import yt_dlp
import whisper
import os

# Create app
app = FastAPI()

# Security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTML file location
@app.get("/")
async def read_index():
    # Make sure this matches exactly where your index.html lives!
    return FileResponse('frontend/index.html')

# load the AI model
print("Loading AI Model...")
model = whisper.load_model("small")

# The AI endpoint
@app.get("/generate")
def get_lyrics(url: str):
    # Downloader settings
    options = {
        'format': 'bestaudio/best',
        'outtmpl': 'song_to_transcribe', # saves the file as 'song_to_transcribe.mp3'
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'keepvideo': False,
        'source_address': '0.0.0.0'  
    }

    # Starts the download
    print(f"Downloading from: {url}")
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

    # Starts the AI transcription
    print("AI is now transcribing... please wait.")
    result = model.transcribe("song_to_transcribe.mp3", initial_prompt="These are song lyrics with verse and chorus.")

    # Cleans up the text
    lyrics_with_breaks = ""
    for segment in result['segments']:
        lyrics_with_breaks += segment['text'].strip() + "\n"

    # Sends it back to the website
    print("Done! Sending lyrics to the website.")
    return {"lyrics": lyrics_with_breaks}