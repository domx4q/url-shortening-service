from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse

from database import Database
from functions import create_short_url, validate_url
from models import Stats, Url, UrlString

app = FastAPI()
db = Database("urls.db")


@app.get("/{shortCode}")
async def redirect(shortCode: str) -> RedirectResponse:
    try:
        url = db.get_short_url(shortCode)
        db.access_url(shortCode)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short code not found")
    return RedirectResponse(url.url)


@app.post("/shorten", status_code=status.HTTP_201_CREATED,
          responses={status.HTTP_400_BAD_REQUEST: {"description": "Invalid URL"}})
# we use a Pydantic model as a parameter to tell pydantic to validate the request body
async def shorten_url(url: UrlString) -> Url:
    url: str = url.url
    if not validate_url(url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL")
    try:
        return create_short_url(url, db)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL could not be shortened")


@app.get("/shorten/{shortCode}", status_code=status.HTTP_200_OK,
         responses={status.HTTP_404_NOT_FOUND: {"description": "Short code not found"}})
async def get_url(shortCode: str) -> Url:
    try:
        return db.get_short_url(shortCode)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short code not found")


@app.put("/shorten/{shortCode}", status_code=status.HTTP_200_OK,
         responses={status.HTTP_400_BAD_REQUEST: {"description": "Invalid URL"},
                    status.HTTP_404_NOT_FOUND  : {"description": "Short code not found"}})
async def update_url(shortCode: str, url: UrlString) -> Url:
    url: str = url.url
    if not validate_url(url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL")
    try:
        return db.update_short_url(shortCode, url)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short code not found")


@app.delete("/shorten/{shortCode}", status_code=status.HTTP_204_NO_CONTENT,
            responses={status.HTTP_404_NOT_FOUND: {"description": "Short code not found"}})
async def delete_url(shortCode: str) -> None:
    try:
        db.delete_short_url(shortCode)
        return
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short code not found")


@app.get("/shorten/{shortCode}/stats", status_code=status.HTTP_200_OK,
         responses={status.HTTP_404_NOT_FOUND: {"description": "Short code not found"}})
async def get_stats(shortCode: str) -> Stats:
    try:
        stats = db.get_stats(shortCode)
        return stats
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short code not found")
