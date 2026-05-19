from sqlalchemy.orm import Session
from app.models.sanpham import SanPham
from app.schemas.sanpham import SanPhamCreate, SanPhamUpdate

class SanPhamService:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(SanPham).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_category(db: Session, category: str):
        return db.query(SanPham).filter(SanPham.danh_muc == category).all()

    @staticmethod
    def get_by_id(db: Session, product_id: int):
        return db.query(SanPham).filter(SanPham.id == product_id).first()

    @staticmethod
    def create(db: Session, product: SanPhamCreate):
        db_product = SanPham(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        
        # Ghi nhật ký Admin
        from app.services.admin_activity_service import AdminActivityService
        AdminActivityService.ghi_log(db, f"Đã thêm sản phẩm mới: {db_product.ten_san_pham}", "Admin")
        
        return db_product

    @staticmethod
    def update(db: Session, product_id: int, product: SanPhamUpdate):
        db_product = db.query(SanPham).filter(SanPham.id == product_id).first()
        if not db_product:
            return None
        
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        
        db.commit()
        db.refresh(db_product)
        
        # Ghi nhật ký Admin
        from app.services.admin_activity_service import AdminActivityService
        AdminActivityService.ghi_log(db, f"Đã cập nhật thông tin sản phẩm: {db_product.ten_san_pham}", "Admin")
        
        return db_product

    @staticmethod
    def delete(db: Session, product_id: int):
        db_product = db.query(SanPham).filter(SanPham.id == product_id).first()
        if not db_product:
            return False
            
        product_name = db_product.ten_san_pham
        db.delete(db_product)
        db.commit()
        
        # Ghi nhật ký Admin
        from app.services.admin_activity_service import AdminActivityService
        AdminActivityService.ghi_log(db, f"Xóa vĩnh viễn sản phẩm: {product_name}", "Admin")
        
        return True
