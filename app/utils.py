from app.models import CVData, JobMatchResult
from pdfminer.high_level import extract_text
import re


def parse_cv(file_path: str, required_skills_list: str) -> CVData:
    try:
        text = extract_text(file_path)

        # Extract email
        email = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+', text)
        email = email.group(0) if email else "Not found"

        # Extract phone number
        phone = re.search(r'\\+?[0-9]{10,15}', text)
        phone = phone.group(0) if phone else "Not found"

        # Extract skills (example keywords)
        skills = [skill for skill in required_skills_list if skill.lower() in text.lower()]

        return CVData(name="Unknown", email=email, phone=phone, skills=skills)
    except Exception as e:
        raise ValueError(f"Error parsing CV: {str(e)}")


def match_skills(job_role: str, required_skills: list[str], extracted_skills: list[str]) -> JobMatchResult:
    missing_skills = [skill for skill in required_skills if skill.lower() not in [s.lower() for s in extracted_skills]]
    additional_skills = [skill for skill in extracted_skills if skill.lower() not in [s.lower() for s in required_skills]]
    match_percentage = (len(required_skills) - len(missing_skills)) / len(required_skills) * 100 if required_skills else 0

    return JobMatchResult(
        job_role=job_role,
        required_skills=required_skills,
        extracted_skills=extracted_skills,
        missing_skills=missing_skills,
        additional_skills=additional_skills,
        match_percentage=round(match_percentage, 2)
    )
