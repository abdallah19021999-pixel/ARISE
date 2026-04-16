import streamlit as st
import json
import os

# 1. إعدادات النظام
st.set_page_config(page_title="SYSTEM: ARISE", page_icon="⚡", layout="wide")

# 2. الـ CSS الاحترافي (إلغاء الأبيض وتحويل الزر لنيون)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');

    .stApp {
        background: #00050a;
        color: #e0f2ff;
    }

    /* تصميم الـ Glass Container */
    .glass-box {
        background: rgba(0, 20, 40, 0.6);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 15px;
        padding: 40px;
        margin: auto;
        max-width: 700px;
        box-shadow: 0 0 40px rgba(0, 212, 255, 0.1);
    }

    /* === القضاء على اللون الأبيض في المدخلات === */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, .stSelectbox div {
        background-color: rgba(0, 10, 20, 0.8) !important;
        border: 2px solid #00d4ff !important;
        color: #00d4ff !important;
        border-radius: 5px !important;
    }
    
    input { color: #00d4ff !important; font-family: 'Orbitron', sans-serif !important; }
    label { color: #00d4ff !important; font-family: 'Orbitron', sans-serif !important; letter-spacing: 1px; }

    /* === زر ARISE النيون المضيء === */
    .stButton > button {
        background: transparent !important;
        color: #00d4ff !important;
        border: 2px solid #00d4ff !important;
        padding: 15px 60px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        text-transform: uppercase;
        letter-spacing: 5px;
        transition: 0.5s;
        box-shadow: 0 0 15px #00d4ff, inset 0 0 15px #00d4ff;
        display: block;
        margin: 40px auto 0 auto !important;
    }

    .stButton > button:hover {
        background: #00d4ff !important;
        color: #000 !important;
        box-shadow: 0 0 50px #00d4ff, 0 0 20px #00d4ff;
        transform: scale(1.05);
    }

    /* إخفاء الأيقونات الافتراضية للـ Number Input (الـ Plus/Minus) لزيادة الاحترافية */
    input[type=number]::-webkit-inner-spin-button, 
    input[type=number]::-webkit-outer-spin-button { 
        -webkit-appearance: none; margin: 0; 
    }

    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات
def load_data():
    if os.path.exists("monarch_nexus.json"):
        with open("monarch_nexus.json", "r", encoding="utf-8") as f: return json.dump(f)
    return {"initialized": False, "lv": 1, "xp": 0}

if 'user' not in st.session_state:
    st.session_state.user = {"initialized": False, "lv": 1, "xp": 0}
user = st.session_state.user

# 4. واجهة إدخال البيانات (The Awakening)
if not user['initialized']:
    # شاشة التنبيه العلوية (System Notification)
    st.markdown("""
        <div style='text-align:center; margin-top:50px;'>
            <div style='border: 1px solid #00d4ff; padding: 20px; border-radius: 10px; display: inline-block; background: rgba(0,212,255,0.05); box-shadow: 0 0 20px rgba(0,212,255,0.2);'>
                <h1 style='color:#00d4ff; font-family: "Orbitron"; font-size: 28px; margin:0; text-shadow: 0 0 10px #00d4ff;'>SYSTEM NOTIFICATION</h1>
                <p style='color:#888; font-family: "Cairo"; margin-top:10px;'>أنت الآن مؤهل لتكون لاعباً في النظام</p>
            </div>
        </div>
        <br>
    """, unsafe_allow_html=True)

    # نموذج البيانات النيون
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("awakening_form", clear_on_submit=False):
            u_name = st.text_input("CODE NAME")
            u_goal = st.selectbox("OBJECTIVE", ["HYPERTROPHY (Bulk)", "DEFINITION (Cut)"])
            
            c1, c2 = st.columns(2)
            u_weight = c1.number_input("Weight (kg)", 40, 200, 80)
            u_height = c2.number_input("Height (cm)", 120, 230, 175)
            
            # الزر النيون
            submitted = st.form_submit_button("ARISE")
            if submitted:
                if u_name:
                    user.update({"name": u_name.upper(), "initialized": True})
                    st.rerun()
                else:
                    st.error("Player name is required to initialize the system.")

# 5. شاشة الـ Dashboard (بعد الـ Arise)
else:
    st.markdown(f"""
        <div style='text-align:center; margin-top:100px;'>
            <h1 style='font-size:60px; color:white;'>LEVEL {user['lv']}</h1>
            <h2 style='color:#00d4ff;'>{user['name']}</h2>
            <p style='color:#555;'>SYSTEM STATUS: ONLINE</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("RESET SYSTEM"):
        st.session_state.user = {"initialized": False, "lv": 1, "xp": 0}
        st.rerun()
