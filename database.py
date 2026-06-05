import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Database file names (Source of Truth)
REG_FILE = 'training_data.csv'
DOC_FILE = 'documents.csv'
TRAINER_FILE = 'trainers.csv'

# Environment detection: True if running on Streamlit Cloud (Linux / sharing mode), False if running locally (Windows)
IS_CLOUD = (os.name != 'nt') or ("STREAMLIT_SHARING_MODE" in os.environ)

def init_db():
    pass

def init_docs_db():
    pass

def init_trainers_db():
    pass

# --- REGISTRATIONS ---
def get_registrations(use_cache=False):
    if os.path.exists(REG_FILE):
        try:
            df = pd.read_csv(REG_FILE)
            # Ensure new columns exist
            for col in ['ActualAttendees', 'Note']:
                if col not in df.columns:
                    df[col] = ""
            
            # Cast all text columns to str type to avoid any float64 dtype issues
            text_cols = ['Timestamp', 'Department', 'Team', 'Session', 'Content', 'Date', 'TimeSlot', 'Status', 'ActualAttendees', 'Note']
            for col in text_cols:
                if col in df.columns:
                    df[col] = df[col].fillna("").astype(str)
            return df
        except Exception as e:
            st.error(f"Lỗi đọc file training_data.csv: {e}")
            
    # Fallback to empty DataFrame with correct structure
    return pd.DataFrame(columns=[
        'Timestamp', 'Department', 'Team', 'Session', 'Content', 'Date', 'TimeSlot', 'Attendees', 'Status', 'ActualAttendees', 'Note'
    ])

def save_registration(dept, team, session, content, date, timeslot, attendees):
    if IS_CLOUD:
        st.warning("⚠️ Đang chạy ở chế độ trực tuyến (Read-Only). Không thể thêm mới lịch học từ trang web này!")
        return False
        
    df = get_registrations(use_cache=False)
    text_cols = ['Timestamp', 'Department', 'Team', 'Session', 'Content', 'Date', 'TimeSlot', 'Status', 'ActualAttendees', 'Note']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str)
            
    new_entry = {
        'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Department': dept, 'Team': team, 'Session': session, 'Content': content,
        'Date': date.strftime("%Y-%m-%d") if hasattr(date, 'strftime') else str(date),
        'TimeSlot': timeslot, 'Attendees': attendees, 'Status': 'Pending',
        'ActualAttendees': '', 'Note': ''
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(REG_FILE, index=False)
    return True

def update_registration(index, dept, team, session, content, date, timeslot, attendees, status="Pending", actual_attendees="", note=""):
    if IS_CLOUD:
        st.warning("⚠️ Đang chạy ở chế độ trực tuyến (Read-Only). Không thể chỉnh sửa lịch học từ trang web này!")
        return False
        
    df = get_registrations(use_cache=False)
    try:
        # Cast all text columns to string type to avoid float64 dtype issues entirely
        text_cols = ['Timestamp', 'Department', 'Team', 'Session', 'Content', 'Date', 'TimeSlot', 'Status', 'ActualAttendees', 'Note']
        for col in text_cols:
            if col in df.columns:
                df[col] = df[col].fillna("").astype(str)
                
        def safe_str(val):
            if pd.isna(val) or str(val).strip().lower() == 'nan':
                return ""
            return str(val).strip()
        
        df.at[index, 'Department'] = safe_str(dept)
        df.at[index, 'Team'] = safe_str(team)
        df.at[index, 'Session'] = safe_str(session)
        df.at[index, 'Content'] = safe_str(content)
        df.at[index, 'Date'] = date.strftime("%Y-%m-%d") if hasattr(date, 'strftime') else safe_str(date)
        df.at[index, 'TimeSlot'] = safe_str(timeslot)
        df.at[index, 'Attendees'] = int(attendees)
        df.at[index, 'Status'] = safe_str(status)
        df.at[index, 'ActualAttendees'] = safe_str(actual_attendees)
        df.at[index, 'Note'] = safe_str(note)
        
        df.to_csv(REG_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Lỗi khi cập nhật: {e}")
        return False

def delete_registration(index):
    if IS_CLOUD:
        st.warning("⚠️ Đang chạy ở chế độ trực tuyến (Read-Only). Không thể xóa lịch học từ trang web này!")
        return False
        
    df = get_registrations(use_cache=False)
    try:
        df = df.drop(index)
        df.to_csv(REG_FILE, index=False)
        return True
    except Exception as e: 
        st.error(f"Lỗi khi xóa: {e}")
        return False

def sync_local_to_sheets():
    # Deprecated for Option A
    return True

def sync_sheets_to_local():
    # Deprecated for Option A
    return True

# --- DOCUMENTS ---
def get_documents(use_cache=False):
    if os.path.exists(DOC_FILE):
        try:
            df = pd.read_csv(DOC_FILE)
            if 'Team' not in df.columns:
                df['Team'] = "Chung"
            df['Team'] = df['Team'].fillna("Chung")
            return df
        except Exception as e:
            pass
            
    return pd.DataFrame(columns=['Title', 'Description', 'FileURL', 'Category', 'UploadDate', 'Team'])

def save_document(title, description, file_url, category, team="Chung"):
    if IS_CLOUD:
        st.warning("⚠️ Đang chạy ở chế độ trực tuyến (Read-Only). Không thể thêm tài liệu từ trang web này!")
        return False
        
    df = get_documents(use_cache=False)
    new_doc = {
        'Title': title, 'Description': description, 'FileURL': file_url,
        'Category': category, 'Team': team, 'UploadDate': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    df = pd.concat([df, pd.DataFrame([new_doc])], ignore_index=True)
    df.to_csv(DOC_FILE, index=False)
    return True

def delete_document(index):
    if IS_CLOUD:
        st.warning("⚠️ Đang chạy ở chế độ trực tuyến (Read-Only). Không thể xóa tài liệu từ trang web này!")
        return False
        
    df = get_documents(use_cache=False)
    try:
        df = df.drop(index)
        df.to_csv(DOC_FILE, index=False)
        return True
    except Exception: 
        return False

# --- TRAINERS ---
def get_trainers():
    if os.path.exists(TRAINER_FILE):
        try:
            return pd.read_csv(TRAINER_FILE)
        except Exception as e:
            pass
            
    return pd.DataFrame(columns=['Name', 'Role_VN', 'Role_KR', 'Team', 'Desc', 'ImageFile'])

def save_trainer(name, role_vn, role_kr, team, desc, image_file):
    if IS_CLOUD:
        st.warning("⚠️ Đang chạy ở chế độ trực tuyến (Read-Only). Không thể thêm giảng viên từ trang web này!")
        return False
        
    df = get_trainers()
    new_trainer = {
        'Name': name, 'Role_VN': role_vn, 'Role_KR': role_kr,
        'Team': team, 'Desc': desc, 'ImageFile': image_file
    }
    df = pd.concat([df, pd.DataFrame([new_trainer])], ignore_index=True)
    df.to_csv(TRAINER_FILE, index=False)
    return True

def delete_trainer(index):
    if IS_CLOUD:
        st.warning("⚠️ Đang chạy ở chế độ trực tuyến (Read-Only). Không thể xóa giảng viên từ trang web này!")
        return False
        
    df = get_trainers()
    try:
        df = df.drop(index)
        df.to_csv(TRAINER_FILE, index=False)
        return True
    except Exception: 
        return False
