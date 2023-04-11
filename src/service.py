from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import uvicorn
import librosa
import tempfile
import soundfile as sf
import logging
from midiutil import MIDIFile


class Service:
    def __init__(
        self,
        service_host: str,
        service_port: int,
    ):
        self.service_host = service_host
        self.service_port = service_port
        self.app = FastAPI()
        self.app.on_event("shutdown")(self.close)

        # Initialize the routes
        self.app.post("/half_mp3")(self.process_audio)
        self.app.get("/midi")(self.generate_midi)
        self.app.get("/")(self.read_root)

    def run(self):
        config = uvicorn.Config(
            app=self.app,
            host=self.service_host,
            port=self.service_port,
        )
        server = uvicorn.Server(config)
        server.run()

    async def close(self):
        """Gracefull shutdown."""
        logging.warning("Shutting down the app.")

    async def read_root(self):
        """Read the root."""
        return {"Hello": "World"}

    async def process_audio(self, file: UploadFile = File(...)):
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

    async def generate_midi(self):
        with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as temp_file:
            # create a MIDIFile object with one track
            midi_file = MIDIFile(1)

            # set the tempo (in BPM)
            midi_file.addTempo(0, 0, 120)

            # add some notes to the track
            channel = 0
            time = 0
            for pitch in [60, 62, 64, 65, 67, 69, 71, 72]:
                duration = 1
                midi_file.addNote(channel, channel, pitch, time, duration, 100)
                time += 1

            # write the MIDI file to the temporary file
            midi_file.writeFile(temp_file)

            # read the MIDI file as bytes
            temp_file.seek(0)
            return FileResponse(temp_file.name, media_type="audio/midi")
