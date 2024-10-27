import random
import validators

from database import Database
from models import Url


def generate_short_code() -> str:
    return "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6))


def create_short_url(url: str, db: Database, retrie_count: int = 0) -> Url:
    short = generate_short_code()
    try:
        return db.create_short_url(url, short)
    except ValueError:
        if retrie_count > 50:
            raise ValueError("Could not generate a unique short code")
        return create_short_url(url, db, retrie_count + 1)

def validate_url(url: str) -> bool:
    return validators.url(url)