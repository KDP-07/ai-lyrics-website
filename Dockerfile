FROM python:3.9
RUN apt-get update && apt-get install -y ffmpeg
WORKDIR /code
COPY . .
RUN pip install fastapi uvicorn openai-whisper python-multipart
# Hugging Face MUST use port 7860