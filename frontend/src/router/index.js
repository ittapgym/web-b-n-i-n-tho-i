import { createRouter, createWebHistory } from 'vue-router'
import DangNhap from '../views/DangNhap.vue'
import DangKy from '../views/DangKy.vue'
import TrangChu from '../views/TrangChu.vue'
import DienThoai from '../views/DienThoai.vue'
import MayTinhBang from '../views/MayTinhBang.vue'
import Laptop from '../views/Laptop.vue'
import PhuKien from '../views/PhuKien.vue'
import HoTro from '../views/HoTro.vue'
import TaiKhoan from '../views/TaiKhoan.vue'
import GioHang from '../views/GioHang.vue'
import ChiTietSanPham from '../views/ChiTietSanPham.vue'
import NhanVienDangNhap from '../views/NhanVienDangNhap.vue'
import NhanVienLichLam from '../views/NhanVienLichLam.vue'

const routes = [
  {
    path: '/',
    name: 'TrangChu',
    component: TrangChu
  },
  {
    path: '/login',
    name: 'DangNhap',
    component: DangNhap
  },
  {
    path: '/dang-ky',
    name: 'DangKy',
    component: DangKy
  },
  {
    path: '/dien-thoai',
    name: 'DienThoai',
    component: DienThoai
  },
  {
    path: '/may-tinh-bang',
    name: 'MayTinhBang',
    component: MayTinhBang
  },
  {
    path: '/laptop',
    name: 'Laptop',
    component: Laptop
  },
  {
    path: '/phu-kien',
    name: 'PhuKien',
    component: PhuKien
  },
  { 
    path: '/ho-tro',
    name: 'HoTro',
    component: HoTro
  },
  {
    path: '/account',
    name: 'TaiKhoan',
    component: TaiKhoan
  },
  {
    path: '/cart',
    name: 'GioHang',
    component: GioHang
  },
  {
    path: '/san-pham/:id',
    name: 'ChiTietSanPham',
    component: ChiTietSanPham
  },
  {
    path: '/nhan-vien/dang-nhap',
    name: 'NhanVienDangNhap',
    component: NhanVienDangNhap
  },
  {
    path: '/nhan-vien/lich-lam',
    name: 'NhanVienLichLam',
    component: NhanVienLichLam
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 }
  }
})

// Navigation Guard
router.beforeEach((to, from) => {
  const protectedRoutes = ['GioHang', 'TaiKhoan']
  const token = localStorage.getItem('access_token') || localStorage.getItem('token')
  
  if (protectedRoutes.includes(to.name) && !token) {
    // Lưu đường dẫn hiện tại để sau login quay lại
    localStorage.setItem('redirect_after_login', to.fullPath)
    return { name: 'DangNhap' }
  }
  return true;
})

export default router
