from fastapi import FastAPI, File, UploadFile
from starlette.responses import FileResponse, StreamingResponse

app = FastAPI()

@app.post("/upload_file")
async def upload_file(up_file: UploadFile):
    file = up_file.file
    filename = up_file.filename
    with open(f"lesson7/{filename}_1", "wb") as f:
        f.write(file.read())


@app.post("/uploads_file")
async def uploads_file(up_files: list[UploadFile]):
    for f in up_files:
        file = f.file
        filename = f.filename
        with open(f"lesson7/{filename}_1", "wb") as f:
            f.write(file.read())


@app.get('/get_file_local/{filename}')
async def get_file_local(filename: str):
    return FileResponse(filename)


def iterfile(filename: str):
    with open(filename, "rb") as f:
        while chunk :=f.read(1024*1024):
            yield chunk



@app.get('/get_file_stream/{filename}')
async def get_file_stream(filename: str):
    return StreamingResponse(iterfile("lesson7/"+filename), media_type="text/txt")