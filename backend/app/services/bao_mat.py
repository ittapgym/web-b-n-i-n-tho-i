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
        Mã hóa mật khẩu dạng văn bản thô sang dạng chuỗi băm (hash) bảo mật bằng bcrypt.

        Args:
            mat_khau (str): Mật khẩu gốc dạng chữ thường.

        Returns:
            str: Chuỗi mật khẩu đã được mã hóa bảo mật.
        """
        return pwd_context.hash(mat_khau)

    @staticmethod
    def xac_minh_mat_khau(mat_khau_goc: str, mat_khau_hash: str) -> bool:
        """
        Xác minh đối chiếu xem mật khẩu người dùng nhập vào có khớp với chuỗi băm lưu trong cơ sở dữ liệu hay không.

        Args:
            mat_khau_goc (str): Mật khẩu thô do người dùng nhập.
            mat_khau_hash (str): Chuỗi mật khẩu băm đã lưu trong cơ sở dữ liệu.

        Returns:
            bool: True nếu thông tin khớp chính xác, ngược lại là False.
        """
        return pwd_context.verify(mat_khau_goc, mat_khau_hash)

    @staticmethod
    def tao_token_truy_cap(data: dict, thoi_gian_het_han: timedelta = None):
        """
        Tạo mã Access Token định dạng JWT (JSON Web Token) dùng để xác thực các yêu cầu API từ client.

        Args:
            data (dict): Dữ liệu tải trọng (payload) cần mã hóa vào token (chứa trường "sub" là email).
            thoi_gian_het_han (timedelta, optional): Thời gian hết hạn của token. Nếu không truyền sẽ lấy cấu hình mặc định.

        Returns:
            str: Chuỗi mã hóa Access Token định dạng JWT.
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
