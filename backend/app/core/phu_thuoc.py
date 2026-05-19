from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.models.nguoidung import NguoiDung

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/xac-thuc/dang-nhap")

def lay_nguoi_dung_hien_tai(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    chuoi_loi_xac_thuc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Khong the xac minh thong tin dang nhap",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise chuoi_loi_xac_thuc
    except JWTError:
        raise chuoi_loi_xac_thuc
        
    nguoi_dung = db.query(NguoiDung).filter(NguoiDung.email == email).first()
    if nguoi_dung is None:
        raise chuoi_loi_xac_thuc
    return nguoi_dung
