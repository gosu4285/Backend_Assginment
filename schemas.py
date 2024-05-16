from pydantic import BaseModel
from typing import Optional


class UrlInfo(BaseModel):
    original_url: str
    expired_period: Optional[int] = 0
