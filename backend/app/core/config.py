import os
from dotenv import load_dotenv

load_dotenv()

class CauHinh:
    TEN_DU_AN: str = "Peach Store API"
    PHIEN_BAN: str = "1.0.0"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "bi_mat_mac_dinh_sieu_cap")
    ALGORITHM: str = "HS256"
    THOI_GIAN_TOKEN_PHUT: int = 60
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

settings = CauHinh()
