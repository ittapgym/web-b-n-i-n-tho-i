from sqlalchemy.orm import Session
from app.models.hoatdong_admin import HoatDongAdmin
from datetime import datetime

class AdminActivityService:
    @staticmethod
    def ghi_log(db: Session, thao_tac: str, nhan_vien: str = "Admin"):
        """Ghi nhật ký hoạt động của Admin. Tự động bỏ qua các thao tác làm mới, load lại, xem danh sách."""
        thao_tac_lower = thao_tac.lower()
        ignore_keywords = [
            "xem danh sách", "load", "tải lại", "làm mới", 
            "refresh", "get", "fetch", "view", "đọc tin", "truy vấn"
        ]
        # Không ghi log các thao tác chỉ đọc hoặc làm mới dữ liệu
        if any(kw in thao_tac_lower for kw in ignore_keywords):
            return None
            
        try:
            log = HoatDongAdmin(
                nhan_vien=nhan_vien,
                thao_tac=thao_tac,
                thoi_gian=datetime.utcnow()
            )
            db.add(log)
            db.commit()
            db.refresh(log)
            return log
        except Exception as e:
            db.rollback()
            print(f">>> Lỗi ghi log Admin: {e}")
            return None
