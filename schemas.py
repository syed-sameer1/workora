from pydantic import BaseModel
from typing import List

class RegisterSchema(BaseModel):
    name: str
    email: str
    password: str
    experience: int
    education: str
    skills: List[str]

class LoginSchema(BaseModel):
    email: str
    password: str

class EditProfileSchema(BaseModel):
    experience: int
    education: str
    skills: List[str]
