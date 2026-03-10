# AI Lyrics Generator

A full-stack web application using **OpenAI Whisper AI** to transcribe YouTube audio into lyrics with high accuracy. 

## Live Features
- **AI Transcription:** Uses the Whisper small model for fast and accurate speech-to-text.
- **Modern UI:** Responsive design featuring **Glassmorphism** and CSS3 animations.
- **UX Focused:** Includes a loading spinner, real-time status updates, and a "Copy to Clipboard" feature.
- **Asynchronous Processing:** Built with **FastAPI** to handle long-running AI tasks without freezing the interface.

## Tech Stack
| Layer | Technology |
| :--- | :--- |
| **Frontend** | JavaScript (ES6+), CSS3 (Glassmorphism), HTML5 |
| **Backend** | Python, FastAPI, Uvicorn |
| **AI/ML** | OpenAI Whisper (ASR Model) |
| **Data** | yt-dlp, FFmpeg |

## How it Works
1. The user pastes a YouTube URL into the frontend.
2. The **FastAPI** backend receives the URL and uses **yt-dlp** to extract the audio.
3. The audio is processed by the **Whisper AI** model to generate text segments.
4. The backend sends the formatted lyrics back to the frontend as a JSON response.
5. The UI dynamically renders the lyrics and provides a "Copy" option.

## Local Setup
1. Clone the repository.
2. Install dependencies: `pip install fastapi uvicorn yt-dlp openai-whisper`.
3. Ensure **FFmpeg** is installed on your system.
4. Run the server: `uvicorn main:app --reload --port 8080`.
5. Open `index.html` in your browser.
