from pydantic import BaseModel

class BilingualMessage(BaseModel):
    en: str
    hi: str
