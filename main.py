from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, FileResponse
import librosa
import io
import tempfile
import os
import soundfile as sf

app = FastAPI()


@app.post("/half_mp3")
async def process_audio(file: UploadFile = File(...)):
    # Save the uploaded file on disk
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as audio_file:
        content = await file.read()
        audio_file.write(content)

    # Load the audio file using librosa
    audio, sr = librosa.load(file_path)

    # Split the audio file in half
    split_point = len(audio) // 2
    audio_first_half = audio[:split_point]

    # Save the first half of the audio file to disk
    new_file_path = f"uploads/{os.path.splitext(file.filename)[0]}_half{os.path.splitext(file.filename)[1]}"
    sf.write(new_file_path, audio_first_half, sr)

    # Return the new file to the user
    return FileResponse(new_file_path, media_type="audio/mpeg")
