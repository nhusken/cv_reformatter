"""
Data models for CV information.
"""
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PersonalInfo:
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

@dataclass
class Experience:
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = None
    description: Optional[str] = None

@dataclass
class Education:
    institution: str
    degree: str
    field: str
    start_date: str
    end_date: Optional[str] = None
    grade: Optional[str] = None

@dataclass
class Skills:
    technical: List[str]
    soft: List[str]
    languages: List[str]

@dataclass
class CVData:
    personal_info: PersonalInfo
    experience: List[Experience]
    education: List[Education]
    skills: Skills
    summary: Optional[str] = None
