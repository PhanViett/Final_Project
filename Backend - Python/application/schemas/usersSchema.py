from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr


class LoginSchema(BaseModel):
    tai_khoan: str
    mat_khau: constr(min_length=8)