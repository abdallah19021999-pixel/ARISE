import streamlit as st
import json
import os

st.set_page_config(page_title="SYSTEM: ARISE", layout="centered")

# CSS السيطرة المطلقة - القضاء على اللون الأبيض والأزرار البدائية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');

    .stApp { background-color: #00050a; color: #00d4ff; }

    /* تحويل كل الخانات لأسود نيون ومنع اللون الأبيض */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, .stSelectbox div {
        background-color: #050a0f !important;
        border: 2px solid #00d4ff !important;
        color: #00d4ff !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
    }
    
    /* تغيير لون الخط داخل الخانات */
    input { color: #00d4ff !important; font-family: 'Orbitron', sans-serif; }
    
    /* القضاء على أزرار +/- البدائية */
    input[type=number]::-webkit-inner-spin-button, 
    input[type=number]::-webkit-outer-spin-button { 
        -webkit-appearance: none; margin: 0; 
    }

    /* زرار ARISE النيون الحقيقي */
    .stButton > button {
        width: 100%;
        background: transparent !important;
        color: #00d4ff !important;
        border: 2px solid #00d4ff !important;
        font-family: 'Orbitron', sans-serif;
        font-size: 24px !important;
        text-shadow: 0 0 10px #00d4ff;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.4), inset 0 0 10px rgba(0, 212, 255, 0.2);
        transition: 0.5s;
        height: 60px;
        margin-top: 20px;
    }
    .stButton > button:hover {
        background: #00d4ff !important;
        color: #000 !important;
        box-shadow: 0 0 50px #00d4ff;
    }

    /* الـ Labels */
    label { 
        color: #00d4ff !important; 
        font-family: 'Orbitron', sans-serif; 
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# شاشة الـ Notification (زي الصورة اللي عجبتك)
st.markdown("""
    <div style='text-align:center; border: 1px solid #00d4ff; padding: 20px; background: rgba(0, 212, 255, 0.05); margin-bottom: 30px;'>
        <h2 style='font-family: Orbitron; color: #00d4ff; text-shadow: 0 0 10px #00d4ff;'>SYSTEM NOTIFICATION</h2>
        <p style='font-family: Cairo; color: #888;'>أنت الآن مؤهل لتكون لاعباً في النظام</p>
    </div>
""", unsafe_allow_html=True)

# النموذج (بدون العبط الأبيض)
with st.container():
    u_name = st.text_input("CODE NAME")
    u_goal = st.selectbox("OBJECTIVE", ["HYPERTROPHY (Bulk)", "DEFINITION (Cut)"])
    
    col1, col2 = st.columns(2)
    u_w = col1.number_input("Weight (kg)", value=80)
    u_h = col2.number_input("Height (cm)", value=175)
    
    if st.button("ARISE"):
        if u_name:
            st.success(f"WELCOME, {u_name}. SYSTEM INITIALIZED.")
