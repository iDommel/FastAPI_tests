from fastapi import FastAPI, File, UploadFile
from pydub import AudioSegment, exceptions
from io import BytesIO

app = FastAPI()

@app.post("/process_audio")
async def process_audio(file: UploadFile = File(...)):
    try:
        # Read the file content into memory
        content = await file.read()

        # Load the audio file from memory using pydub
        audio = AudioSegment.from_file(BytesIO(content))

        # Apply some basic editing (e.g. reverse the audio)
        edited_audio = audio.reverse()

        # Write the edited audio file to memory
        output = BytesIO()
        edited_audio.export(output, format="mp3")

        # Return the edited audio file as a response
        return output.getvalue()
    except FileNotFoundError:
        return {"message": "The file was not found."}
    except exceptions.CouldntDecodeError:
        return {"message": "The audio file could not be decoded. Please check the file format and try again."}
    except Exception as e:
        print("Error:", e)
        print("Request payload:", file)
        return {"message": "Error processing audio file."}

@app.post("/identical_audio")
async def process_audio(file: UploadFile = File(...)):
    try:
        # Read the file content into memory
        print("reading file:", file);
        content = await file.read()
        # Return the original file as a streaming response
        return StreamingResponse(BytesIO(content), media_type=file.content_type)
    except Exception as e:
        print("Error:", e)
        print("Request payload:", file)
        return {"message": "Error processing audio file."}


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        mybytes = BytesIO(content)
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except FileNotFoundError:
        return {"message": "The file was not found."}
    except exceptions.CouldntDecodeError:
        return {"message": "The audio file could not be decoded. Please check the file format and try again."}
    except Exception as e:
        return {"message": "There was an error uploading the file"}
    finally:
        await file.close()