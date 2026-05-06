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
        "menu_reg": "📝 Đăng ký Đào tạo / 교육 신청",
        "menu_trainers": "👨‍🏫 Giảng viên / 강사 정보",
        "menu_docs": "📚 Tài liệu / 교육 자료",
        "menu_admin": "🔐 Quản trị viên / 관리자",
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
        "error": "⚠️ Vui lòng điền đủ thông tin. / mọi thông tin đều được yêu cầu.",
        "admin_title": "🔐 Khu vực Quản trị viên / 관리자 전용",
        "password": "Nhập mật khẩu / 비밀번호를 입력하세요:",
        "auth_success": "Xác thực thành công! / 인증 성공!",
        "tab_list": "📊 Danh sách Tổng hợp / 전체 목록",
        "tab_manage": "🗑️ Quản lý & Xóa / quản lý và xóa",
        "tab_docs": "📂 Quản lý Tài liệu / quản lý tài liệu",
        "list_title": "📊 Toàn bộ danh sách đăng ký / Toàn bộ danh sách đăng ký",
        "download": "📥 Tải xuống (CSV) / tải xuống",
        "no_data": "Chưa có dữ liệu. / Không có dữ liệu.",
        "delete_title": "🗑️ Xóa bản đăng ký / Xóa bản đăng ký",
        "delete_btn": "Xóa / Xóa",
        "placeholder_team": "Ví dụ: Kỹ thuật... / Ví dụ: kỹ thuật...",
        "placeholder_time": "Ví dụ: 09:00...",
        "placeholder_dept": "Ví dụ: Bảo vệ... / Ví dụ: bảo vệ...",
        "people": "người / người",
        "sessions": ["Buổi 1: Lý thuyết / 1회차: 이론", "Buổi 2: Thực hành cơ bản / 2회차: 기본 실습", "Buổi 3: Thực hành nâng cao / 3회차: 심화 실습", "Buổi 4: Chia sẻ bài tập / 4회차: 과제 공유"],
        "stats_title": "📊 Tóm tắt tình hình đăng ký",
        "stat_total_regs": "Lượt đăng ký",
        "stat_depts": "Bộ phận tham gia",
        "stat_total_people": "Tổng số nhân viên",
        "participating_depts_list": "Các Bộ phận đã tham gia:",
        "trainer_title": "👨‍🏫 Đội ngũ Giảng viên AI / Đội ngũ giảng viên AI",
        "docs_title": "📚 Kho tài liệu đào tạo / Kho tài liệu đào tạo",
        "docs_no_data": "Chưa có dữ liệu tài liệu. / Không có tài liệu.",
        "doc_upload": "Tải lên tài liệu mới / Tải lên tài liệu mới",
        "doc_name": "Tên tài liệu / Tên tài liệu",
        "doc_desc": "Mô tả ngắn / Mô tả ngắn",
        "doc_cat": "Danh mục / Danh mục",
        "doc_file": "Chọn file tài liệu / Chọn file tài liệu",
        "doc_date": "Ngày đăng / Ngày đăng",
        "doc_success": "Tải lên thành công! / Tải lên thành công!",
        "doc_download": "Tải về / Tải về"
    },
    "한국어": {
        "sidebar_title": "🛠 Quản lý Đào tạo / 교육 관리",
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
        "doc_download": "다운로드 / Tải về"
    }
}

# Initial language check
if "lang" not in st.session_state:
    st.session_state.lang = "Tiếng Việt"

# --- SIDEBAR BRANDING ---
try:
    if os.path.exists("Hinh anh logo cong ty.png"):
        st.sidebar.image("Hinh anh logo cong ty.png", use_container_width=True)
    elif os.path.exists("images/Hinh anh logo cong ty.png"):
        st.sidebar.image("images/Hinh anh logo cong ty.png", use_container_width=True)
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
    [T["menu_home"], T["menu_reg"], T["menu_trainers"], T["menu_docs"], T["menu_admin"]],
    key="menu_radio"
)

# --- HOME PAGE ---
if menu == T["menu_home"]:
    st.markdown(f'<div class="main-header"><h1>{T["home_title"]}</h1><p>{T["home_subtitle"]}</p></div>', unsafe_allow_html=True)
    
    registrations = db.get_registrations()
    
    # Month Selection
    current_month = st.radio(T["select_month"], [5, 6, 7], horizontal=True, format_func=lambda x: f"{T['month_label']} {x}")
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
                # Keep fixed dept options
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
    if "docs_authenticated" not in st.session_state:
        st.session_state.docs_authenticated = False

    if not st.session_state.docs_authenticated:
        st.markdown(f'<div class="main-header"><h1>{T["docs_title"]}</h1></div>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.info("🔐 Vui lòng nhập mật khẩu để truy cập tài liệu đào tạo. / 교육 자료에 액세스하려면 비밀번호를 입력하십시오.")
        
        doc_pass = st.text_input("Mật khẩu tài liệu / 자료 비밀번호:", type="password", key="doc_password_input")
        if st.button("Truy cập / 액세스", key="doc_auth_btn"):
            if doc_pass == "tpm2026": # Mật khẩu mặc định
                st.session_state.docs_authenticated = True
                st.rerun()
            else:
                st.error("Mật khẩu không chính xác. / 비밀번호가 틀렸습니다.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="main-header"><h1>{T["docs_title"]}</h1></div>', unsafe_allow_html=True)
        
        # Logout button for docs
        col_title, col_logout = st.columns([5, 1])
        with col_logout:
            if st.button("🔒 Khóa / 잠금", help="Đăng xuất khỏi phần tài liệu"):
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
            
            for cat in categories:
                st.markdown(f"#### 📂 {cat}")
                cat_docs = docs[docs['Category'] == cat]
                if not cat_docs.empty:
                    for idx, row in cat_docs.iterrows():
                        with st.expander(f"📄 {row['Title']}"):
                            st.write(f"**{T['doc_desc']}:** {row['Description']}")
                            st.write(f"**{T['doc_date']}:** {row['UploadDate']}")
                            
                            # Use a direct link instead of st.button for reliable downloading on Cloud
                            doc_url = row.get('FileURL', '#')
                            st.markdown(f'''
                                <a href="{doc_url}" target="_blank" style="
                                    text-decoration: none;
                                    background-color: #4b6cb7;
                                    color: white;
                                    padding: 8px 16px;
                                    border-radius: 5px;
                                    font-weight: bold;
                                    display: inline-block;
                                    margin-top: 10px;
                                ">📥 {T['doc_download']}</a>
                            ''', unsafe_allow_html=True)
                else:
                    st.markdown(f"<span style='color: gray; font-style: italic;'>{T['docs_no_data']}</span>", unsafe_allow_html=True)
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
            
        tab_list, tab_manage, tab_docs, tab_trainers = st.tabs([T["tab_list"], T["tab_manage"], T["tab_docs"], "👨‍🏫 Quản lý Giảng viên" if lang == "Tiếng Việt" else "👨‍🏫 강사 관리"])
        
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
            else:
                st.info(T["no_data"])
                
        with tab_manage:
            st.markdown(f"### {T['delete_title']}")
            if not registrations.empty:
                for index, row in registrations.iterrows():
                    with st.expander(f"📌 {row['Date']} - {row['Department']} ({row['Team']})"):
                        with st.form(key=f"edit_form_{index}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                edit_dept = st.text_input(T["dept"], value=row['Department'], key=f"dept_{index}")
                                edit_team = st.text_input(T["team"], value=row['Team'], key=f"team_{index}")
                                
                                try:
                                    sess_idx = T["sessions"].index(row['Session'])
                                except ValueError:
                                    sess_idx = 0
                                edit_session = st.selectbox(T["session"], T["sessions"], index=sess_idx, key=f"session_{index}")
                                
                                edit_attendees = st.number_input(T["attendees"], min_value=1, value=int(row['Attendees']), key=f"att_{index}")
                            with col2:
                                try:
                                    parsed_date = datetime.strptime(row['Date'], "%Y-%m-%d").date()
                                except:
                                    parsed_date = date(2026, 5, 1)
                                edit_date = st.date_input(T["date"], value=parsed_date, key=f"date_{index}")
                                edit_timeslot = st.text_input(T["time_exact"] + " (Sáng/Chiều hh:mm)", value=row['TimeSlot'], key=f"time_{index}")
                                
                            c_sub1, c_sub2 = st.columns([1, 1])
                            with c_sub1:
                                edit_status = st.checkbox("✅ Đã hoàn thành (Completed)", value=(row.get('Status') == 'Completed'), key=f"status_{index}")
                                save_label = "💾 Lưu thay đổi" if lang == "Tiếng Việt" else "💾 변경 사항 저장"
                                if st.form_submit_button(save_label):
                                    status_val = "Completed" if edit_status else "Pending"
                                    if db.update_registration(index, edit_dept, edit_team, edit_session, row['Content'], edit_date, edit_timeslot, edit_attendees, status_val):
                                        st.rerun()
                        
                        if st.button(T["delete_btn"], key=f"del_{index}"):
                            if db.delete_registration(index):
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
                doc_url = st.text_input("Link tài liệu (Google Drive...) / 자료 링크 (구글 드라이브...)")
                
                submit_doc = st.form_submit_button(T["doc_upload"])
                if submit_doc and doc_url and doc_name:
                    db.save_document(doc_name, doc_desc, doc_url, doc_cat)
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
                    st.success("Thêm thành công! / thành công!")
                    
            st.markdown("---")
            dyn_trainers = db.get_trainers()
            if not dyn_trainers.empty:
                for index, row in dyn_trainers.iterrows():
                    with st.expander(f"👤 {row['Name']} - {row['Team']}"):
                        st.write(f"**Chức danh:** {row['Role_VN']} / {row['Role_KR']}")
                        st.write(f"**Mô tả:** {row['Desc']}")
                        if row.get('ImageFile') and str(row.get('ImageFile')) != 'nan':
                            st.write(f"**Ảnh:** {row['ImageFile']}")
                        if st.button("🗑️ Xóa / xóa", key=f"del_trainer_{index}"):
                            if db.delete_trainer(index):
                                st.rerun()
            else:
                st.info("Chưa có giảng viên được thêm mới. / không có.")
