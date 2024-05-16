from sqlalchemy.orm import Session
from datetime import datetime

from sql_app import models


def insert_url_mapping(db: Session, original_url: str, short_url: str, expired_time: datetime = None):
    db_url_mapping = models.UrlMapping(
        original_url=original_url,
        short_key=short_url,
        expired_time=expired_time,
        count=0
    )
    db.add(db_url_mapping)
    db.commit()
    db.refresh(db_url_mapping)


def get_original_url(db: Session, short_key: str):
    q = db.query(models.UrlMapping)\
          .filter(models.UrlMapping.short_key == short_key)\
          .first()
    if q is None:
        return None

    if q.expired_time is not None and q.expired_time < datetime.now():
        db.delete(q)
        db.commit()
        return None

    q.count += 1
    db.commit()
    return q.original_url


def get_short_url(db: Session, original_url: str):
    q = db.query(models.UrlMapping)\
          .filter(models.UrlMapping.original_url == original_url)\
          .first()
    if q is None:
        return None
    return q.short_key


def get_short_key_count(db: Session, short_key: str):
    q = db.query(models.UrlMapping)\
          .filter(models.UrlMapping.short_key == short_key)\
          .first()
    if q is None:
        return None
    return q.count
