from pydantic import Field , BaseModel , EmailStr , field_validator
from app.shared.validators.password import password_validator
from app.shared.validators.phone_number import phone_number_validator
from app.authorization.roles import Role


class RequestCreateUser(BaseModel):
         
    first_name : str = Field( ..., min_length=2, max_length=50)

    last_name : str = Field( ..., min_length=2, max_length=50)
    
    username: str = Field( ..., min_length=3, max_length=50)
    
    email : EmailStr = Field( ...,)

    role : Role = Field(default='USER')
    
    password : str = Field( ...,)
    
    phone_number : str = Field( ..., min_length=10 , max_length=100)

    @field_validator("password")
    def validate_password(cls, value):
        return password_validator(value)

    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        return phone_number_validator(value)


class VerifyEmailRequest(BaseModel):
    token: str

class ResendEmailVerificationRequest(BaseModel):
    email: EmailStr

class RequestLoginUser(BaseModel):
    email: str
    password: str

class RequestForgotPassword(BaseModel):
    email: EmailStr

class RequestResetPassword(BaseModel):
    token: str
    new_password: str

    @field_validator("new_password")
    def validate_password(cls, value):
        return password_validator(value)