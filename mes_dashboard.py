import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from mes_api import get_mes_data_with_fallback

# Page configuration
st.set_page_config(
    page_title="MES Production Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>📊 MES PRODUCTION DASHBOARD</h1><p>Hệ thống giám sát lỗi sản xuất thời gian thực</p></div>', unsafe_allow_html=True)

# Filter Sidebar or Top
with st.sidebar:
    st.header("🔍 Bộ lọc dữ liệu")
    start_d = st.date_input("Từ ngày", value=date(2026, 4, 11))
    end_d = st.date_input("Đến ngày", value=date(2026, 4, 11))
    btn_fetch = st.button("🚀 Lấy dữ liệu MES", use_container_width=True)
    
    st.markdown("---")
    st.info("💡 Lưu ý: Nếu hệ thống MES lỗi, Dashboard sẽ tự động hiển thị dữ liệu mẫu để demo.")

# Data Processing
if btn_fetch or "mes_df" not in st.session_state:
    s_str = start_d.strftime("%Y%m%d")
    e_str = end_d.strftime("%Y%m%d")
    
    with st.spinner("Đang kết nối tới hệ thống MES..."):
        df = get_mes_data_with_fallback(s_str, e_str)
        st.session_state.mes_df = df

df = st.session_state.mes_df

if not df.empty:
    # Key Metrics
    total_fails = df['FAIL_COUNT'].sum()
    avg_fail_rate = df['FAIL_RATE'].mean()
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Tổng số lỗi", f"{total_fails} EA")
    with m2:
        st.metric("Tỷ lệ lỗi trung bình", f"{avg_fail_rate:.2f}%")
    with m3:
        st.metric("Số máy đang chạy", len(df['EQUIPMENT'].unique()))

    st.markdown("<br/>", unsafe_allow_html=True)

    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Phân tích lỗi theo máy")
        fig1 = px.bar(df, x="EQUIPMENT", y="FAIL_COUNT", color="FAIL_GROUP", 
                      title="Số lượng lỗi (EA)", barmode="group",
                      color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        st.subheader("🎯 Tỷ lệ lỗi theo nhóm")
        fig2 = px.pie(df, values="FAIL_RATE", names="FAIL_GROUP", 
                      title="Phân bổ tỷ lệ lỗi (%)", hole=0.5,
                      color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    
    # Table
    st.subheader("📋 Bảng dữ liệu chi tiết")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Download
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Tải xuống báo cáo (CSV)",
        data=csv,
        file_name=f"MES_NG_Report_{start_d}.csv",
        mime="text/csv",
    )
else:
    st.warning("⚠️ Không tìm thấy dữ liệu trong khoảng thời gian này.")
