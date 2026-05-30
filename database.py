import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit_gsheets import GSheetsConnection

# Database file names (for fallback/migration)
REG_FILE = 'training_data.csv'
DOC_FILE = 'documents.csv'
TRAINER_FILE = 'trainers.csv'

# Worksheet names
WS_REG = "Registrations"
WS_DOC = "Documents"
WS_TRAIN = "Trainers"

def get_connection():
    return st.connection("gsheets", type=GSheetsConnection)

def init_db():
    pass

def init_docs_db():
    pass

def init_trainers_db():
    pass

# --- REGISTRATIONS ---
def get_registrations(use_cache=False):
    # 1. Prioritize local CSV file as the absolute Source of Truth
    if os.path.exists(REG_FILE):
        try:
            df = pd.read_csv(REG_FILE)
            # Ensure new columns exist
            for col in ['ActualAttendees', 'Note']:
                if col not in df.columns:
                    df[col] = ""
            df['ActualAttendees'] = df['ActualAttendees'].fillna("").astype(str)
            df['Note'] = df['Note'].fillna("").astype(str)
            return df
        except Exception as e:
            st.warning(f"Lỗi đọc file local training_data.csv: {e}. Đang tự động thử tải từ Google Sheets...")

    # 2. Fallback to Google Sheets if local file is missing or corrupted
    try:
        conn = get_connection()
        ttl = 60 if use_cache else 0
        df = conn.read(worksheet=WS_REG, ttl=ttl)
        if df is not None and not df.empty:
            df = df.dropna(how='all')
            # Ensure columns exist
            for col in ['ActualAttendees', 'Note']:
                if col not in df.columns:
                    df[col] = ""
            df['ActualAttendees'] = df['ActualAttendees'].fillna("").astype(str)
            df['Note'] = df['Note'].fillna("").astype(str)
            # Cache it locally immediately
            df.to_csv(REG_FILE, index=False)
            return df
    except Exception as e:
        pass

    # 3. Ultimate fallback: empty DataFrame with correct structure
    return pd.DataFrame(columns=[
        'Timestamp', 'Department', 'Team', 'Session', 'Content', 'Date', 'TimeSlot', 'Attendees', 'Status', 'ActualAttendees', 'Note'
    ])

def save_registration(dept, team, session, content, date, timeslot, attendees):
    df = get_registrations(use_cache=False)
    df['ActualAttendees'] = df['ActualAttendees'].fillna("").astype(str)
    df['Note'] = df['Note'].fillna("").astype(str)
    new_entry = {
        'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Department': dept, 'Team': team, 'Session': session, 'Content': content,
        'Date': date.strftime("%Y-%m-%d") if hasattr(date, 'strftime') else str(date),
        'TimeSlot': timeslot, 'Attendees': attendees, 'Status': 'Pending',
        'ActualAttendees': '', 'Note': ''
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    
    # Save locally first (100% reliable)
    df.to_csv(REG_FILE, index=False)
    
    # Attempt cloud save in the background
    try:
        conn = get_connection()
        conn.update(worksheet=WS_REG, data=df)
    except Exception as e:
        # Silently fail or write warning without breaking local usage
        pass

def update_registration(index, dept, team, session, content, date, timeslot, attendees, status="Pending", actual_attendees="", note=""):
    df = get_registrations(use_cache=False)
    try:
        # Cast columns to string type to avoid float64 dtype issues entirely
        df['ActualAttendees'] = df['ActualAttendees'].fillna("").astype(str)
        df['Note'] = df['Note'].fillna("").astype(str)
        
        df.at[index, 'Department'] = str(dept)
        df.at[index, 'Team'] = str(team)
        df.at[index, 'Session'] = str(session)
        df.at[index, 'Content'] = str(content)
        df.at[index, 'Date'] = date.strftime("%Y-%m-%d") if hasattr(date, 'strftime') else str(date)
        df.at[index, 'TimeSlot'] = str(timeslot)
        df.at[index, 'Attendees'] = int(attendees)
        df.at[index, 'Status'] = str(status)
        df.at[index, 'ActualAttendees'] = str(actual_attendees) if pd.notna(actual_attendees) else ""
        df.at[index, 'Note'] = str(note) if pd.notna(note) else ""
        
        # Save locally first
        df.to_csv(REG_FILE, index=False)
        
        # Attempt cloud update
        try:
            conn = get_connection()
            conn.update(worksheet=WS_REG, data=df)
        except Exception as e:
            pass
            
        return True
    except Exception as e:
        st.error(f"Error updating: {e}")
        return False

def delete_registration(index):
    df = get_registrations(use_cache=False)
    try:
        df = df.drop(index)
        
        # Save locally first
        df.to_csv(REG_FILE, index=False)
        
        # Attempt cloud delete
        try:
            conn = get_connection()
            conn.update(worksheet=WS_REG, data=df)
        except Exception as e:
            pass
            
        return True
    except Exception as e: 
        return False

def sync_local_to_sheets():
    if os.path.exists(REG_FILE):
        try:
            df = pd.read_csv(REG_FILE)
            for col in ['ActualAttendees', 'Note']:
                if col not in df.columns:
                    df[col] = ""
            df['ActualAttendees'] = df['ActualAttendees'].fillna("")
            df['Note'] = df['Note'].fillna("")
            
            conn = get_connection()
            conn.update(worksheet=WS_REG, data=df)
            return True
        except Exception as e:
            raise Exception(f"GSheets Push Sync Error: {e}")
    return False

def sync_sheets_to_local():
    try:
        conn = get_connection()
        
        # 1. Sync Registrations
        df_reg = conn.read(worksheet=WS_REG, ttl=0)
        if df_reg is not None and not df_reg.empty:
            df_reg = df_reg.dropna(how='all')
            for col in ['ActualAttendees', 'Note']:
                if col not in df_reg.columns:
                    df_reg[col] = ""
            df_reg['ActualAttendees'] = df_reg['ActualAttendees'].fillna("")
            df_reg['Note'] = df_reg['Note'].fillna("")
            df_reg.to_csv(REG_FILE, index=False)
            
        # 2. Sync Documents
        df_doc = conn.read(worksheet=WS_DOC, ttl=0)
        if df_doc is not None and not df_doc.empty:
            df_doc = df_doc.dropna(how='all')
            if 'Team' not in df_doc.columns:
                df_doc['Team'] = "Chung"
            df_doc['Team'] = df_doc['Team'].fillna("Chung")
            df_doc.to_csv(DOC_FILE, index=False)
            
        # 3. Sync Trainers
        df_train = conn.read(worksheet=WS_TRAIN, ttl=0)
        if df_train is not None and not df_train.empty:
            df_train = df_train.dropna(how='all')
            df_train.to_csv(TRAINER_FILE, index=False)
            
        return True
    except Exception as e:
        raise Exception(f"GSheets Pull Sync Error: {e}")

# --- DOCUMENTS ---
def get_documents(use_cache=False):
    # 1. Prioritize local CSV file
    if os.path.exists(DOC_FILE):
        try:
            df = pd.read_csv(DOC_FILE)
            if 'Team' not in df.columns:
                df['Team'] = "Chung"
            df['Team'] = df['Team'].fillna("Chung")
            return df
        except Exception as e:
            pass
            
    # 2. Fallback to Google Sheets
    try:
        conn = get_connection()
        ttl = 300 if use_cache else 0
        df = conn.read(worksheet=WS_DOC, ttl=ttl)
        if df is not None and not df.empty:
            df = df.dropna(how='all')
            if 'Team' not in df.columns:
                df['Team'] = "Chung"
            df['Team'] = df['Team'].fillna("Chung")
            # Cache locally
            df.to_csv(DOC_FILE, index=False)
            return df
    except Exception as e:
        pass
        
    # 3. Ultimate empty DataFrame fallback
    return pd.DataFrame(columns=['Title', 'Description', 'FileURL', 'Category', 'UploadDate', 'Team'])

def save_document(title, description, file_url, category, team="Chung"):
    df = get_documents(use_cache=False)
    new_doc = {
        'Title': title, 'Description': description, 'FileURL': file_url,
        'Category': category, 'Team': team, 'UploadDate': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    df = pd.concat([df, pd.DataFrame([new_doc])], ignore_index=True)
    
    # Save locally first
    df.to_csv(DOC_FILE, index=False)
    
    # Attempt cloud save
    try:
        conn = get_connection()
        conn.update(worksheet=WS_DOC, data=df)
    except Exception: 
        pass
    return True

def delete_document(index):
    df = get_documents(use_cache=False)
    try:
        df = df.drop(index)
        
        # Save locally first
        df.to_csv(DOC_FILE, index=False)
        
        # Attempt cloud delete
        try:
            conn = get_connection()
            conn.update(worksheet=WS_DOC, data=df)
        except Exception: 
            pass
        return True
    except Exception: 
        return False

# --- TRAINERS ---
def get_trainers():
    # 1. Prioritize local CSV file
    if os.path.exists(TRAINER_FILE):
        try:
            return pd.read_csv(TRAINER_FILE)
        except Exception as e:
            pass
            
    # 2. Fallback to Google Sheets
    try:
        conn = get_connection()
        df = conn.read(worksheet=WS_TRAIN, ttl=0)
        if df is not None and not df.empty:
            df = df.dropna(how='all')
            # Cache locally
            df.to_csv(TRAINER_FILE, index=False)
            return df
    except Exception as e:
        pass
        
    # 3. Ultimate empty DataFrame fallback
    return pd.DataFrame(columns=['Name', 'Role_VN', 'Role_KR', 'Team', 'Desc', 'ImageFile'])

def save_trainer(name, role_vn, role_kr, team, desc, image_file):
    df = get_trainers()
    new_trainer = {
        'Name': name, 'Role_VN': role_vn, 'Role_KR': role_kr,
        'Team': team, 'Desc': desc, 'ImageFile': image_file
    }
    df = pd.concat([df, pd.DataFrame([new_trainer])], ignore_index=True)
    
    # Save locally first
    df.to_csv(TRAINER_FILE, index=False)
    
    # Attempt cloud save
    try:
        conn = get_connection()
        conn.update(worksheet=WS_TRAIN, data=df)
    except Exception: 
        pass
    return True

def delete_trainer(index):
    df = get_trainers()
    try:
        df = df.drop(index)
        
        # Save locally first
        df.to_csv(TRAINER_FILE, index=False)
        
        # Attempt cloud delete
        try:
            conn = get_connection()
            conn.update(worksheet=WS_TRAIN, data=df)
        except Exception: 
            pass
        return True
    except Exception: 
        return False
