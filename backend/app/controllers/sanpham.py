from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.core.database import get_db
from app.schemas.sanpham import SanPhamRead, SanPhamCreate, SanPhamUpdate
from app.services.sanpham_service import SanPhamService


class XoaNhieuRequest(BaseModel):
    ids: List[int]

router = APIRouter(prefix="/san-pham", tags=["San Pham"])

@router.get("/", response_model=List[SanPhamRead])
def get_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return SanPhamService.get_all(db, skip=skip, limit=limit)

@router.get("/danh-muc/{category}", response_model=List[SanPhamRead])
def get_products_by_category(category: str, db: Session = Depends(get_db)):
    return SanPhamService.get_by_category(db, category=category)

@router.get("/{product_id}", response_model=SanPhamRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = SanPhamService.get_by_id(db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Khong tim thay san pham")
    return db_product

@router.post("/", response_model=SanPhamRead, status_code=status.HTTP_201_CREATED)
def create_new_product(product: SanPhamCreate, db: Session = Depends(get_db)):
    return SanPhamService.create(db, product=product)

@router.put("/{product_id}", response_model=SanPhamRead)
def update_existing_product(product_id: int, product: SanPhamUpdate, db: Session = Depends(get_db)):
    db_product = SanPhamService.update(db, product_id=product_id, product=product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Khong tim thay san pham")
    return db_product

@router.post("/xoa-nhieu")
def delete_multiple_products(request: XoaNhieuRequest, db: Session = Depends(get_db)):
    success_count = 0
    for product_id in request.ids:
        if SanPhamService.delete(db, product_id=product_id):
            success_count += 1
    return {"message": f"Đã xóa thành công {success_count} sản phẩm"}

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    success = SanPhamService.delete(db, product_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Khong tim thay san pham")
    return None
