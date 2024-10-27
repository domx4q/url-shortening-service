from datetime import datetime

from pydantic import BaseModel

class Url(BaseModel):
    id: int
    url: str
    shortCode: str
    createdAt: datetime
    updatedAt: datetime

class UrlString(BaseModel):
    url: str

    def __str__(self):
        return self.url

class Stats(Url):
    accessCount: int