from pydantic import BaseModel, ConfigDict , Field , field_validator , model_validator
from fastapi.exceptions import HTTPException
from datetime import datetime

class LoginIn (BaseModel) : 
    username : str
    password : str


class UserOut(BaseModel):
    id: int
    username : str
    email: str

    model_config = ConfigDict(from_attributes=True)


class LoginOut (BaseModel) : 
    user:UserOut
    access:str
    refresh:str
    success:str


class SignupIn (BaseModel) : 

    username:str = Field(max_length= 300)
    password:str = Field(max_length= 250)
    confirm_password:str
    email:str
    @field_validator('password')
    @classmethod
    def validate_password(cls,v:str): 
        v=v.strip()
        if len(v) < 8: 
            raise ValueError('حداقل کاراکتر مجاز برای رمزعبور هشت تا می باشد')
        if not any(i.isdigit() for i in v): 
            raise ValueError('رمزعبور باید شامل اعداد باشد')
        if not any(i.isalpha() for i in v): 
            raise ValueError('رمزعبور باید شامل حروف باشد')
        if not any(i in ['#' , '@' , '!' , '&',  '*' , '$'] for i in v): 
            raise ValueError('رمزعبور باید شامل سمبل ها باشد')
        return v

    @model_validator(mode= 'after')
    def validate_passwords (self) : 

        if self.password != self.confirm_password : 
            raise ValueError('رمزعبور با تایید رمزعبور یکسان نمی باشد')
        
        return self
    

class SignupOut (BaseModel) : 
    id:int
    username:str
    model_config = ConfigDict(from_attributes= True)


class VerifySignupIN (BaseModel) : 

    code : int

class CreateUserOut (BaseModel) :

    id : int
    username : str
    email : str
    joined_at : datetime

    model_config = ConfigDict(from_attributes= True)


class VerifySignupOut (BaseModel) : 

    user : CreateUserOut
    success : str

    