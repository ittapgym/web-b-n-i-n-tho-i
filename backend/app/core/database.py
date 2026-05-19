from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Lấy URL từ config
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

if not SQLALCHEMY_DATABASE_URL:
    print("[!] DATABASE_URL khong duoc cau hinh! Tam thoi su dung SQLite fallback de tranh crash.")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./peach_store_fallback.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Hàm lấy session database
def get_db():
    """Ham generator cung cap session ket noi database cho cac API"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
