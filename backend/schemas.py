from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    password: str
    security_question: str
    security_answer: str

class UserLogin(BaseModel):
    username: str
    password: str

class ResetPassword(BaseModel):
    username: str
    security_answer: str
    new_password: str
