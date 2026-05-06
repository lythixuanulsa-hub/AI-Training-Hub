import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Connection to Google Sheets
def get_connection():
    return st.connection("gsheets", type=GSheetsConnection)

def init_db(): pass
def init_docs_db(): pass
def init_trainers_db(): pass

# --- REGISTRATIONS ---
def get_registrations(use_cache=True):
    conn = get_connection()
    ttl = 300 if use_cache else 0
    try:
        df = conn.read(worksheet="Registrations", ttl=ttl)
        return df
    except Exception:
        return pd.DataFrame(columns=[
            'Timestamp', 'Department', 'Team', 'Session', 'Content', 'Date', 'TimeSlot', 'Attendees', 'Status'
        ])

def save_registration(dept, team, session, content, date, timeslot, attendees):
    conn = get_connection()
    df = get_registrations()
    new_entry = {
        'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Department': dept, 'Team': team, 'Session': session, 'Content': content,
        'Date': date.strftime("%Y-%m-%d") if hasattr(date, 'strftime') else str(date),
        'TimeSlot': timeslot, 'Attendees': attendees, 'Status': 'Pending'
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    conn.update(worksheet="Registrations", data=df)

def update_registration(index, dept, team, session, content, date, timeslot, attendees, status="Pending"):
    conn = get_connection()
    df = get_registrations()
    try:
        df.at[index, 'Department'] = dept
        df.at[index, 'Team'] = team
        df.at[index, 'Session'] = session
        df.at[index, 'Content'] = content
        df.at[index, 'Date'] = date.strftime("%Y-%m-%d") if hasattr(date, 'strftime') else str(date)
        df.at[index, 'TimeSlot'] = timeslot
        df.at[index, 'Attendees'] = attendees
        df.at[index, 'Status'] = status
        conn.update(worksheet="Registrations", data=df)
        return True
    except Exception as e:
        st.error(f"Error updating: {e}")
        return False

def delete_registration(index):
    conn = get_connection()
    df = get_registrations()
    try:
        df = df.drop(index)
        conn.update(worksheet="Registrations", data=df)
        return True
    except Exception: return False

# --- DOCUMENTS ---
def get_documents(use_cache=True):
    conn = get_connection()
    ttl = 300 if use_cache else 0
    try:
        return conn.read(worksheet="Documents", ttl=ttl)
    except Exception:
        return pd.DataFrame(columns=['Title', 'Description', 'FileURL', 'Category', 'UploadDate'])

def save_document(title, description, file_url, category):
    conn = get_connection()
    df = get_documents()
    new_doc = {
        'Title': title, 'Description': description, 'FileURL': file_url,
        'Category': category, 'UploadDate': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    df = pd.concat([df, pd.DataFrame([new_doc])], ignore_index=True)
    conn.update(worksheet="Documents", data=df)
    return True

def delete_document(index):
    conn = get_connection()
    df = get_documents()
    try:
        df = df.drop(index)
        conn.update(worksheet="Documents", data=df)
        return True
    except Exception: return False

# --- TRAINERS ---
def get_trainers():
    conn = get_connection()
    try:
        return conn.read(worksheet="Trainers", ttl=300)
    except Exception:
        return pd.DataFrame(columns=['Name', 'Role_VN', 'Role_KR', 'Team', 'Desc', 'ImageFile'])

def save_trainer(name, role_vn, role_kr, team, desc, image_file):
    conn = get_connection()
    df = get_trainers()
    new_trainer = {
        'Name': name, 'Role_VN': role_vn, 'Role_KR': role_kr,
        'Team': team, 'Desc': desc, 'ImageFile': image_file
    }
    df = pd.concat([df, pd.DataFrame([new_trainer])], ignore_index=True)
    conn.update(worksheet="Trainers", data=df)
    return True

def delete_trainer(index):
    conn = get_connection()
    df = get_trainers()
    try:
        df = df.drop(index)
        conn.update(worksheet="Trainers", data=df)
        return True
    except Exception: return False
