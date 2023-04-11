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
    # Create a temporary file to store the uploaded file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_audio_file:
        # Save the uploaded file to the temporary file
        content = await file.read()
        tmp_audio_file.write(content)

        # Load the audio file using librosa
        audio, sr = librosa.load(tmp_audio_file.name)

        # Split the audio file in half
        split_point = len(audio) // 2
        audio_first_half = audio[:split_point]

        # Create a temporary file to store the first half of the audio file
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".mp3"
        ) as tmp_audio_half_file:
            # Save the first half of the audio file to the temporary file
            sf.write(tmp_audio_half_file.name, audio_first_half, sr)

            # Return the new file to the user
            return FileResponse(tmp_audio_half_file.name, media_type="audio/mpeg")
