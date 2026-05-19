from app.core.database import SessionLocal
from app.models.donhang import DonHang

def check_orders():
    db = SessionLocal()
    try:
        orders = db.query(DonHang).all()
        print(f"Total orders: {len(orders)}")
        for o in orders:
            print(f"ID: {o.id}, Customer: {o.ten_khach_hang}, Total: {o.tong_tien}")
    finally:
        db.close()

if __name__ == "__main__":
    check_orders()
