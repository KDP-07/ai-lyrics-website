from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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
    # removed 'frontend/' because it's no longer in a folder
    return FileResponse('index.html')

# load the AI model
print("Loading AI Model...")
model = whisper.load_model("small")

# The AI endpoint (Now accepts POST requests with Files)
@app.post("/generate")
async def get_lyrics(file: UploadFile = File(...)):
    print(f"Receiving file: {file.filename}")
    
    # 1. Save the uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 2. Run the AI transcription
    print("AI is now transcribing... please wait.")
    result = model.transcribe(temp_file_path, initial_prompt="These are song lyrics with verse and chorus.")

    # 3. Clean up the text formatting
    lyrics_with_breaks = ""
    for segment in result['segments']:
        lyrics_with_breaks += segment['text'].strip() + "\n"

    # 4. Delete the audio file so the server doesn't get full
    os.remove(temp_file_path)

    print("Done! Sending lyrics to the website.")
    return {"lyrics": lyrics_with_breaks}