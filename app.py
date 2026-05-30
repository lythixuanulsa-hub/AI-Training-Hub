import streamlit as st
# Trigger reload
import pandas as pd
from datetime import datetime, date, timedelta
import database as db
import os
import calendar

# Page configuration
st.set_page_config(
    page_title="Lịch đăng ký đào tạo AI năm 2026",
    page_icon="📅",
    layout="wide"
)

# Load CSS
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles.css")

# Initialize database
db.init_db()
db.init_docs_db()
db.init_trainers_db()

# Trainer Data
TRAINERS = [
    {"name": "Yun kwon", "role_vn": "Lead Instructor (Chủ trì)", "role_kr": "수석 강사 (주관)", "team": "TPM Team Leader", "desc": "Chuyên gia cao cấp về chuyển đổi số và AI."},
    {"name": "Xuan (쑤언)", "role_vn": "Main Instructor / Representative", "role_kr": "주강사 / 대표", "team": "TPM Team", "desc": "Giảng viên chính phụ trách nội dung đào tạo."},
    {"name": "Trang (짱)", "role_vn": "Co-Instructor / Support", "role_kr": "보조 강사 / 지원", "team": "TPM Team", "desc": "Hỗ trợ học viên và quản lý lớp học."},
    {"name": "Duy (주이)", "role_vn": "Co-Instructor / Technical Support", "role_kr": "보조 강사 / 기술 지원", "team": "TPM Team", "desc": "Phụ trách kỹ thuật và hướng dẫn thực hành."}
]

# Language Dictionary
LANG_DICT = {
    "Tiếng Việt": {
        "sidebar_title": "🛠 Quản lý Đào tạo / 교육 관리",
        "lang_select": "🌐 Ngôn ngữ / 언어 chọn:",
        "menu_label": "Chức năng / 메뉴 chọn:",
        "menu_home": "🏠 Trang chủ & Lịch / 홈 및 일정",
        "menu_progress": "📈 Tiến độ Bộ phận / 부서별 진도",
        "menu_reg": "📝 Đăng ký Đào tạo / 교육 신청",
        "menu_trainers": "👨‍🏫 Giảng viên / 강사 정보",
        "menu_docs": "📚 Tài liệu / 교육 자료",
        "menu_admin": "🔐 Quản trị viên / 관리자",
        "progress_title": "📈 Tiến độ đào tạo AI theo Bộ phận",
        "progress_subtitle": "2026년 부서별 AI 교육 진행 현황",
        "team_name": "Tên Team / 팀명",
        "completed_ratio": "Tỷ lệ hoàn thành",
        "planned_upcoming": "Đã lên lịch",
        "not_registered": "Chưa đăng ký",
        "note_col": "Ghi chú",
        "filter_dept": "Lọc theo Bộ phận:",
        "search_team": "Tìm kiếm Team:",
        "summary_teams": "Tổng số Team",
        "summary_completed": "Đã hoàn thành 4/4",
        "summary_in_progress": "Đang đào tạo",
        "home_title": "Lịch đăng ký đào tạo AI năm 2026",
        "home_subtitle": "2026년 AI 교육 신청 일정",
        "select_month": "Chọn tháng xem lịch / 일정 조회 월 선택:",
        "month_label": "Tháng / 월",
        "calendar_title": "🗓 Lịch trình Tháng / 일정표 -",
        "weekdays": ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"],
        "legend": "🟢 **Xanh lá**: Hoàn thành (✅) | 🔵 **Xanh dương**: Ca Sáng | 🟠 **Cam**: Ca Chiều | ⬛ **Xám**: Ngày nghỉ (Chủ Nhật)",
        "reg_title": "📝 Biểu mẫu Đăng ký Đào tạo / 교육 신청서",
        "reg_note": "⚠️ **Lưu ý:** Các bộ phận hãy đăng ký theo một khung giờ và thứ cố định hàng tuần. / 매주 고정된 요일과 시간대를 선택하여 신청해 주세요.",
        "dept": "Bộ phận / 부서:",
        "team": "Team (tự điền) / 팀명:",
        "session": "3. Buổi đào tạo / 교육 회차:",
        "attendees": "6. Số lượng người nhận đào tạo / 교육 인원:",
        "date": "4. Ngày đào tạo (Tháng 5, 6, 7) / 교육 날짜:",
        "timeslot": "5. Khung giờ / 시간대:",
        "period": "Buổi / 구분:",
        "morning": "Sáng / 오전",
        "afternoon": "Chiều / 오후",
        "time_exact": "Giờ cụ thể / 상세 시간:",
        "submit": "Xác nhận Đăng ký / 신청 확인",
        "success": "✅ Đã lưu đăng ký thành công! / 신청이 성공적으로 저장되었습니다!",
        "error": "⚠️ Vui lòng điền đủ thông tin. / 모든 정보를 입력해 주세요.",
        "admin_title": "🔐 Khu vực Quản trị viên / 관리자 전용",
        "password": "Nhập mật khẩu / 비밀번호를 입력하세요:",
        "auth_success": "Xác thực thành công! / 인증 성공!",
        "tab_list": "📊 Danh sách Tổng hợp / 전체 목록",
        "tab_manage": "🗑️ Quản lý & Xóa / 관리 및 삭제",
        "tab_docs": "📂 Quản lý Tài liệu / 자료 관리",
        "list_title": "📊 Toàn bộ danh sách đăng ký / 전체 신청 목록",
        "download": "📥 Tải xuống (CSV) / 다운로드",
        "no_data": "Chưa có dữ liệu. / 데이터가 없습니다.",
        "delete_title": "🗑️ Xóa bản đăng ký / 신청 삭제",
        "delete_btn": "Xóa / 삭제",
        "placeholder_team": "Ví dụ: Kỹ thuật... / 예: 기술팀...",
        "placeholder_time": "Ví dụ: 09:00...",
        "placeholder_dept": "Ví dụ: Bảo vệ... / 예: 보안...",
        "people": "người / 명",
        "sessions": ["Buổi 1: Lý thuyết / 1회차: 이론", "Buổi 2: Thực hành cơ bản / 2회차: 기본 실습", "Buổi 3: Thực hành nâng cao / 3회차: 심화 실습", "Buổi 4: Chia sẻ bài tập / 4회차: 과제 공유"],
        "stats_title": "📊 Tóm tắt tình hình đăng ký",
        "stat_total_regs": "Lượt đăng ký",
        "stat_depts": "Bộ phận tham gia",
        "stat_total_people": "Tổng số nhân viên",
        "participating_depts_list": "Các Bộ phận đã tham gia:",
        "trainer_title": "👨‍🏫 Đội ngũ Giảng viên AI / AI 교육 강사팀",
        "docs_title": "📚 Kho tài liệu đào tạo / 교육 자료실",
        "docs_no_data": "Chưa có dữ liệu tài liệu. / 교육 자료가 없습니다.",
        "doc_upload": "Tải lên tài liệu mới / 새 자료 업로드",
        "doc_name": "Tên tài liệu / 자료명",
        "doc_desc": "Mô tả ngắn / 설명",
        "doc_cat": "Danh mục / 카테고리",
        "doc_file": "Chọn file tài liệu / 파일 선택",
        "doc_date": "Ngày đăng / 업로드 날짜",
        "doc_success": "Tải lên thành công! / 업로드 성공!",
        "doc_download": "Tải về / 다운로드",
        "menu_roadmap": "📈 Tiến độ Bộ phận / 부서별 진도",
        "roadmap_title": "📈 Tiến độ Đào tạo AI theo Bộ phận",
        "roadmap_subtitle": "Theo dõi lộ trình và tỉ lệ tham dự 4 buổi học tự động của các Team",
        "roadmap_search": "Tìm kiếm theo tên Team / 팀명 검색:",
        "roadmap_dept": "Lọc theo Bộ phận / 부서별 필터:",
        "roadmap_dept_all": "Tất cả Bộ phận / 전체 부서",
        "status_completed": "Đã học / 완료",
        "status_scheduled": "Lịch học / 예정",
        "status_not_scheduled": "Chưa đăng ký / 미신청",
        "roadmap_actual": "Số người thực tế / 실제 인원",
        "roadmap_note": "Ghi chú / 비고",
        "roadmap_kpi_total_teams": "Số Team đăng ký / 등록 팀 수",
        "roadmap_kpi_completed_sessions": "Số Team hoàn thành / 완료 팀 수",
        "roadmap_kpi_scheduled_sessions": "Số buổi đã đăng ký / 신청 세션 수",
        "roadmap_kpi_avg_progress": "Tiến độ hoàn thành / 완료 진도율",
        "admin_actual_label": "Số người đi học thực tế / 실제 참석 인원:",
        "admin_note_label": "Ghi chú / 비고 (lý do lùi lịch...):"
    },
    "한국어": {
        "sidebar_title": "🛠 Quản lý Đào tạo / 교육 quản lý",
        "lang_select": "🌐 Ngôn ngữ / 언어 chọn:",
        "menu_label": "Chức năng / 메뉴 chọn:",
        "menu_home": "🏠 Trang chủ & Lịch / 홈 및 일정",
        "menu_reg": "📝 Đăng ký Đào tạo / 교육 신청",
        "menu_trainers": "👨‍🏫 강사 정보 / Giảng viên",
        "menu_docs": "📚 교육 자료 / Tài liệu",
        "menu_admin": "🔐 관리자 / Quản trị viên",
        "home_title": "2026년 AI 교육 신청 일정",
        "home_subtitle": "Lịch đăng ký đào tạo AI năm 2026",
        "select_month": "Chọn tháng xem lịch / 일정 조회 월 선택:",
        "month_label": "Tháng / 월",
        "calendar_title": "🗓 Lịch trình Tháng / 일정표 -",
        "weekdays": ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"],
        "legend": "🟢 **초록색**: 교육 완료 (✅) | 🔵 **파란색**: 오전 | 🟠 **주황색**: 오후 | ⬛ **회색**: 휴일 (일요일)",
        "reg_title": "📝 교육 신청서 / Biểu mẫu Đăng ký",
        "reg_note": "⚠️ **참고:** 매주 고정된 요일과 시간대를 선택하여 신청해 주세요. / Lưu ý: Đăng ký theo khung giờ cố định.",
        "dept": "부서 / Bộ phận:",
        "team": "팀명 / Team (tự điền):",
        "session": "3. 교육 회차 / Buổi đào tạo:",
        "attendees": "6. 교육 인원 / Số lượng người:",
        "date": "4. 교육 날짜 (5, 6, 7월) / Ngày đào tạo:",
        "timeslot": "5. 시간대 / Khung giờ:",
        "period": "구분 / Buổi:",
        "morning": "오전 / Sáng",
        "afternoon": "오후 / Chiều",
        "time_exact": "상세 시간 / Giờ cụ thể:",
        "submit": "신청 확인 / Xác nhận",
        "success": "✅ 신청이 성공적으로 저장되었습니다! / Lưu thành công!",
        "error": "⚠️ 모든 정보를 입력해 주세요. / Vui lòng điền đủ thông tin.",
        "admin_title": "🔐 관리자 전용 / Quản trị viên",
        "password": "비밀번호를 입력하세요 / Nhập mật khẩu:",
        "auth_success": "인증 성공! / Xác thực thành công!",
        "tab_list": "📊 전체 목록 / Danh sách",
        "tab_manage": "🗑️ 관리 및 삭제 / Quản lý",
        "tab_docs": "📂 자료 관리 / Quản lý Tài liệu",
        "list_title": "📊 전체 신청 목록 / Toàn bộ danh sách",
        "download": "📥 전체 다운로드 (CSV) / Tải xuống",
        "no_data": "데이터가 없습니다. / Chưa có dữ liệu.",
        "delete_title": "🗑️ 신청 삭제 / Xóa bản đăng ký",
        "delete_btn": "삭제 / Xóa",
        "placeholder_team": "예: 기술팀... / Ví dụ: Kỹ thuật...",
        "placeholder_time": "예: 09:00...",
        "placeholder_dept": "예: 보안... / Ví dụ: Bảo vệ...",
        "people": "명 / người",
        "sessions": ["1회차: 이론 / Buổi 1: Lý thuyết", "2회차: 기본 실습 / Buổi 2: Thực hành cơ bản", "3회차: 심화 실습 / Buổi 3: Thực hành nâng cao", "4회차: 과제 공유 / Buổi 4: Chia sẻ bài tập"],
        "stats_title": "📊 등록 현황 요약",
        "stat_total_regs": "총 등록 건수",
        "stat_depts": "참여 부서 수",
        "stat_total_people": "총 참여 인원",
        "participating_depts_list": "참여 부서 목록:",
        "trainer_title": "👨‍🏫 AI 교육 강사팀 / Đội ngũ Giảng viên AI",
        "docs_title": "📚 교육 자료실 / Kho tài liệu đào tạo",
        "docs_no_data": "교육 자료가 없습니다. / Chưa có dữ liệu tài liệu.",
        "doc_upload": "새 자료 업로드 / Tải lên tài liệu mới",
        "doc_name": "자료명 / Tên tài liệu",
        "doc_desc": "설명 / Mô tả ngắn",
        "doc_cat": "카테고리 / Danh mục",
        "doc_file": "파일 선택 / Chọn file tài liệu",
        "doc_date": "업로드 날짜 / Ngày đăng",
        "doc_success": "업로드 성공! / Tải lên thành công!",
        "doc_download": "다운로드 / Tải về",
        "menu_roadmap": "📈 부서별 진도 / Tiến độ Bộ phận",
        "roadmap_title": "📈 부서별 AI 교육 진행 현황",
        "roadmap_subtitle": "각 팀의 4회차 교육 일정 및 이수 현황을 자동 추적합니다.",
        "roadmap_search": "팀명 검색 / Tìm kiếm theo tên Team:",
        "roadmap_dept": "부서별 필터 / Lọc theo Bộ phận:",
        "roadmap_dept_all": "전체 부서 / Tất cả Bộ phận",
        "status_completed": "이수완료 / Đã học",
        "status_scheduled": "교육예정 / Lịch học",
        "status_not_scheduled": "미신청 / Chưa đăng ký",
        "roadmap_actual": "실제 인원 / Số người thực tế",
        "roadmap_note": "비고 / Ghi chú",
        "roadmap_kpi_total_teams": "Số Team đăng ký / 등록 팀 수",
        "roadmap_kpi_completed_sessions": "Số Team hoàn thành / 완료 팀 수",
        "roadmap_kpi_scheduled_sessions": "Số buổi đã đăng ký / 신청 세션 수",
        "roadmap_kpi_avg_progress": "Tiến độ hoàn thành / 완료 진도율",
        "admin_actual_label": "실제 참석 인원 / Số người đi học thực tế:",
        "admin_note_label": "비고 / Ghi chú (일정 연기 사유...):"
    }
}

# Initial language check
if "lang" not in st.session_state:
    st.session_state.lang = "Tiếng Việt"
if "docs_authenticated" not in st.session_state:
    st.session_state.docs_authenticated = False

# --- SIDEBAR BRANDING ---
try:
    import os
    if os.path.exists("KakaoTalk_20260502_160619185.jpg"):
        st.sidebar.image("KakaoTalk_20260502_160619185.jpg", use_container_width=True)
    else:
        st.sidebar.image("images/KakaoTalk_20260502_160619185.jpg", use_container_width=True)
except Exception:
    pass

st.sidebar.markdown(f'<h1 style="color: #333; font-size: 1.4rem; text-align: center; margin-top: 0; margin-bottom: 20px; border-bottom: 2px solid #4b6cb7; padding-bottom: 10px;">TPM _ AI TRAINING HUB</h1>', unsafe_allow_html=True)

# 1. Language Selection in Sidebar (Moved below title)
lang_choice = st.sidebar.radio(
    "🌐 Ngôn ngữ / 언어 chọn:",
    ["Tiếng Việt", "한국어"],
    index=0 if st.session_state.lang == "Tiếng Việt" else 1,
    key="lang_radio"
)

# Update session state and rerun if language changed
if lang_choice != st.session_state.lang:
    st.session_state.lang = lang_choice
    st.rerun()

lang = st.session_state.lang
T = LANG_DICT[lang]

# Sidebar Navigation
st.sidebar.markdown("<br/>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    T["menu_label"],
    [T["menu_home"], T["menu_roadmap"], T["menu_reg"], T["menu_trainers"], T["menu_docs"], T["menu_admin"]],
    key="menu_radio"
)

# --- HOME PAGE ---
if menu == T["menu_home"]:
    st.markdown(f'<div class="main-header"><h1>{T["home_title"]}</h1><p>{T["home_subtitle"]}</p></div>', unsafe_allow_html=True)
    
    registrations = db.get_registrations()
    
    # Dynamic default month selection based on the current real-world month
    today_month = datetime.now().month
    default_idx = 0
    if today_month == 6:
        default_idx = 1
    elif today_month == 7:
        default_idx = 2
    elif today_month > 7:
        default_idx = 2  # Default to last month if after July
        
    current_month = st.radio(T["select_month"], [5, 6, 7], index=default_idx, horizontal=True, format_func=lambda x: f"{T['month_label']} {x}")
    year = 2026
    
    st.markdown(f"### {T['calendar_title']} {current_month} / {year}")
    
    # CALENDAR RENDER LOGIC
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, current_month)
    
    weekdays = T["weekdays"]
    header_cols = st.columns(7)
    for i, day in enumerate(weekdays):
        header_cols[i].markdown(f'<div style="background:#4b6cb7; color:white; text-align:center; padding:10px; border-radius:5px; font-weight:bold;">{day}</div>', unsafe_allow_html=True)
    
    if not registrations.empty:
        registrations['Date'] = pd.to_datetime(registrations['Date'])
    
    for week in month_days:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                is_sunday = (i == 6)
                day_class = "calendar-day sunday-day" if is_sunday else "calendar-day"
                
                if day == 0:
                    st.markdown(f'<div class="{day_class} other-month"></div>', unsafe_allow_html=True)
                else:
                    target_date = date(year, current_month, day)
                    day_html = f'<div class="{day_class}"><span class="day-number">{day}</span>'
                    
                    if not registrations.empty:
                        day_regs = registrations[registrations['Date'].dt.date == target_date]
                        for _, row in day_regs.iterrows():
                            # Handle session translations if stored in Vietnamese but viewing in Korean
                            display_dept = row['Department']
                            display_timeslot = row['TimeSlot']
                            # Map morning/afternoon in display
                            display_timeslot = display_timeslot.replace("Sáng", T["morning"]).replace("Chiều", T["afternoon"])
                            
                            is_morning = "Sáng" in row['TimeSlot']
                            marker_class = "event-morning" if is_morning else "event-afternoon"
                            short_session = str(row["Session"]).split(":")[0] if ":" in str(row["Session"]) else row["Session"]
                            
                            if row.get('Status') == 'Completed':
                                status_text = "Đã học" if lang == "Tiếng Việt" else "교육 완료:"
                                day_html += f'<div class="event-marker event-completed">✅ <b>{row["Team"]}</b><br/>{status_text} {short_session}</div>'
                            else:
                                day_html += f'<div class="event-marker {marker_class}"><b>{display_dept} ({row["Team"]})</b><br/>📖 {short_session}<br/>⏱ {display_timeslot}<br/>👥 {row["Attendees"]} {T["people"]}</div>'
                    
                    day_html += '</div>'
                    st.markdown(day_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(T["legend"])

# --- ROADMAP PAGE ---
elif menu == T["menu_roadmap"]:
    st.markdown(f'<div class="main-header"><h1>{T["roadmap_title"]}</h1><p>{T["roadmap_subtitle"]}</p></div>', unsafe_allow_html=True)
    
    registrations = db.get_registrations(use_cache=False)
    if registrations.empty:
        st.info(T["no_data"])
    else:
        df = registrations.copy()
        df['Department'] = df['Department'].fillna("").astype(str).str.strip()
        df['Team'] = df['Team'].fillna("").astype(str).str.strip()
        
        # Filter empty or invalid rows
        df = df[(df['Department'] != "") & (df['Team'] != "")]
        
        if df.empty:
            st.info(T["no_data"])
        else:
            df = df.sort_values(by=['Department', 'Team', 'Date'])
            unique_teams = df[['Department', 'Team']].drop_duplicates().values.tolist()
            
            # UI Filters
            col_f1, col_f2 = st.columns([1, 2])
            with col_f1:
                depts_list = [T["roadmap_dept_all"]] + sorted(list(set(df['Department'].tolist())))
                selected_dept = st.selectbox(T["roadmap_dept"], depts_list)
            with col_f2:
                search_query = st.text_input(T["roadmap_search"], "").strip()
                
            # Filter teams
            filtered_teams = []
            for dept, team in unique_teams:
                if selected_dept != T["roadmap_dept_all"] and dept != selected_dept:
                    continue
                if search_query and search_query.lower() not in team.lower() and search_query.lower() not in dept.lower():
                    continue
                filtered_teams.append((dept, team))
                
            def parse_session_num(session_str):
                s = str(session_str).lower()
                if "buổi 1" in s or "1회차" in s or "buoi 1" in s:
                    return 1
                elif "buổi 2" in s or "2회차" in s or "buoi 2" in s:
                    return 2
                elif "buổi 3" in s or "3회차" in s or "buoi 3" in s:
                    return 3
                elif "buổi 4" in s or "4회차" in s or "buoi 4" in s:
                    return 4
                return None

            team_data = []
            total_teams_count = len(filtered_teams)
            completed_teams_count = 0
            in_progress_teams_count = 0
            
            for dept, team in filtered_teams:
                team_regs = df[(df['Department'] == dept) & (df['Team'] == team)]
                sessions_map = {1: None, 2: None, 3: None, 4: None}
                
                for _, row_reg in team_regs.iterrows():
                    sess_num = parse_session_num(row_reg['Session'])
                    if sess_num:
                        existing = sessions_map[sess_num]
                        if existing is None or (existing['Status'] != 'Completed' and row_reg['Status'] == 'Completed'):
                            sessions_map[sess_num] = row_reg
                        elif existing['Status'] == row_reg['Status']:
                            if str(row_reg['Date']) > str(existing['Date']):
                                sessions_map[sess_num] = row_reg

                completed_sessions = sum(1 for k, v in sessions_map.items() if v is not None and v['Status'] == 'Completed')
                scheduled_sessions = sum(1 for k, v in sessions_map.items() if v is not None and v['Status'] != 'Completed')
                
                if completed_sessions == 4:
                    completed_teams_count += 1
                elif completed_sessions > 0 or scheduled_sessions > 0:
                    in_progress_teams_count += 1
                    
                team_data.append({
                    'Department': dept,
                    'Team': team,
                    'sessions': sessions_map,
                    'completed_count': completed_sessions
                })
                
            # Calculate metrics
            total_registered_sessions = sum(sum(1 for v in item['sessions'].values() if v is not None) for item in team_data)
            total_completed_sessions = sum(item['completed_count'] for item in team_data)
            avg_progress = (total_completed_sessions / total_registered_sessions * 100) if total_registered_sessions > 0 else 0.0
            
            # Render Stats Cards
            st.markdown(f"""
            <div class="stats-container">
                <div class="stat-card" style="border-top: 4px solid #4b6cb7;">
                    <div class="stat-value">{total_teams_count}</div>
                    <div class="stat-label">{T['roadmap_kpi_total_teams']}</div>
                </div>
                <div class="stat-card" style="border-top: 4px solid #27ae60;">
                    <div class="stat-value">{completed_teams_count}</div>
                    <div class="stat-label">{T['roadmap_kpi_completed_sessions']}</div>
                </div>
                <div class="stat-card" style="border-top: 4px solid #f39c12;">
                    <div class="stat-value">{total_registered_sessions}</div>
                    <div class="stat-label">{T['roadmap_kpi_scheduled_sessions']}</div>
                </div>
                <div class="stat-card" style="border-top: 4px solid #9b59b6;">
                    <div class="stat-value">{avg_progress:.1f}%</div>
                    <div class="stat-label">{T['roadmap_kpi_avg_progress']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # HTML Table styles for a highly visual, modern 4-column roadmap display
            dept_header = "Các Bộ phận PLV<br/>PLV 부서"
            team_header = "Team"
            participation_header = "Tham gia?<br/>참가?"
            note_header = "Note"
            
            table_html = f"""
            <div style="overflow-x: auto;">
                <table class="progress-table" style="width:100%; border-collapse: collapse; margin-top:20px; font-family: sans-serif; background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #ddd;">
                    <thead>
                        <tr style="background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%); color: white; text-align: center; font-size: 0.9rem;">
                            <th style="padding: 14px 10px; text-align: center; width: 40px; border: 1px solid #ddd; color: white !important;">No</th>
                            <th style="padding: 14px 10px; text-align: center; width: 120px; border: 1px solid #ddd; color: white !important;">{dept_header}</th>
                            <th style="padding: 14px 10px; text-align: center; width: 160px; border: 1px solid #ddd; color: white !important;">{team_header}</th>
                            <th style="padding: 14px 10px; text-align: center; width: 85px; border: 1px solid #ddd; color: white !important;">{participation_header}</th>
                            <th style="padding: 14px 10px; text-align: center; width: 110px; border: 1px solid #ddd; color: white !important;">{T['sessions'][0].split(':')[0]}</th>
                            <th style="padding: 14px 10px; text-align: center; width: 110px; border: 1px solid #ddd; color: white !important;">{T['sessions'][1].split(':')[0]}</th>
                            <th style="padding: 14px 10px; text-align: center; width: 110px; border: 1px solid #ddd; color: white !important;">{T['sessions'][2].split(':')[0]}</th>
                            <th style="padding: 14px 10px; text-align: center; width: 110px; border: 1px solid #ddd; color: white !important;">{T['sessions'][3].split(':')[0]}</th>
                            <th style="padding: 14px 10px; text-align: center; width: 160px; border: 1px solid #ddd; color: white !important;">{note_header}</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            for i, item in enumerate(team_data):
                dept_val = item['Department']
                team_val = item['Team']
                sessions = item['sessions']
                completed_sessions = item['completed_count']
                
                bg_color = "#ffffff" if i % 2 == 0 else "#fcfcfc"
                session_cells = []
                notes = []
                
                for s_idx in range(1, 5):
                    row_data = sessions[s_idx]
                    if row_data is not None:
                        date_str = str(row_data['Date'])
                        try:
                            dt = datetime.strptime(date_str, "%Y-%m-%d")
                            formatted_date = dt.strftime("%Y-%m-%d")
                        except:
                            formatted_date = date_str
                            
                        status = row_data.get('Status', 'Pending')
                        attendees = int(row_data['Attendees'])
                        actual = row_data.get('ActualAttendees', "")
                        
                        row_note = row_data.get('Note', "")
                        if pd.notna(row_note) and str(row_note).strip() != "" and str(row_note).lower() != "nan":
                            notes.append(str(row_note).strip())
                        
                        if status == 'Completed':
                            actual_str = str(actual).strip()
                            if actual_str == "" or actual_str.lower() == "nan" or pd.isna(actual):
                                display_att = f"{attendees}/{attendees}"
                            else:
                                try:
                                    display_att = f"{int(float(actual_str))}/{attendees}"
                                except:
                                    display_att = f"{actual_str}/{attendees}"
                                    
                            cell_html = f"""
                            <td style="padding: 10px 4px; text-align: center; vertical-align: middle; background-color: #d4edda; border: 1px solid #ddd; font-size: 0.8rem; line-height: 1.35;">
                                <span style="color: #155724; font-weight: bold;">✅ {T['status_completed'].split(' / ')[0]}</span><br/>
                                <span style="color: #155724; font-weight: 500;">{formatted_date}</span><br/>
                                <span style="color: #155724; font-weight: bold;">👥 {display_att}</span>
                            </td>
                            """
                        else:
                            people_label = "người" if lang == "Tiếng Việt" else "명"
                            cell_html = f"""
                            <td style="padding: 10px 4px; text-align: center; vertical-align: middle; background-color: #fff3e0; border: 1px solid #ddd; font-size: 0.8rem; line-height: 1.35;">
                                <span style="color: #e65100; font-weight: bold;">📅 {T['status_scheduled'].split(' / ')[0]}</span><br/>
                                <span style="color: #e65100; font-weight: 500;">{formatted_date}</span><br/>
                                <span style="color: #e65100; font-weight: bold;">👥 {attendees} {people_label}</span>
                            </td>
                            """
                    else:
                        cell_html = f"""
                        <td style="padding: 10px 4px; text-align: center; vertical-align: middle; background-color: #ffffff; border: 1px solid #ddd; color: #ccc; font-size: 0.8rem; line-height: 1.35;">
                            <span style="color: #999;">--</span><br/>
                            <span style="color: #bbb;">{T['status_not_scheduled'].split(' / ')[0]}</span>
                        </td>
                        """
                    session_cells.append(cell_html)
                
                # Show only manual notes entered in the database
                combined_notes_str = "<br/>".join(notes) if notes else ""
                participation_val = "Yes" if lang == "Tiếng Việt" else "예"
                
                row_html = f"""
                <tr style="background: {bg_color}; border-bottom: 1px solid #ddd; transition: background 0.2s;">
                    <td style="padding: 10px 8px; font-weight: bold; color: #666; text-align: center; border: 1px solid #ddd;">{i+1}</td>
                    <td style="padding: 10px 8px; font-weight: bold; color: #182848; border: 1px solid #ddd;">{dept_val}</td>
                    <td style="padding: 10px 8px; font-weight: 600; color: #333; border: 1px solid #ddd;">{team_val}</td>
                    <td style="padding: 10px 8px; text-align: center; font-weight: bold; color: #2e7d32; border: 1px solid #ddd; background-color: #f9f9f9;">{participation_val}</td>
                    {session_cells[0]}
                    {session_cells[1]}
                    {session_cells[2]}
                    {session_cells[3]}
                    <td style="padding: 10px 8px; font-size: 0.8rem; color: #333333; font-weight: 500; max-width: 160px; word-wrap: break-word; vertical-align: middle; border: 1px solid #ddd;">{combined_notes_str}</td>
                </tr>
                """
                table_html += row_html
                
            table_html += """
                    </tbody>
                </table>
            </div>
            """
            # Loại bỏ các ký tự xuống dòng và khoảng trắng thừa để tránh trình phân tích cú pháp Markdown của Streamlit hiểu nhầm thành khối code
            clean_table_html = "".join([line.strip() for line in table_html.split("\n")])
            st.markdown(clean_table_html, unsafe_allow_html=True)

# --- REGISTRATION PAGE ---
elif menu == T["menu_reg"]:
    st.markdown(f"## {T['reg_title']}")
    st.warning(T["reg_note"])
    
    min_date = date(2026, 5, 1)
    max_date = date(2026, 7, 31)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("registration_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                dept_options = ["Kỹ thuật", "Sản xuất", "QC", "RD", "Kinh doanh", "Kế toán", "Kho", "Khác (tự nhập)"]
                if lang == "한국어":
                    dept_options_kr = ["기술", "생산", "QC", "RD", "영업", "회계", "창고", "기타 (직접 입력)"]
                    dept_selection = st.selectbox(T["dept"], dept_options_kr)
                else:
                    dept_selection = st.selectbox(T["dept"], dept_options)
                
                final_dept = dept_selection
                if "Khác" in dept_selection or "기타" in dept_selection:
                    final_dept = st.text_input(T["placeholder_dept"], placeholder=T["placeholder_dept"])
                
                team_name = st.text_input(T["team"], placeholder=T["placeholder_team"])
                session_type = st.selectbox(T["session"], T["sessions"])
                attendees = st.number_input(T["attendees"], min_value=1, max_value=200, value=5)
            with col2:
                training_date = st.date_input(T["date"], value=min_date, min_value=min_date, max_value=max_date)
                st.write(T["timeslot"])
                
                period = st.radio(T["period"], [f'{T["morning"]} (09:30)', f'{T["afternoon"]} (13:30)'], horizontal=True)
                
                # Standardize storage to Vietnamese for morning/afternoon to maintain DB consistency
                if period.startswith(T["morning"]):
                    storage_period = "Sáng"
                    exact_time = "09:30"
                else:
                    storage_period = "Chiều"
                    exact_time = "13:30"
                
                final_timeslot = f"{storage_period} {exact_time}"
                
            submitted = st.form_submit_button(T["submit"])
            if submitted:
                if team_name and final_dept:
                    db.save_registration(final_dept, team_name, session_type, "", training_date, final_timeslot, attendees)
                    st.success(T["success"])
                else:
                    st.error(T["error"])
        st.markdown('</div>', unsafe_allow_html=True)

# --- TRAINERS PAGE ---
elif menu == T["menu_trainers"]:
    st.markdown(f"## {T['trainer_title']}")
    
    dyn_trainers_df = db.get_trainers()
    dynamic_trainers = []
    if not dyn_trainers_df.empty:
        for _, row in dyn_trainers_df.iterrows():
            dynamic_trainers.append({
                "name": row['Name'],
                "role_vn": row['Role_VN'],
                "role_kr": row['Role_KR'],
                "team": row['Team'],
                "desc": row['Desc'],
                "image": row.get('ImageFile', "")
            })
    
    all_trainers = TRAINERS + dynamic_trainers
    
    cols = st.columns(2)
    for idx, trainer in enumerate(all_trainers):
        with cols[idx % 2]:
            image_html = '<div class="trainer-avatar">👤</div>'
            t_img = trainer.get('image', "")
            if t_img and str(t_img) != 'nan' and t_img != "":
                img_path = os.path.join("images", str(t_img))
                if os.path.exists(img_path):
                    import base64
                    with open(img_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode()
                    image_html = f'<img src="data:image/png;base64,{encoded_string}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;">'
            
            st.markdown(f"""
            <div class="trainer-card">
                <div style="display: flex; align-items: center;">
                    {image_html}
                    <div style="margin-left: 15px;">
                        <h3 style="margin: 0; color: #4b6cb7;">{trainer['name']}</h3>
                        <p style="margin: 2px 0; font-weight: bold; color: #31333F;">{trainer['role_vn'] if lang == "Tiếng Việt" else trainer['role_kr']}</p>
                        <p style="margin: 0; font-size: 0.9rem; color: #666;">{trainer['team']}</p>
                    </div>
                </div>
                <hr style="margin: 10px 0; border: 0.5px solid #eee;">
                <p style="font-size: 0.95rem; line-height: 1.4; color: #444;">{trainer['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

# --- DOCUMENTS PAGE ---
elif menu == T["menu_docs"]:
    st.markdown(f'<div class="main-header"><h1>{T["docs_title"]}</h1></div>', unsafe_allow_html=True)
    
    if not st.session_state.docs_authenticated:
        st.info("🔐 Vui lòng nhập mật khẩu để truy cập tài liệu công ty. / 회사 자료에 접근하려면 비밀번호를 입력하세요.")
        doc_password = st.text_input(T["password"], type="password", key="doc_pass_input")
        if st.button("Truy cập / 접속"):
            if doc_password == "plv2026":
                st.session_state.docs_authenticated = True
                st.rerun()
            else:
                st.error("Mật khẩu không chính xác. / 비밀번호가 틀렸습니다.")
    else:
        if st.button("🔒 Khóa tài liệu / 자료 잠금"):
            st.session_state.docs_authenticated = False
            st.rerun()
        
        docs = db.get_documents()
        if docs.empty:
            st.info(T["docs_no_data"])
        else:
            categories = [
                "Tài liệu chung / 일반 자료", 
                "Lý thuyết / 이론 자료", 
                "Ví dụ thực hành / 실습 예제", 
                "Bài tập các Bộ phận / 부서별 과제",
                "Nhật ký đào tạo / 교육 일지"
            ]
            
            # List of categories that should be grouped by team
            group_by_team_cats = [
                "Ví dụ thực hành / 실습 예제", 
                "Bài tập các Bộ phận / 부서별 과제",
                "Nhật ký đào tạo / 교육 일지"
            ]
            
            for cat in categories:
                st.markdown(f"#### 📂 {cat}")
                cat_docs = docs[docs['Category'] == cat]
                
                if cat_docs.empty:
                    st.markdown(f"<span style='color: gray; font-style: italic;'>{T['docs_no_data']}</span>", unsafe_allow_html=True)
                else:
                    if cat in group_by_team_cats:
                        # Grouping by team for these categories
                        teams_in_cat = sorted(cat_docs['Team'].unique())
                        for team_name in teams_in_cat:
                            with st.expander(f"📁 Team: {team_name}"):
                                team_docs = cat_docs[cat_docs['Team'] == team_name]
                                for idx, row in team_docs.iterrows():
                                    st.markdown(f"**📄 {row['Title']}**")
                                    st.write(f"_{row['Description']}_")
                                    doc_url = row.get('FileURL', '#')
                                    st.markdown(f'<a href="{doc_url}" target="_blank" class="download-link">📥 {T["doc_download"]}</a>', unsafe_allow_html=True)
                                    if idx < team_docs.index[-1]: st.markdown("<hr style='margin:10px 0; border:0.1px solid #eee;'>", unsafe_allow_html=True)
                    else:
                        # Normal flat listing for other categories
                        for idx, row in cat_docs.iterrows():
                            with st.expander(f"📄 {row['Title']}"):
                                st.write(f"**{T['doc_desc']}:** {row['Description']}")
                                st.write(f"**{T['doc_date']}:** {row['UploadDate']}")
                                doc_url = row.get('FileURL', '#')
                                st.markdown(f'<a href="{doc_url}" target="_blank" class="download-link">📥 {T["doc_download"]}</a>', unsafe_allow_html=True)
                st.markdown("---")

# --- ADMIN PAGE ---
elif menu == T["menu_admin"]:
    st.markdown(f"## {T['admin_title']}")
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        password = st.text_input(T["password"], type="password")
        if st.button("Đăng nhập / 로그인"):
            if password == "admin123":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Mật khẩu không chính xác." if lang == "Tiếng Việt" else "비밀번호가 틀렸습니다.")
    else:
        st.success(T["auth_success"])
        if st.button("🚪 Đăng xuất / 로그아웃"):
            st.session_state.authenticated = False
            st.rerun()
            
        tab_list, tab_roadmap_edit, tab_manage, tab_docs, tab_trainers = st.tabs([
            T["tab_list"], 
            "🎯 Quản lý Tiến độ các Team" if lang == "Tiếng Việt" else "🎯 팀별 진도 관리",
            "📅 Quản lý Lịch đào tạo" if lang == "Tiếng Việt" else "📅 교육 일정 관리",
            T["tab_docs"], 
            "👨‍🏫 Quản lý Giảng viên" if lang == "Tiếng Việt" else "👨‍🏫 강사 관리"
        ])
        
        registrations = db.get_registrations(use_cache=False)
        
        with tab_list:
            st.markdown(f"### {T['list_title']}")
            if not registrations.empty:
                display_df = registrations[['Date', 'TimeSlot', 'Department', 'Team', 'Session', 'Attendees']].copy()
                display_df['TimeSlot'] = display_df['TimeSlot'].apply(lambda x: x.replace("Sáng", T["morning"]).replace("Chiều", T["afternoon"]))
                
                display_df.columns = [
                    'Ngày' if lang == "Tiếng Việt" else '날짜', 
                    'Giờ' if lang == "Tiếng Việt" else '시간', 
                    'Bộ phận' if lang == "Tiếng Việt" else '부서', 
                    'Team', 
                    'Nội dung' if lang == "Tiếng Việt" else '교육 내용', 
                    'Số người' if lang == "Tiếng Việt" else '인원'
                ]
                st.dataframe(display_df.sort_values(by=display_df.columns[0]), use_container_width=True, hide_index=True)
                
                csv = registrations.to_csv(index=False).encode('utf-8-sig')
                st.download_button(T["download"], csv, "lich_dao_tao_tong_hop.csv", "text/csv")
                
                # Nút đồng bộ dữ liệu local lên Google Sheets
                st.markdown("---")
                st.markdown("### 🔄 Đồng bộ hóa Dữ liệu / 데이터 동기화")
                st.info("Hệ thống hỗ trợ đồng bộ hai chiều giữa file CSV local và Google Sheets trực tuyến. / 로컬 CSV 파일과 구글 시트 간의 양방향 동기화를 지원합니다.")
                
                col_sync1, col_sync2 = st.columns(2)
                with col_sync1:
                    st.markdown("##### 📤 Tải lên Cloud (Push)")
                    st.caption("Tải dữ liệu từ file local lên Google Sheets (Ghi đè Cloud)")
                    if st.button("🔄 Local sang Google Sheets / Push to Sheets"):
                        with st.spinner("Đang đồng bộ... / 동기화 중..."):
                            try:
                                if db.sync_local_to_sheets():
                                    st.success("✅ Đồng bộ thành công! Google Sheets đã được cập nhật dữ liệu mới nhất. / 동기화가 완료되었습니다!")
                                    st.rerun()
                                else:
                                    st.error("❌ Không tìm thấy file dữ liệu local. / 로컬 파일을 찾을 수 없습니다.")
                            except Exception as e:
                                st.error(f"❌ Lỗi đồng bộ: {e}")
                                
                with col_sync2:
                    st.markdown("##### 📥 Tải xuống Local (Pull)")
                    st.caption("Tải dữ liệu từ Google Sheets xuống file local (Ghi đè Local)")
                    if st.button("📥 Google Sheets về Local / Pull to Local"):
                        with st.spinner("Đang tải dữ liệu... / 다운로드 중..."):
                            try:
                                if db.sync_sheets_to_local():
                                    st.success("✅ Tải dữ liệu thành công! File local đã được cập nhật từ Google Sheets. / 다운로드 완료되었습니다!")
                                    st.rerun()
                                else:
                                    st.error("❌ Không tải được dữ liệu từ Google Sheets.")
                            except Exception as e:
                                st.error(f"❌ Lỗi tải dữ liệu: {e}")
            else:
                st.info(T["no_data"])
                
        with tab_roadmap_edit:
            st.markdown(f"### {'🎯 Quản lý & Chỉnh sửa Tiến độ các Team' if lang == 'Tiếng Việt' else '🎯 팀별 진도 관리 및 수정'}")
            st.info("Chọn Bộ phận và Team để chỉnh sửa nhanh lộ trình 4 buổi học. / 부서와 팀을 선택하여 4회차 교육 진도를 신속하게 수정하세요.")
            
            def parse_session_num_edit(session_str):
                s = str(session_str).lower()
                if "buổi 1" in s or "1회차" in s or "buoi 1" in s:
                    return 1
                elif "buổi 2" in s or "2회차" in s or "buoi 2" in s:
                    return 2
                elif "buổi 3" in s or "3회차" in s or "buoi 3" in s:
                    return 3
                elif "buổi 4" in s or "4회차" in s or "buoi 4" in s:
                    return 4
                return None

            if not registrations.empty:
                # Lọc các đăng ký hợp lệ
                valid_regs = registrations.copy()
                valid_regs['Department'] = valid_regs['Department'].fillna("").astype(str).str.strip()
                valid_regs['Team'] = valid_regs['Team'].fillna("").astype(str).str.strip()
                valid_regs = valid_regs[(valid_regs['Department'] != "") & (valid_regs['Team'] != "")]
                
                if valid_regs.empty:
                    st.info(T["no_data"])
                else:
                    col_sel1, col_sel2 = st.columns(2)
                    with col_sel1:
                        depts_edit = sorted(list(set(valid_regs['Department'].tolist())))
                        selected_dept_edit = st.selectbox("1. Chọn Bộ phận / 부서 선택:", depts_edit, key="edit_rm_dept_sel")
                    with col_sel2:
                        teams_edit = sorted(list(set(valid_regs[valid_regs['Department'] == selected_dept_edit]['Team'].tolist())))
                        selected_team_edit = st.selectbox("2. Chọn Team / 팀 선택:", teams_edit, key="edit_rm_team_sel")
                    
                    st.markdown("---")
                    st.markdown(f"#### 🎯 Lộ trình của Team: **{selected_team_edit}** ({selected_dept_edit})")
                    
                    # Lấy đăng ký của Team
                    team_regs_edit = valid_regs[(valid_regs['Department'] == selected_dept_edit) & (valid_regs['Team'] == selected_team_edit)]
                    
                    sessions_map_edit = {1: None, 2: None, 3: None, 4: None}
                    for idx, row in team_regs_edit.iterrows():
                        sess_num = parse_session_num_edit(row['Session'])
                        if sess_num:
                            sessions_map_edit[sess_num] = (idx, row)
                            
                    for s_idx in range(1, 5):
                        session_str = T["sessions"][s_idx - 1]
                        
                        st.markdown(f"##### **Buổi {s_idx}: {session_str.split(' / ')[0]}**")
                        
                        session_data = sessions_map_edit[s_idx]
                        if session_data is not None:
                            idx, row = session_data
                            status_label = "🟢 **Đã hoàn thành / 이수완료**" if row['Status'] == 'Completed' else "🔵 **Đang lên lịch / 교육예정**"
                            st.markdown(status_label)
                            if row['Status'] != 'Completed':
                                if st.button("✅ Hoàn thành nhanh / 빠른 완료", key=f"quick_comp_vertical_{s_idx}_{idx}"):
                                    p_att = int(row['Attendees'])
                                    if db.update_registration(idx, row['Department'], row['Team'], row['Session'], row['Content'], row['Date'], row['TimeSlot'], p_att, "Completed", str(p_att), str(row.get('Note', '') if pd.notna(row.get('Note')) else '')):
                                        st.success("Đã hoàn thành! / 완료되었습니다!")
                                        st.rerun()
                            
                            with st.form(key=f"quick_edit_vertical_{s_idx}_{idx}"):
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    edit_dept = st.text_input("Bộ phận / 부서:", value=row['Department'], key=f"q_dept_{s_idx}_{idx}")
                                    edit_team = st.text_input("Team / 팀명:", value=row['Team'], key=f"q_team_{s_idx}_{idx}")
                                    st.text_input("Nội dung / 회차:", value=row['Session'], disabled=True, key=f"q_sess_{s_idx}_{idx}")
                                with col2:
                                    try:
                                        p_date = datetime.strptime(row['Date'], "%Y-%m-%d").date()
                                    except:
                                        p_date = date(2026, 5, 1)
                                    edit_date = st.date_input("Ngày học / 날짜:", value=p_date, key=f"q_date_{s_idx}_{idx}")
                                    edit_timeslot = st.text_input("Giờ học / 시간:", value=row['TimeSlot'], key=f"q_time_{s_idx}_{idx}")
                                    edit_att = st.number_input("Kế hoạch / kế hoạch (명):", min_value=1, value=int(row['Attendees']), key=f"q_att_{s_idx}_{idx}")
                                with col3:
                                    edit_status = st.checkbox("Đã hoàn thành (Completed)", value=(row.get('Status') == 'Completed'), key=f"q_status_{s_idx}_{idx}")
                                    
                                    actual_val = row.get('ActualAttendees', "")
                                    if pd.isna(actual_val) or str(actual_val).strip() == "" or str(actual_val).lower() == "nan":
                                        actual_val_num = edit_att
                                    else:
                                        try:
                                            actual_val_num = int(float(actual_val))
                                        except:
                                            actual_val_num = edit_att
                                    edit_actual = st.number_input("Thực tế / 실제 (명):", min_value=0, value=actual_val_num, key=f"q_actual_{s_idx}_{idx}")
                                    edit_note = st.text_input("Ghi chú / 비고:", value=str(row.get('Note', "") if pd.notna(row.get('Note')) else ""), key=f"q_note_{s_idx}_{idx}")
                                
                                c_form_btn1, c_form_btn2 = st.columns([1, 5])
                                with c_form_btn1:
                                    save_btn = st.form_submit_button("💾 Lưu / 저장")
                                    if save_btn:
                                        status_val = "Completed" if edit_status else "Pending"
                                        actual_to_save = str(int(edit_actual)) if status_val == "Completed" else ""
                                        if db.update_registration(idx, edit_dept, edit_team, row['Session'], row['Content'], edit_date, edit_timeslot, edit_att, status_val, actual_to_save, edit_note):
                                            st.success("Đã lưu! / 저장완료!")
                                            st.rerun()
                            
                            # Nút xóa đặt ở ngoài form
                            if st.button("🗑️ Xóa buổi học / 삭제", key=f"q_del_vert_{s_idx}_{idx}"):
                                if db.delete_registration(idx):
                                    st.success("Đã xóa! / 삭제완료!")
                                    st.rerun()
                        else:
                            st.markdown("⚪ **Chưa đăng ký / 미신청**")
                            with st.form(key=f"quick_add_vertical_{s_idx}"):
                                col_add1, col_add2, col_add3 = st.columns(3)
                                with col_add1:
                                    st.text_input("Bộ phận / 부서:", value=selected_dept_edit, disabled=True, key=f"q_add_dept_{s_idx}")
                                    st.text_input("Team / 팀명:", value=selected_team_edit, disabled=True, key=f"q_add_team_{s_idx}")
                                with col_add2:
                                    add_date = st.date_input("Ngày học / 날짜:", value=date(2026, 5, 1), key=f"q_add_date_{s_idx}")
                                    period_choice = st.radio("Buổi / 구분:", ["Sáng (09:30)", "Chiều (13:30)"], key=f"q_add_period_{s_idx}", horizontal=True)
                                    add_timeslot = "Sáng 09:30" if "Sáng" in period_choice else "Chiều 13:30"
                                with col_add3:
                                    add_att = st.number_input("Số người / 인원:", min_value=1, value=6, key=f"q_add_att_{s_idx}")
                                    
                                if st.form_submit_button("➕ Lên lịch Buổi học / 일정 추가"):
                                    db.save_registration(selected_dept_edit, selected_team_edit, session_str, "", add_date, add_timeslot, add_att)
                                    st.success("Đã thêm lịch! / 추가완료!")
                                    st.rerun()
                                    
                        st.markdown("<hr style='margin: 1.5rem 0; border: 0.5px solid #eee;'>", unsafe_allow_html=True)
            else:
                st.info(T["no_data"])



        with tab_manage:
            st.markdown(f"### {'📅 Quản lý & Xóa Lịch đào tạo' if lang == 'Tiếng Việt' else '📅 교육 일정 관리 및 삭제'}")
            st.info("Khu vực quản lý, chỉnh sửa hoặc xóa bất kỳ buổi học nào trong danh sách tổng hợp. / 전체 신청 목록에서 모든 교육 일정을 관리, 수정 hoặc 삭제할 수 있는 공간입니다.")
            
            if not registrations.empty:
                col_filt1, col_filt2 = st.columns(2)
                with col_filt1:
                    search_query = st.text_input("🔍 Tìm kiếm theo Bộ phận/Team/Nội dung / 부서/팀/내용 검색:", key="manage_search_query").strip().lower()
                with col_filt2:
                    sort_order = st.selectbox("↕️ Sắp xếp theo ngày / 날짜 정렬:", ["Mới nhất trước / 최신순", "Cũ nhất trước / 오래된순"], key="manage_sort_order")
                
                filtered_regs = registrations.copy()
                if search_query:
                    filtered_regs = filtered_regs[
                        filtered_regs['Department'].fillna("").astype(str).str.lower().str.contains(search_query) |
                        filtered_regs['Team'].fillna("").astype(str).str.lower().str.contains(search_query) |
                        filtered_regs['Session'].fillna("").astype(str).str.lower().str.contains(search_query) |
                        filtered_regs['Date'].fillna("").astype(str).str.lower().str.contains(search_query)
                    ]
                
                if sort_order == "Mới nhất trước / 최신순":
                    filtered_regs = filtered_regs.sort_values(by='Date', ascending=False)
                else:
                    filtered_regs = filtered_regs.sort_values(by='Date', ascending=True)
                
                if filtered_regs.empty:
                    st.info("Không tìm thấy kết quả phù hợp. / 검색 결과가 없습니다.")
                else:
                    for index, row in filtered_regs.iterrows():
                        display_time = row['TimeSlot'].replace("Sáng", T["morning"]).replace("Chiều", T["afternoon"])
                        with st.expander(f"📌 [{row['Date']}] - {row['Department']} ({row['Team']}) - {row['Session']}"):
                            with st.form(key=f"edit_general_form_{index}"):
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    edit_dept = st.text_input(T["dept"], value=row['Department'], key=f"gen_dept_{index}")
                                    edit_team = st.text_input(T["team"], value=row['Team'], key=f"gen_team_{index}")
                                    edit_session = st.selectbox(T["session"], T["sessions"], index=T["sessions"].index(row['Session']) if row['Session'] in T["sessions"] else 0, key=f"gen_sess_{index}")
                                with col2:
                                    try:
                                        p_date = datetime.strptime(row['Date'], "%Y-%m-%d").date()
                                    except:
                                        p_date = date(2026, 5, 1)
                                    edit_date = st.date_input(T["date"], value=p_date, key=f"gen_date_{index}")
                                    edit_timeslot = st.text_input(T["timeslot"], value=row['TimeSlot'], key=f"gen_time_{index}")
                                    edit_att = st.number_input(T["attendees"], min_value=1, value=int(row['Attendees']), key=f"gen_att_{index}")
                                with col3:
                                    edit_status = st.checkbox("Đã hoàn thành / 이수완료", value=(row.get('Status') == 'Completed'), key=f"gen_status_{index}")
                                    
                                    actual_val = row.get('ActualAttendees', "")
                                    if pd.isna(actual_val) or str(actual_val).strip() == "" or str(actual_val).lower() == "nan":
                                        actual_val_num = edit_att
                                    else:
                                        try:
                                            actual_val_num = int(float(actual_val))
                                        except:
                                            actual_val_num = edit_att
                                            
                                    edit_actual = st.number_input("Thực tế / 실제 (명):", min_value=0, value=actual_val_num, key=f"gen_actual_{index}")
                                    edit_note = st.text_input("Ghi chú / 비고:", value=str(row.get('Note', "") if pd.notna(row.get('Note')) else ""), key=f"gen_note_{index}")
                                
                                c_form_btn1, c_form_btn2 = st.columns([1, 5])
                                with c_form_btn1:
                                    if st.form_submit_button("💾 Lưu / 저장"):
                                        status_val = "Completed" if edit_status else "Pending"
                                        actual_to_save = str(int(edit_actual)) if status_val == "Completed" else ""
                                        if db.update_registration(index, edit_dept, edit_team, edit_session, "", edit_date, edit_timeslot, edit_att, status_val, actual_to_save, edit_note):
                                            st.success("Đã cập nhật lịch thành công! / 성공적으로 업데이트되었습니다!")
                                            st.rerun()
                                            
                            # Operations placed outside form: Quick complete & Delete
                            col_ops1, col_ops2 = st.columns([1, 5])
                            with col_ops1:
                                if row['Status'] != 'Completed':
                                    if st.button("✅ Hoàn thành nhanh", key=f"gen_quick_comp_{index}"):
                                        p_att = int(row['Attendees'])
                                        if db.update_registration(index, row['Department'], row['Team'], row['Session'], row['Content'], row['Date'], row['TimeSlot'], p_att, "Completed", str(p_att), str(row.get('Note', '') if pd.notna(row.get('Note')) else '')):
                                            st.success("Đã hoàn thành! / 완료되었습니다!")
                                            st.rerun()
                            with col_ops2:
                                if st.button("🗑️ " + T["delete_btn"], key=f"gen_del_{index}"):
                                    if db.delete_registration(index):
                                        st.success("Đã xóa lịch thành công! / 성공적으로 삭제되었습니다!")
                                        st.rerun()
            else:
                st.info(T["no_data"])


        with tab_docs:
            st.markdown(f"### {T['tab_docs']}")
            
            with st.form("upload_doc_form", clear_on_submit=True):
                st.write(T["doc_upload"])
                doc_name = st.text_input(T["doc_name"])
                doc_desc = st.text_area(T["doc_desc"])
                categories = [
                    "Tài liệu chung / 일반 자료", 
                    "Lý thuyết / 이론 자료", 
                    "Ví dụ thực hành / 실습 예제", 
                    "Bài tập các Bộ phận / 부서별 과제",
                    "Nhật ký đào tạo / 교육 일지"
                ]
                doc_cat = st.selectbox(T["doc_cat"], categories)
                
                # Dynamic team selection from existing registrations
                registrations_inner = db.get_registrations()
                existing_teams = sorted(registrations_inner['Team'].unique().tolist()) if not registrations_inner.empty else []
                other_label = "Khác (Tự nhập) / 기타 (직접 입력)"
                
                group_by_team_cats = [
                    "Ví dụ thực hành / 실습 예제", 
                    "Bài tập các Bộ phận / 부서별 과제",
                    "Nhật ký đào tạo / 교육 일지"
                ]
                
                final_doc_team = "Chung"
                if doc_cat in group_by_team_cats:
                    team_options = existing_teams + [other_label]
                    selected_team = st.selectbox("Chọn Team cho tài liệu / Team 선택:", team_options)
                    if selected_team == other_label:
                        final_doc_team = st.text_input("Nhập tên Team mới / 새 Team 이름 입력:")
                    else:
                        final_doc_team = selected_team

                doc_url = st.text_input("Link tài liệu (Google Drive...) / 자료 링크 (구글 드라이브...)")
                
                submit_doc = st.form_submit_button(T["doc_upload"])
                if submit_doc and doc_url and doc_name:
                    db.save_document(doc_name, doc_desc, doc_url, doc_cat, final_doc_team)
                    st.success(T["doc_success"])
            
            st.markdown("---")
            docs = db.get_documents(use_cache=False)
            if not docs.empty:
                for index, row in docs.iterrows():
                    with st.expander(f"📄 {row['Title']} ({row['Category']})"):
                        st.write(f"**Link:** {row.get('FileURL', 'No Link')}")
                        if st.button(f"🗑️ {T['delete_btn']}", key=f"del_doc_{index}"):
                            if db.delete_document(index):
                                st.rerun()
            else:
                st.info(T["no_data"])
                
        with tab_trainers:
            st.markdown(f"### {'Thêm giảng viên mới' if lang == 'Tiếng Việt' else '새 강사 추가'}")
            
            with st.form("add_trainer_form", clear_on_submit=True):
                t_name = st.text_input("Tên / 이름")
                t_role_vn = st.text_input("Chức danh (VN) / 직함 (VN)")
                t_role_kr = st.text_input("Chức danh (KR) / 직함 (KR)")
                t_team = st.text_input("Team / 팀")
                t_desc = st.text_area("Mô tả / 설명")
                t_image = st.file_uploader("Ảnh chân dung / 프로필 사진 (Tùy chọn/선택사항)", type=['png', 'jpg', 'jpeg'])
                
                submit_trainer = st.form_submit_button("Thêm Giảng viên / 강사 추가")
                if submit_trainer and t_name:
                    image_filename = ""
                    if t_image is not None:
                        image_filename = t_image.name
                        if not os.path.exists("images"):
                            os.makedirs("images")
                        with open(os.path.join("images", image_filename), "wb") as f:
                            f.write(t_image.getbuffer())
                    
                    db.save_trainer(t_name, t_role_vn, t_role_kr, t_team, t_desc, image_filename)
                    st.success("Thêm thành công! / 성공적으로 추가되었습니다!")
                    
            st.markdown("---")
            dyn_trainers = db.get_trainers()
            if not dyn_trainers.empty:
                for index, row in dyn_trainers.iterrows():
                    with st.expander(f"👤 {row['Name']} - {row['Team']}"):
                        st.write(f"**Chức danh:** {row['Role_VN']} / {row['Role_KR']}")
                        st.write(f"**Mô tả:** {row['Desc']}")
                        if row.get('ImageFile') and str(row.get('ImageFile')) != 'nan':
                            st.write(f"**Ảnh:** {row['ImageFile']}")
                        if st.button("🗑️ Xóa / 삭제", key=f"del_trainer_{index}"):
                            if db.delete_trainer(index):
                                st.rerun()
            else:
                st.info("Chưa có giảng viên được thêm mới. / 추가된 강사가 없습니다.")
