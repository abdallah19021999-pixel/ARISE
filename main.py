import streamlit as st
import json
import os

# 1. إعدادات النظام
st.set_page_config(page_title="SYSTEM: ARISE", layout="centered")

# 2. الـ CSS الاحترافي (بساطة مطلقة وفخامة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');

    /* الخلفية واللون الأساسي */
    .stApp {
        background-color: #000000 !important;
        color: #e0f2ff !important;
    }

    /* التحكم في عرض العناصر عشان التناسق */
    [data-testid="stVerticalBlock"] > div:has(div.stForm) {
        max-width: 420px;
        margin: auto;
    }

    /* تنظيف الخانات - وداعاً للسطور الزرقاء التقيلة */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, .stSelectbox div {
        background-color: #0a0a0a !important;
        border: 1px solid #1a1a1a !important; /* حدود خافتة جداً */
        color: #00d4ff !important;
        border-radius: 4px !important;
        transition: 0.3s ease-in-out;
    }
    
    /* تأثير خفيف جداً عند الوقوف على الخانة */
    div[data-baseweb="input"]:focus-within {
        border: 1px solid #00d4ff !important;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.2) !important;
    }
    
    input { color: #00d4ff !important; font-family: 'Orbitron', sans-serif !important; }

    /* زرار ARISE: نيون ناعم واحترافي */
    .stButton > button {
        width: 100% !important;
        background: transparent !important;
        color: #00d4ff !important;
        border: 1px solid #00d4ff !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 22px !important;
        font-weight: bold !important;
        letter-spacing: 5px !important;
        padding: 12px !important;
        border-radius: 2px !important;
        box-shadow: 0 0 5px rgba(0, 212, 255, 0.2) !important;
        transition: 0.4s all !important;
        margin-top: 25px !important;
    }

    .stButton > button:hover {
        background: #00d4ff !important;
        color: #000 !important;
        box-shadow: 0 0 25px #00d4ff !important;
        border: 1px solid #00d4ff !important;
    }

    /* تنسيق العناوين والـ Labels */
    label { 
        color: #555 !important; /* لون رمادي هادي للـ labels عشان ميزحمش العين */
        font-family: 'Orbitron', sans-serif !important; 
        font-size: 11px !important;
        letter-spacing: 1.5px;
        margin-bottom: 5px !important;
    }

    /* إخفاء أي زوائد من ستريمليت */
    header, footer {visibility: hidden !important;}
    </style>
    """, unsafe_allow_html=True)

# 3. واجهة النظام (The Sleek Header)
st.markdown("""
    <div style='text-align:center; margin-top:60px; margin-bottom: 40px;'>
        <h1 style='color:#00d4ff; font-family: "Orbitron"; font-size: 20px; letter-spacing: 10px; opacity: 0.8;'>SYSTEM ARISE</h1>
        <div style='width: 50px; height: 1px; background: #00d4ff; margin: 15px auto; opacity: 0.3;'></div>
    </div>
""", unsafe_allow_html=True)

# 4. الفورم المتناسق والبسيط
with st.form("awakening_sleek"):
    u_name = st.text_input("IDENTIFICATION", placeholder="ENTER NAME...")
    u_goal = st.selectbox("GOAL", ["HYPERTROPHY", "DEFINITION"])
    
    # الزرار النيون الاحترافي
    if st.form_submit_button("ARISE"):
        if u_name:
            st.markdown(f"""
                <div style='border-top: 1px solid #00d4ff; padding-top: 20px; margin-top: 30px; text-align: center;'>
                    <h3 style='font-family: Orbitron; color: #fff; font-size: 16px; letter-spacing: 2px;'>ACCESS GRANTED</h3>
                    <p style='font-family: Cairo; color: #555; font-size: 12px;'>WELCOME, PLAYER {u_name.upper()}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Input required.")
