import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Tự động tìm đường dẫn file .env ở cùng thư mục với file script này
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path)

def get_mes_front_ng_list(start_date, end_date, eqp_list="", op_list="4700", device_list="", prod_list="MASS,REPAIR,RE_TEST,SAMPLE,ETC"):
    """
    Lấy dữ liệu Front NG List từ hệ thống MES.
    
    Args:
        start_date (str): Ngày bắt đầu (YYYYMMDD)
        end_date (str): Ngày kết thúc (YYYYMMDD)
        eqp_list (str): Danh sách mã máy, cách nhau bằng dấu phẩy
        op_list (str): Danh sách mã công đoạn (mặc định 4700: Active Align)
        device_list (str): Danh sách mã sản phẩm
        prod_list (str): Loại sản xuất
        
    Returns:
        pd.DataFrame: Dữ liệu trả về dưới dạng DataFrame của pandas
    """
    
    url = "http://192.168.60.29:8070/pl/plv/mes/eqp/frontnglist"
    
    # Lấy API Key từ môi trường (file .env)
    api_key = os.getenv("MES_API_KEY")
    
    if not api_key:
        print(f"DEBUG: Khác phục lỗi - Không tìm thấy API Key tại {dotenv_path}")
        raise ValueError("Lỗi: Không tìm thấy MES_API_KEY trong file .env!")
    else:
        # In ra 4 ký tự đầu của Key để kiểm tra (bảo mật)
        print(f"DEBUG: Đã load API Key (Bắt đầu bằng: {api_key[:4]}...)")

    headers = {
        "X-Api-Key": api_key,
        "Content-Type": "application/json"
    }
    
    # Gửi dữ liệu trực tiếp, không bọc trong key 'params'
    payload = {
        "start_date": start_date,
        "end_date": end_date,
        "eqp_list": eqp_list,
        "op_list": op_list,
        "device_list": device_list,
        "prod_list": prod_list
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"DEBUG: Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Lỗi API (Status {response.status_code}): {response.text}")
            return pd.DataFrame()
            
        data = response.json()
        print(f"DEBUG: Phản hồi từ Server: {data}")
        
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict):
            if "data" in data and data["data"] is not None:
                return pd.DataFrame(data["data"])
            elif "sample" in data: # Thử kiểm tra key sample nếu có
                return pd.DataFrame(data["sample"])
            return pd.DataFrame([data])
        else:
            return pd.DataFrame()
            
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API MES: {e}")
        return pd.DataFrame()

# Dữ liệu mẫu để dùng khi API lỗi
SAMPLE_DATA = [
    {"SUM_DATE": "2026-04-11", "OPERATION": "4700 : Active Align", "DEVICE": "110S948UC0 : M3 TELE", "PROD_TYPE": "RE_TEST", "EQUIPMENT": "PLCMV-AA002A", "FAIL_GROUP": "A/F 구동불량", "FAIL_CODE": "[52]AFFail", "FAIL_COUNT": 5, "FAIL_RATE": 1.2},
    {"SUM_DATE": "2026-04-11", "OPERATION": "4700 : Active Align", "DEVICE": "110S948UC0 : M3 TELE", "PROD_TYPE": "MASS", "EQUIPMENT": "PLCMV-AA001A", "FAIL_GROUP": "Lens Crack", "FAIL_CODE": "[10]LensCrack", "FAIL_COUNT": 2, "FAIL_RATE": 0.5},
    {"SUM_DATE": "2026-04-11", "OPERATION": "4700 : Active Align", "DEVICE": "110S948UC0 : M3 TELE", "PROD_TYPE": "RE_TEST", "EQUIPMENT": "PLCMV-AA003A", "FAIL_GROUP": "Dust", "FAIL_CODE": "[22]Dust", "FAIL_COUNT": 12, "FAIL_RATE": 2.8},
    {"SUM_DATE": "2026-04-11", "OPERATION": "4700 : Active Align", "DEVICE": "110S948UC0 : M3 TELE", "PROD_TYPE": "MASS", "EQUIPMENT": "PLCMV-AA002A", "FAIL_GROUP": "Dust", "FAIL_CODE": "[22]Dust", "FAIL_COUNT": 8, "FAIL_RATE": 1.9}
]

def get_mes_data_with_fallback(start_date, end_date):
    """Lấy dữ liệu thật, nếu lỗi thì trả về dữ liệu mẫu để demo"""
    df = get_mes_front_ng_list(start_date, end_date)
    if df.empty or (isinstance(df, pd.DataFrame) and "status" in df.columns and df.iloc[0]["status"] == "error"):
        print("Sử dụng dữ liệu mẫu do API lỗi hoặc không có dữ liệu.")
        return pd.DataFrame(SAMPLE_DATA)
    return df
