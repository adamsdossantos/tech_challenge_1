from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class ActiveUser(BaseModel):
    username: str
    full_name: Optional[str] = None

    class Config:
        from_attributes = True

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int 
    
    class Config:
        env_file = ".env"

settings = Settings()