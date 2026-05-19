from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.core.database import get_db
from app.schemas.sanpham import SanPhamRead, SanPhamCreate, SanPhamUpdate
from app.services.sanpham_service import SanPhamService


class XoaNhieuRequest(BaseModel):
    ids: List[int]

def format_product_urls(product, request: Request) -> SanPhamRead:
    if not product:
        return product
    base_url = str(request.base_url).rstrip('/')
    p_read = SanPhamRead.model_validate(product)
    
    if p_read.hinh_anh:
        ha = p_read.hinh_anh.strip()
        if "127.0.0.1:8000" in ha:
            ha = ha.replace("http://127.0.0.1:8000", "")
        if not ha.startswith("http"):
            p_read.hinh_anh = f"{base_url}{ha}"
        else:
            p_read.hinh_anh = ha
            
    if p_read.thu_vien_anh:
        new_gallery = []
        for img in p_read.thu_vien_anh:
            if img:
                img_str = img.strip()
                if "127.0.0.1:8000" in img_str:
                    img_str = img_str.replace("http://127.0.0.1:8000", "")
                if not img_str.startswith("http"):
                    new_gallery.append(f"{base_url}{img_str}")
                else:
                    new_gallery.append(img_str)
        p_read.thu_vien_anh = new_gallery
        
    return p_read

router = APIRouter(prefix="/san-pham", tags=["San Pham"])

@router.get("/", response_model=List[SanPhamRead])
def get_all_products(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_products = SanPhamService.get_all(db, skip=skip, limit=limit)
    return [format_product_urls(p, request) for p in db_products]

@router.get("/danh-muc/{category}", response_model=List[SanPhamRead])
def get_products_by_category(request: Request, category: str, db: Session = Depends(get_db)):
    db_products = SanPhamService.get_by_category(db, category=category)
    return [format_product_urls(p, request) for p in db_products]

@router.get("/{product_id}", response_model=SanPhamRead)
def get_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    db_product = SanPhamService.get_by_id(db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Khong tim thay san pham")
    return format_product_urls(db_product, request)

@router.post("/", response_model=SanPhamRead, status_code=status.HTTP_201_CREATED)
def create_new_product(request: Request, product: SanPhamCreate, db: Session = Depends(get_db)):
    db_product = SanPhamService.create(db, product=product)
    return format_product_urls(db_product, request)

@router.put("/{product_id}", response_model=SanPhamRead)
def update_existing_product(request: Request, product_id: int, product: SanPhamUpdate, db: Session = Depends(get_db)):
    db_product = SanPhamService.update(db, product_id=product_id, product=product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Khong tim thay san pham")
    return format_product_urls(db_product, request)

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
