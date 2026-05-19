import sys
import os
sys.path.append(os.getcwd())

from app.core.database import SessionLocal
from app.models.nguoidung import NguoiDung

db = SessionLocal()
try:
    users = db.query(NguoiDung).all()
    for u in users:
        print(f"ID: {u.id} | ho_ten: {repr(u.ho_ten)} | email: {repr(u.email)} | so_dien_thoai: {repr(u.so_dien_thoai)} | dia_chi: {repr(u.dia_chi)}")
finally:
    db.close()
