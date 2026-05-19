from app.core.database import SessionLocal
from app.models.yeu_cau_ho_tro import YeuCauHoTro

def delete_all_tickets():
    db = SessionLocal()
    try:
        num_deleted = db.query(YeuCauHoTro).delete()
        db.commit()
        print(f"Successfully deleted {num_deleted} support ticket(s).")
    except Exception as e:
        db.rollback()
        print(f"Error deleting support tickets: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    delete_all_tickets()
