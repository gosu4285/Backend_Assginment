from sqlalchemy import Column, Integer, String, DateTime

from sql_app.database import Base


class UrlMapping(Base):
    __tablename__ = "url_mapping"
    original_url = Column(String, primary_key=True, comment='원본 url')
    short_key = Column(String, nullable=False, comment='단축 url key')
    expired_time = Column(DateTime, nullable=True, comment='단축 url key 만료시간')
    count = Column(Integer, nullable=False, comment='url 조회 수')
