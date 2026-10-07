from pathlib import Path
import shutil

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

from .resume_parser import extract_text
from .rag_engine import ask_question

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

class Question(BaseModel):
    question: str

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    path = UPLOADS_DIR / file.filename

    with path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text(str(path))

    return {
        "content": text[:500]
    }

@app.post("/ask")
def ask(data: Question):

    answer = ask_question(
        data.question
    )

    return {
        "answer": answer
    }
