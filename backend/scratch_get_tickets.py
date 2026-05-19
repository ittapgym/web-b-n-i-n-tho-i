from app.core.database import SessionLocal
from app.models.yeu_cau_ho_tro import YeuCauHoTro

def get_tickets():
    db = SessionLocal()
    try:
        tickets = db.query(YeuCauHoTro).order_by(YeuCauHoTro.id.desc()).all()
        print(f"Total tickets: {len(tickets)}")
        for t in tickets:
            print(f"ID: {t.id}")
            print(f"  Chu de: {t.chu_de}")
            print(f"  Trang thai: {t.trang_thai}")
            print(f"  Hinh anh: {t.hinh_anh}")
            print(f"  User ID: {t.nguoi_dung_id}")
            print("-" * 40)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    get_tickets()
