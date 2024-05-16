from fastapi import FastAPI, Depends, HTTPException
from starlette.responses import RedirectResponse
import shortuuid
from sqlalchemy.orm import Session
from datetime import datetime as dt, timedelta

from sql_app import db_api, models
from sql_app.database import SessionLocal, engine
from schemas import UrlInfo

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/shorten")
def create_short_url(url_data: UrlInfo, db: Session = Depends(get_db)):
    short_url = db_api.get_short_url(db, url_data.original_url)
    if short_url is None:
        short_url = shortuuid.ShortUUID().random(length=7)
        expired_time = None
        if url_data.expired_period != 0:
            expired_time = dt.now() + timedelta(days=url_data.expired_period)
        db_api.insert_url_mapping(db, url_data.original_url, short_url, expired_time)
    return {"short_url": short_url}


@app.get("/{short_key}")
def read_short_url(short_key: str, db: Session = Depends(get_db)):
    orginal_url = db_api.get_original_url(db, short_key)
    if orginal_url is None:
        raise HTTPException(status_code=404, detail="original_url not exist")
    return RedirectResponse(url=orginal_url, status_code=301)


@app.get("/stats/{short_key}")
def get_short_key_read_count(short_key: str, db: Session = Depends(get_db)):
    read_count = db_api.get_short_key_count(db, short_key)
    if read_count is None:
        raise HTTPException(status_code=404, detail="short_key not exist")
    return {"read_count": read_count}
