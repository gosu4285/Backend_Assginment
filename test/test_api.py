from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from sql_app.database import Base
from sql_app import db_api

TEST_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app, follow_redirects=False)

_ORIGINAL_URL = "https://www.youtube.com/"
_SHORT_KEY = None


def test_create_short_url():
    global _SHORT_KEY
    request_data = {
        "original_url": _ORIGINAL_URL
    }
    response = client.post(url='/shorten', json=request_data)
    assert response.status_code == 200

    db = next(override_get_db())
    _SHORT_KEY = db_api.get_short_url(db, request_data["original_url"])
    assert response.json()["short_url"] == _SHORT_KEY


def test_create_short_url_duplication():
    request_data = {
        "original_url": _ORIGINAL_URL
    }
    response = client.post(url='/shorten', json=request_data)
    assert response.status_code == 200
    assert response.json()["short_url"] == _SHORT_KEY


def test_read_short_url():
    db = next(override_get_db())
    before_count = db_api.get_short_key_count(db, _SHORT_KEY)
    response = client.get(f'/{_SHORT_KEY}')

    assert response.status_code == 301
    after_count = db_api.get_short_key_count(db, _SHORT_KEY)
    assert after_count == before_count + 1


def test_read_short_url_not_exist_key():
    short_key = "ABCD"
    response = client.get(f'/{short_key}')
    assert response.status_code == 404


def test_get_short_key_read_count():
    db = next(override_get_db())
    short_key_read_count = db_api.get_short_key_count(db, _SHORT_KEY)

    response = client.get(f'/stats/{_SHORT_KEY}')
    assert response.status_code == 200
    assert response.json() == {"read_count": short_key_read_count}


def test_get_short_key_not_exist_key():
    short_key = "ABCD"
    response = client.get(f'/stats/{short_key}')
    assert response.status_code == 404
