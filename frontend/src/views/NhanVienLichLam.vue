<template>
  <div class="staff-roster-page">
    <!-- Header -->
    <header class="roster-header">
      <div class="roster-brand">
        <span class="brand-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FF9500" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="display: block; filter: drop-shadow(0 2px 6px rgba(255, 149, 0, 0.2));"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
        </span>
        <div>
          <h1>Lịch làm việc cá nhân</h1>
          <p class="staff-info">
            Nhân viên: <strong>{{ loggedEmployee?.name }}</strong> | Vai trò: 
            <span class="role-badge">{{ getRoleLabel(loggedEmployee?.role) }}</span>
          </p>
        </div>
      </div>
      <div class="header-actions">
        <button class="logout-btn" @click="handleLogout">
          Đăng xuất
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
        </button>
      </div>
    </header>

    <!-- Main Container -->
    <main class="roster-main">
      <!-- Toolbar controls -->
      <div class="roster-toolbar">
        <div class="view-switchers">
          <button 
            class="switch-btn" 
            :class="{ active: viewMode === 'week' }" 
            @click="viewMode = 'week'"
          >
            Xem theo Tuần
          </button>
          <button 
            class="switch-btn" 
            :class="{ active: viewMode === 'month' }" 
            @click="viewMode = 'month'"
          >
            Xem theo Tháng
          </button>
        </div>

        <div class="calendar-navigator">
          <button class="nav-arrow" @click="navigateCalendar(-1)">‹</button>
          <span class="nav-title">{{ viewTitle }}</span>
          <button class="nav-arrow" @click="navigateCalendar(1)">›</button>
        </div>
      </div>

      <!-- Weekly View Grid -->
      <div v-if="viewMode === 'week'" class="week-grid-view">
        <div 
          v-for="day in weekDays" 
          :key="day.dateStr" 
          class="week-day-card"
          :class="{ today: isToday(day.dateStr), 'past-day': isPast(day.dateStr) }"
          :style="{ opacity: isPast(day.dateStr) ? 0.65 : 1, background: isPast(day.dateStr) ? '#fafafa' : '#ffffff' }"
        >
          <div class="day-header" style="position: relative;">
            <span class="day-name">{{ day.name }}</span>
            <span class="day-number" :style="{ textDecoration: isPast(day.dateStr) ? 'line-through' : 'none', color: isPast(day.dateStr) ? '#FF2D55' : 'inherit' }">{{ day.dayNum }}</span>
            <span v-if="isPast(day.dateStr)" style="font-size: 9px; font-weight: 700; color: #FF2D55; background: rgba(255, 45, 85, 0.1); padding: 2px 6px; border-radius: 4px; text-transform: uppercase; margin-top: 4px; display: inline-block;">
              Ngày đã qua
            </span>
          </div>
          
          <div class="day-shifts">
            <div 
              v-for="s in getShiftsForDate(day.dateStr)" 
              :key="s.id" 
              class="shift-card"
              :class="getShiftClass(s.shift)"
            >
              <div class="shift-badge">{{ s.shift }}</div>
              <div class="shift-time">{{ getShiftTime(s.shift) }}</div>
              <div v-if="s.notes" class="shift-notes">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="display: inline-block; vertical-align: -1px; margin-right: 4px; color: #86868b;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
                <span>{{ s.notes }}</span>
              </div>
            </div>
            
            <div v-if="getShiftsForDate(day.dateStr).length === 0" class="no-shifts" style="display: flex; justify-content: center; align-items: center; gap: 4px; height: 100%;">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#86868b" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="opacity: 0.85;"><path d="M18 8h1a4 4 0 0 1 0 8h-1"></path><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"></path><line x1="6" y1="1" x2="6" y2="4"></line><line x1="10" y1="1" x2="10" y2="4"></line><line x1="14" y1="1" x2="14" y2="4"></line></svg>
              <span>Nghỉ ngơi</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Monthly View Calendar -->
      <div v-else class="month-calendar-view">
        <div class="calendar-header-row">
          <span v-for="day in ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']" :key="day" class="cal-header-cell">{{ day }}</span>
        </div>
        <div class="calendar-grid">
          <div 
            v-for="(cell, idx) in monthCells" 
            :key="idx" 
            class="calendar-day-cell"
            :class="{ 
              'other-month': !cell.isCurrentMonth, 
              today: isToday(cell.dateStr),
              'has-shift': getShiftsForDate(cell.dateStr).length > 0
            }"
            @click="selectDate(cell.dateStr)"
          >
            <span class="cell-number">{{ cell.dayNum }}</span>
            <div class="cell-shifts">
              <span 
                v-for="s in getShiftsForDate(cell.dateStr)" 
                :key="s.id" 
                class="cell-shift-dot"
                :title="s.shift"
                :class="getShiftClass(s.shift)"
              ></span>
            </div>
          </div>
        </div>

        <!-- Selected Day Details Sidebar / Footer -->
        <div class="selected-day-details">
          <h3>Chi tiết ngày {{ formatDateVN(selectedDate) }}</h3>
          <div class="details-list">
            <div 
              v-for="s in getShiftsForDate(selectedDate)" 
              :key="s.id" 
              class="shift-detail-item"
              :class="getShiftClass(s.shift)"
            >
              <div class="detail-top">
                <span class="detail-shift">{{ s.shift }}</span>
                <span class="detail-time">{{ getShiftTime(s.shift) }}</span>
              </div>
              <p v-if="s.notes" class="detail-notes"><strong>Ghi chú công việc:</strong> {{ s.notes }}</p>
            </div>
            <div v-if="getShiftsForDate(selectedDate).length === 0" class="detail-empty" style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; padding: 24px 0;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#86868b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="opacity: 0.85;"><path d="M18 8h1a4 4 0 0 1 0 8h-1"></path><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"></path><line x1="6" y1="1" x2="6" y2="4"></line><line x1="10" y1="1" x2="10" y2="4"></line><line x1="14" y1="1" x2="14" y2="4"></line></svg>
              <span>Không có lịch làm việc trong ngày này. Bạn được nghỉ ngơi!</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const loggedEmployee = ref(null);
const schedules = ref([]);
const viewMode = ref('week');
const currentDate = ref(new Date());
const selectedDate = ref(new Date().toISOString().split('T')[0]);

// Load user and schedules
onMounted(() => {
  const staff = localStorage.getItem('logged_employee');
  const token = localStorage.getItem('staff_token');
  
  if (!staff || !token) {
    router.push('/nhan-vien/dang-nhap');
    return;
  }
  
  loggedEmployee.value = JSON.parse(staff);
  fetchStaffSchedules();
});

const fetchStaffSchedules = async () => {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'}/api/admin/schedules`);
    if (res.ok) {
      const data = await res.json();
      // Filter by logged-in employee ID
      schedules.value = data.filter(s => s.employeeId === loggedEmployee.value?.id);
    }
  } catch (e) {
    console.error("Lỗi tải lịch làm: ", e);
  }
};

const handleLogout = () => {
  localStorage.removeItem('logged_employee');
  localStorage.removeItem('staff_token');
  router.push('/nhan-vien/dang-nhap');
};

const getRoleLabel = (role) => {
  const roles = {
    'ADMIN': 'Admin',
    'MANAGER': 'Quản lý',
    'STAFF': 'Nhân viên bán hàng',
    'SUPPORT': 'CSKH & Hỗ trợ',
    'SE': 'Kỹ thuật viên'
  };
  return roles[role] || role;
};

// Date helpers
const getLocalDateString = () => {
  const d = new Date();
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

const isToday = (dateStr) => {
  return dateStr === getLocalDateString();
};

const isPast = (dateStr) => {
  return dateStr < getLocalDateString();
};

const getShiftsForDate = (dateStr) => {
  return schedules.value.filter(s => s.date === dateStr);
};

const getShiftTime = (shift) => {
  const times = {
    'Ca Sáng': '08:00 - 12:00',
    'Ca Chiều': '12:00 - 18:00',
    'Ca Tối': '18:00 - 22:00',
    'Cả Ngày': '08:00 - 22:00'
  };
  return times[shift] || 'Không xác định';
};

const getShiftClass = (shift) => {
  const classes = {
    'Ca Sáng': 'morning',
    'Ca Chiều': 'afternoon',
    'Ca Tối': 'evening',
    'Cả Ngày': 'all-day'
  };
  return classes[shift] || '';
};

// Week View Calculations
const weekDays = computed(() => {
  const days = [];
  const startOfWeek = new Date(currentDate.value);
  const day = startOfWeek.getDay();
  const diff = startOfWeek.getDate() - day + (day === 0 ? -6 : 1); // Adjust for Mon start
  startOfWeek.setDate(diff);

  const dayNames = ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chủ Nhật'];
  
  for (let i = 0; i < 7; i++) {
    const d = new Date(startOfWeek);
    d.setDate(startOfWeek.getDate() + i);
    const dateStr = d.toISOString().split('T')[0];
    days.push({
      name: dayNames[i],
      dayNum: d.getDate(),
      dateStr: dateStr
    });
  }
  return days;
});

// Month View Calculations
const monthCells = computed(() => {
  const cells = [];
  const year = currentDate.value.getFullYear();
  const month = currentDate.value.getMonth();

  // First day of month
  const firstDay = new Date(year, month, 1);
  let startOffset = firstDay.getDay() - 1; // Mon is 0
  if (startOffset < 0) startOffset = 6; // Sun is 6

  // Total days in month
  const totalDays = new Date(year, month + 1, 0).getDate();

  // Prev month days
  const prevMonthDays = new Date(year, month, 0).getDate();
  for (let i = startOffset - 1; i >= 0; i--) {
    const d = new Date(year, month - 1, prevMonthDays - i);
    cells.push({
      dayNum: d.getDate(),
      dateStr: d.toISOString().split('T')[0],
      isCurrentMonth: false
    });
  }

  // Current month days
  for (let i = 1; i <= totalDays; i++) {
    const d = new Date(year, month, i);
    cells.push({
      dayNum: i,
      dateStr: d.toISOString().split('T')[0],
      isCurrentMonth: true
    });
  }

  // Next month days to pad to full weeks (multiples of 7)
  const remaining = 42 - cells.length; // 6 rows max
  for (let i = 1; i <= remaining; i++) {
    const d = new Date(year, month + 1, i);
    cells.push({
      dayNum: i,
      dateStr: d.toISOString().split('T')[0],
      isCurrentMonth: false
    });
  }

  return cells;
});

const viewTitle = computed(() => {
  const monthNames = [
    'Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6',
    'Tháng 7', 'Tháng 8', 'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12'
  ];
  const year = currentDate.value.getFullYear();
  const month = currentDate.value.getMonth();
  
  if (viewMode.value === 'week') {
    const start = weekDays.value[0];
    const end = weekDays.value[6];
    return `Tuần: ${start?.dayNum} - ${end?.dayNum} ${monthNames[month]} ${year}`;
  } else {
    return `${monthNames[month]}, ${year}`;
  }
});

const navigateCalendar = (direction) => {
  const d = new Date(currentDate.value);
  if (viewMode.value === 'week') {
    d.setDate(d.getDate() + (direction * 7));
  } else {
    d.setMonth(d.getMonth() + direction);
  }
  currentDate.value = d;
};

const selectDate = (dateStr) => {
  selectedDate.value = dateStr;
};

const formatDateVN = (dateStr) => {
  if (!dateStr) return '';
  const [y, m, d] = dateStr.split('-');
  return `${d}/${m}/${y}`;
};
</script>

<style scoped>
.staff-roster-page {
  min-height: 100vh;
  background-color: #f5f5f7;
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  display: flex;
  flex-direction: column;
}

.roster-header {
  background: #ffffff;
  border-bottom: 1px solid #d2d2d7;
  padding: 16px 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
}

.roster-brand {
  display: flex;
  align-items: center;
  gap: 16px;
}

.brand-icon {
  font-size: 32px;
}

.roster-brand h1 {
  font-size: 20px;
  font-weight: 700;
  margin: 0;
  color: #1d1d1f;
}

.staff-info {
  font-size: 13px;
  color: #86868b;
  margin: 2px 0 0 0;
}

.role-badge {
  background: rgba(255, 149, 0, 0.1);
  color: #ff9500;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
}

.logout-btn {
  background: rgba(255, 59, 48, 0.08);
  border: none;
  border-radius: 10px;
  color: #ff3b30;
  font-size: 13px;
  font-weight: 600;
  padding: 8px 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: #ff3b30;
  color: #ffffff;
}

.roster-main {
  flex: 1;
  max-width: 1100px;
  width: 100%;
  margin: 0 auto;
  padding: 24px 20px 60px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.roster-toolbar {
  background: #ffffff;
  border-radius: 16px;
  padding: 14px 24px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.view-switchers {
  background: #f5f5f7;
  border-radius: 10px;
  padding: 2px;
  display: flex;
}

.switch-btn {
  background: transparent;
  border: none;
  border-radius: 8px;
  color: #86868b;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  padding: 8px 16px;
  transition: all 0.2s ease;
}

.switch-btn.active {
  background: #ffffff;
  color: #1d1d1f;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}

.calendar-navigator {
  display: flex;
  align-items: center;
  gap: 16px;
}

.nav-arrow {
  background: #f5f5f7;
  border: none;
  border-radius: 8px;
  color: #1d1d1f;
  cursor: pointer;
  font-size: 20px;
  font-weight: bold;
  width: 32px;
  height: 32px;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: background 0.2s;
}

.nav-arrow:hover {
  background: #e8e8ed;
}

.nav-title {
  font-size: 15px;
  font-weight: 600;
  color: #1d1d1f;
  min-width: 180px;
  text-align: center;
}

/* Week View Layout */
.week-grid-view {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 12px;
}

.week-day-card {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid rgba(0,0,0,0.05);
  padding: 16px 12px;
  min-height: 250px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.week-day-card.today {
  border-color: #ff9500;
  box-shadow: 0 8px 24px rgba(255, 149, 0, 0.08);
}

.day-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  border-bottom: 1px solid #f5f5f7;
  padding-bottom: 8px;
}

.day-name {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  color: #86868b;
  letter-spacing: 0.5px;
}

.day-number {
  font-size: 24px;
  font-weight: 700;
  color: #1d1d1f;
  margin-top: 2px;
}

.week-day-card.today .day-number {
  color: #ff9500;
}

.day-shifts {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.shift-card {
  border-radius: 10px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 12px;
  border-left: 4px solid;
}

/* Colors for Shifts */
.shift-card.morning {
  background: rgba(52, 199, 89, 0.08);
  border-left-color: #34C759;
}
.shift-card.morning .shift-badge {
  color: #34C759;
  font-weight: bold;
}

.shift-card.afternoon {
  background: rgba(0, 122, 255, 0.08);
  border-left-color: #007AFF;
}
.shift-card.afternoon .shift-badge {
  color: #007AFF;
  font-weight: bold;
}

.shift-card.evening {
  background: rgba(255, 149, 0, 0.08);
  border-left-color: #FF9500;
}
.shift-card.evening .shift-badge {
  color: #FF9500;
  font-weight: bold;
}

.shift-card.all-day {
  background: rgba(175, 82, 222, 0.08);
  border-left-color: #AF52DE;
}
.shift-card.all-day .shift-badge {
  color: #AF52DE;
  font-weight: bold;
}

.shift-time {
  font-weight: 600;
  color: #1d1d1f;
}

.shift-notes {
  font-size: 11px;
  color: #515154;
  word-break: break-word;
}

.no-shifts {
  font-size: 11.5px;
  color: #86868b;
  text-align: center;
  padding: 20px 0;
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Month View Layout */
.month-calendar-view {
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid rgba(0,0,0,0.05);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.calendar-header-row {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  border-bottom: 1px solid #f5f5f7;
  padding-bottom: 8px;
}

.cal-header-cell {
  font-size: 12px;
  font-weight: 600;
  color: #86868b;
  text-transform: uppercase;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.calendar-day-cell {
  aspect-ratio: 1.2;
  border-radius: 12px;
  padding: 8px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
  transition: all 0.2s;
}

.calendar-day-cell:hover {
  background: #f5f5f7;
}

.calendar-day-cell.other-month {
  opacity: 0.3;
}

.calendar-day-cell.today {
  background: rgba(255, 149, 0, 0.05);
  border: 1px solid #ff9500;
}

.calendar-day-cell.today .cell-number {
  color: #ff9500;
  font-weight: 700;
}

.cell-number {
  font-size: 14px;
  font-weight: 500;
  color: #1d1d1f;
}

.cell-shifts {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
  width: 100%;
}

.cell-shift-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  display: inline-block;
}

.cell-shift-dot.morning { background-color: #34C759; }
.cell-shift-dot.afternoon { background-color: #007AFF; }
.cell-shift-dot.evening { background-color: #FF9500; }
.cell-shift-dot.all-day { background-color: #AF52DE; }

.selected-day-details {
  border-top: 1px solid #f5f5f7;
  padding-top: 20px;
  margin-top: 10px;
}

.selected-day-details h3 {
  font-size: 15px;
  font-weight: 600;
  margin: 0 0 12px 0;
}

.details-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.shift-detail-item {
  padding: 12px 16px;
  border-radius: 12px;
  border-left: 4px solid;
}

.shift-detail-item.morning {
  background: rgba(52, 199, 89, 0.05);
  border-left-color: #34C759;
}
.shift-detail-item.morning .detail-shift { color: #34C759; font-weight: bold; }

.shift-detail-item.afternoon {
  background: rgba(0, 122, 255, 0.05);
  border-left-color: #007AFF;
}
.shift-detail-item.afternoon .detail-shift { color: #007AFF; font-weight: bold; }

.shift-detail-item.evening {
  background: rgba(255, 149, 0, 0.05);
  border-left-color: #FF9500;
}
.shift-detail-item.evening .detail-shift { color: #FF9500; font-weight: bold; }

.shift-detail-item.all-day {
  background: rgba(175, 82, 222, 0.05);
  border-left-color: #AF52DE;
}
.shift-detail-item.all-day .detail-shift { color: #AF52DE; font-weight: bold; }

.detail-top {
  display: flex;
  justify-content: space-between;
  font-size: 13.5px;
  margin-bottom: 4px;
}

.detail-notes {
  font-size: 12.5px;
  color: #515154;
  margin: 4px 0 0 0;
}

.detail-empty {
  font-size: 13px;
  color: #86868b;
  text-align: center;
  padding: 20px 0;
}

@media (max-width: 768px) {
  .week-grid-view {
    grid-template-columns: 1fr;
  }
  
  .week-day-card {
    min-height: auto;
  }
  
  .calendar-day-cell {
    aspect-ratio: 1;
  }
}
</style>
