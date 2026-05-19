from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

# Cau hinh ma hoa mat khau
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class DichVuBaoMat:
    @staticmethod
    def ma_hoa_mat_khau(mat_khau: str) -> str:
        """
        Ma hoa mat khau sang dang hash.
        :param mat_khau: Mat khau dang chu thuong
        :return: Mat khau da duoc hash
        """
        return pwd_context.hash(mat_khau)

    @staticmethod
    def xac_minh_mat_khau(mat_khau_goc: str, mat_khau_hash: str) -> bool:
        """
        Kiem tra mat khau nhap vao co khop voi hash khong.
        :param mat_khau_goc: Mat khau nguoi dung nhap
        :param mat_khau_hash: Mat khau hash trong database
        :return: True neu khop, False neu khong
        """
        return pwd_context.verify(mat_khau_goc, mat_khau_hash)

    @staticmethod
    def tao_token_truy_cap(data: dict, thoi_gian_het_han: timedelta = None):
        """
        Tao JWT Token de dang nhap.
        :param data: Du lieu can ma hoa vao token
        :param thoi_gian_het_han: Thoi gian het han cua token
        :return: Chuoi JWT Token
        """
        du_lieu_ma_hoa = data.copy()
        if thoi_gian_het_han:
            expire = datetime.utcnow() + thoi_gian_het_han
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.THOI_GIAN_TOKEN_PHUT)
        
        du_lieu_ma_hoa.update({"exp": expire})
        token_ma_hoa = jwt.encode(
            du_lieu_ma_hoa, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        return token_ma_hoa
