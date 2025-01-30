from fastapi import FastAPI, UploadFile, Form, HTTPException
from app.models import JobMatchResult
from app.utils import parse_cv, match_skills
import os
import shutil


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to ATS Scanner with FastAPI. A simple ATS scanner built with FastAPI to parse resumes/CVs and extract key information such as name, email, phone, and skills."}


@app.post("/upload_and_match", response_model=JobMatchResult)
async def upload_and_match(
    file: UploadFile,
    job_title: str = Form(...),
    required_skills: str = Form(...)
):
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # Parse required skills from comma-separated string
    required_skills_list = [skill.strip() for skill in required_skills.split(",")]

    upload_dir = "uploaded_files"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Parse CV and extract skills
        parsed_data = parse_cv(file_path, required_skills_list)

        # Match extracted skills with required skills
        result = match_skills(job_title, required_skills_list, parsed_data.skills)
        return result
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
