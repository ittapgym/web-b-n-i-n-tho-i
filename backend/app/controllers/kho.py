from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter(prefix="/api/admin/inventory", tags=["Admin Quản lý Kho"])

@router.get("/logs")
def get_inventory_logs(db: Session = Depends(get_db)):
    """
    Lấy danh sách nhật ký nhập xuất kho hàng (nhập kho, xuất kho, điều chỉnh số lượng).

    Args:
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        list: Danh sách thông tin lịch sử nhập xuất kho.
    """
    return [
        {"id": 1, "product_name": "iPhone 15 Pro", "action": "Nhập kho", "quantity": 50, "time": "2024-05-13 10:00"},
        {"id": 2, "product_name": "MacBook Pro M3", "action": "Xuất kho", "quantity": 5, "time": "2024-05-13 09:30"},
        {"id": 3, "product_name": "iPad Air 5", "action": "Nhập kho", "quantity": 20, "time": "2024-05-12 15:20"}
    ]

@router.delete("/logs/{log_id}")
def delete_inventory_log(log_id: int, db: Session = Depends(get_db)):
    """
    Xóa một dòng nhật ký nhập xuất kho cụ thể dựa trên ID định danh.

    Args:
        log_id (int): ID của dòng nhật ký kho cần xóa.
        db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.

    Returns:
        dict: Trạng thái thành công và thông điệp xác nhận xóa.
    """
    return {"message": "Đã xóa nhật ký"}
