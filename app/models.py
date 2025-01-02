from pydantic import BaseModel
from typing import List

class CVData(BaseModel):
    name: str
    email: str
    phone: str
    skills: List[str]


class JobMatchResult(BaseModel):
    job_role: str
    required_skills: List[str]
    extracted_skills: List[str]
    missing_skills: List[str]
    additional_skills: List[str]
    match_percentage: float
