import streamlit as st
import json
import os

# 1. إعدادات النظام الأساسية
st.set_page_config(page_title="ARISE SYSTEM", layout="centered")

# 2. السيطرة المطلقة على الـ CSS (المنقذ من العبط)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');

    /* خلفية الكون المظلم */
    .stApp {
        background-color: #00050a !important;
        color: #00d4ff !important;
    }

    /* التحكم في حجم الفورم عشان ميبقاش طويل بزيادة */
    [data-testid="stVerticalBlock"] > div:has(div.stForm) {
        max-width: 480px;
        margin: auto;
    }

    /* تدمير اللون الأبيض في كل الخانات (Input + Select) */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, .stSelectbox div {
        background-color: #050a0f !important;
        border: 1px solid #00d4ff !important;
        color: #00d4ff !important;
        border-radius: 4px !important;
    }
    
    /* تغيير لون الخط والـ Placeholder */
    input { 
        color: #00d4ff !important; 
        font-family: 'Orbitron', sans-serif !important; 
        background: transparent !important;
    }
    
    /* تنظيف القائمة المنسدلة (The Dropdown Fix) */
    ul[role="listbox"] {
        background-color: #050a0f !important;
        border: 1px solid #00d4ff !important;
    }
    li[role="option"] {
        color: #00d4ff !important;
        background-color: #050a0f !important;
    }
    li[role="option"]:hover {
        background-color: #00d4ff !important;
        color: #000 !important;
    }

    /* === زر ARISE النيون العملاق === */
    .stButton > button {
        width: 100% !important;
        background: transparent !important;
        color: #00d4ff !important;
        border: 2px solid #00d4ff !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 26px !important;
        font-weight: bold !important;
        letter-spacing: 6px !important;
        text-transform: uppercase !important;
        padding: 15px !important;
        border-radius: 8px !important;
        box-shadow: 0 0 15px #00d4ff, inset 0 0 10px #00d4ff !important;
        transition: 0.4s all !important;
        margin-top: 30px !important;
    }

    .stButton > button:hover {
        background: #00d4ff !important;
        color: #000 !important;
        box-shadow: 0 0 50px #00d4ff, 0 0 20px #00d4ff !important;
        transform: scale(1.02);
    }

    /* تنسيق النصوص والـ Labels */
    label { 
        color: #00d4ff !important; 
        font-family: 'Orbitron', sans-serif !important; 
        text-shadow: 0 0 5px rgba(0,212,255,0.5);
    }
    
    /* إخفاء الزوائد */
    header, footer {visibility: hidden !important;}
    </style>
    """, unsafe_allow_html=True)

# 3. شاشة التنبيه الاحترافية (System Notification)
st.markdown("""
    <div style='text-align:center; margin-top:40px; margin-bottom: 20px;'>
        <div style='display: inline-block; border: 1px solid #00d4ff; padding: 15px 40px; background: rgba(0,212,255,0.05); box-shadow: 0 0 15px rgba(0,212,255,0.2);'>
            <h1 style='color:#00d4ff; font-family: "Orbitron"; font-size: 22px; margin:0; text-shadow: 0 0 10px #00d4ff;'>SYSTEM NOTIFICATION</h1>
            <p style='color:#555; font-family: "Cairo"; margin: 5px 0 0 0; font-size: 14px;'>أنت الآن مؤهل لتكون لاعباً في النظام</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. فورم "الصحوة" المختصر والاحترافي
with st.form("awakening"):
    # الخانات المطلوبة فقط
    u_name = st.text_input("CODE NAME", placeholder="ENTER YOUR NAME...")
    u_goal = st.selectbox("OBJECTIVE", ["HYPERTROPHY (BULK)", "DEFINITION (CUT)"])
    
    # الزرار النيون
    submitted = st.form_submit_button("ARISE")
    
    if submitted:
        if u_name:
            st.markdown(f"""
                <div style='text-align:center; padding:20px; border:2px solid #00d4ff; background:black; margin-top:20px;'>
                    <h2 style='color:white; font-family:Orbitron;'>WELCOME, {u_name.upper()}</h2>
                    <p style='color:#00d4ff;'>THE SYSTEM HAS INITIALIZED YOUR JOURNEY.</p>
                </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.error("Identification required. Enter your Name.")
