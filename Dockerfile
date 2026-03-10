FROM python:3.9
RUN apt-get update && apt-get install -y ffmpeg
WORKDIR /code
COPY . .
RUN pip install fastapi uvicorn yt-dlp openai-whisper
# Hugging Face MUST use port 7860
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]