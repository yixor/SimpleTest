from pydantic import BaseModel, Field, model_validator


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    login: str = Field(min_length=2, max_length=32)
    password: str = Field(min_length=8, max_length=64)
    password_repeat: str = Field(min_length=8, max_length=64)

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.password_repeat:
            raise ValueError("Passwords do not match")
        return self
