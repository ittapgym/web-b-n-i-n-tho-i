from sqlalchemy.orm import Session
from app.models.sanpham import SanPham
from app.schemas.sanpham import SanPhamCreate, SanPhamUpdate

class SanPhamService:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        """
        Lấy danh sách tất cả sản phẩm trong cơ sở dữ liệu với phân trang.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            skip (int, optional): Số bản ghi cần bỏ qua. Mặc định là 0.
            limit (int, optional): Số lượng bản ghi tối đa lấy ra. Mặc định là 100.

        Returns:
            List[SanPham]: Danh sách các đối tượng sản phẩm.
        """
        return db.query(SanPham).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_category(db: Session, category: str):
        """
        Lấy danh sách sản phẩm theo danh mục chỉ định.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            category (str): Tên danh mục cần lọc.

        Returns:
            List[SanPham]: Danh sách sản phẩm thuộc danh mục.
        """
        return db.query(SanPham).filter(SanPham.danh_muc == category).all()

    @staticmethod
    def get_by_id(db: Session, product_id: int):
        """
        Lấy thông tin chi tiết một sản phẩm bằng ID định danh.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            product_id (int): ID sản phẩm cần tìm.

        Returns:
            SanPham: Đối tượng sản phẩm tìm được hoặc None nếu không tồn tại.
        """
        return db.query(SanPham).filter(SanPham.id == product_id).first()

    @staticmethod
    def create(db: Session, product: SanPhamCreate):
        """
        Tạo mới một sản phẩm và lưu vào cơ sở dữ liệu.
        Ghi nhật ký hoạt động của quản trị viên.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            product (SanPhamCreate): Dữ liệu chi tiết sản phẩm mới.

        Returns:
            SanPham: Bản ghi sản phẩm vừa được tạo.
        """
        db_product = SanPham(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        
        # Ghi nhật ký Admin
        from app.services.admin_activity_service import AdminActivityService
        AdminActivityService.ghi_log(db, f"Đã thêm sản phẩm mới: {db_product.ten}", "Admin")
        
        return db_product

    @staticmethod
    def update(db: Session, product_id: int, product: SanPhamUpdate):
        """
        Cập nhật thông tin chi tiết của một sản phẩm.
        Ghi nhật ký hoạt động của quản trị viên.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            product_id (int): ID sản phẩm cần sửa.
            product (SanPhamUpdate): Dữ liệu cập nhật mới.

        Returns:
            SanPham: Đối tượng sản phẩm sau cập nhật hoặc None nếu không tìm thấy.
        """
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
        AdminActivityService.ghi_log(db, f"Đã cập nhật thông tin sản phẩm: {db_product.ten}", "Admin")
        
        return db_product

    @staticmethod
    def delete(db: Session, product_id: int):
        """
        Xóa sản phẩm khỏi hệ thống.
        Ghi nhật ký hoạt động của quản trị viên.

        Args:
            db (Session): Phiên kết nối Cơ sở dữ liệu SQLAlchemy.
            product_id (int): ID sản phẩm cần xóa.

        Returns:
            bool: True nếu xóa thành công, ngược lại là False.
        """
        db_product = db.query(SanPham).filter(SanPham.id == product_id).first()
        if not db_product:
            return False
            
        product_name = db_product.ten
        db.delete(db_product)
        db.commit()
        
        # Ghi nhật ký Admin
        from app.services.admin_activity_service import AdminActivityService
        AdminActivityService.ghi_log(db, f"Xóa vĩnh viễn sản phẩm: {product_name}", "Admin")
        
        return True
