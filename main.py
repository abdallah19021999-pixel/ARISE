import streamlit as st
import json
import os
import time

# 1. إعدادات الصفحة (أولوية للموبايل وشكل الأنمي)
st.set_page_config(page_title="ARISE: MONARCH SYSTEM", page_icon="⚡", layout="centered", initial_sidebar_state="collapsed")

# 2. السيطرة المطلقة على الـ CSS (الديزاين الاحترافي فشخ لعام 2026)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');

    /* خلفية التطبيق - The Deep Abyss */
    .stApp {
        background-color: #00050a;
        background-image: radial-gradient(circle at center, #001a33 0%, #00050a 100%);
        color: #e0f2ff;
        font-family: 'Orbitron', sans-serif;
    }

    /* === تعديل الـ Input Fields لتكون نيون (The Sci-Fi Looks) === */
    /* إخفاء حدود الـ Browser الافتراضية واللون الأبيض */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, .stSelectbox div {
        background-color: #0d1117 !important;
        border: 2px solid #00d4ff !important;
        border-radius: 0px !important; /* زوايا قائمة لشكل النظام */
        color: #00d4ff !important;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 2px;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.2);
    }
    input { color: #00d4ff !important; }

    /* === القضاء على الـ Plus/Minus Buttons (The Fix!) === */
    /* تغيير شكل الـ Number Input ليكون أملس وبدون أزرار بدائية */
    input[type=number]::-webkit-inner-spin-button, 
    input[type=number]::-webkit-outer-spin-button { 
        -webkit-appearance: none; 
        margin: 0; 
    }
    input[type=number] { -moz-appearance: textfield; }

    /* === تنظيف الـ Dropdown List (The White Dropdown Fix) === */
    ul[role="listbox"] {
        background-color: #0d1117 !important;
        border: 1px solid #00d4ff !important;
        color: #00d4ff !important;
    }
    li[role="option"]:hover {
        background-color: #00d4ff !important;
        color: #000 !important;
    }

    /* === كارت الحالة (Status Window) === */
    .status-window {
        border: 2px solid #00d4ff;
        background: rgba(0, 20, 40, 0.9);
        padding: 25px;
        border-radius: 5px;
        box-shadow: 0 0 25px #00d4ff44;
        margin-bottom: 25px;
        text-align: center;
    }

    /* === أزرار العضلات النيون === */
    .stButton > button {
        width: 100%; height: 55px; border-radius: 0px; background: #000;
        color: #00d4ff; border: 2px solid #00d4ff; font-weight: bold;
        transition: 0.4s; letter-spacing: 2px;
    }
    .stButton > button:hover {
        background: #00d4ff; color: #000; box-shadow: 0 0 30px #00d4ff;
    }

    /* === صندوق التمارين المتقدمة === */
    .ex-card {
        background: rgba(0, 212, 255, 0.05);
        border-right: 4px solid #00d4ff;
        padding: 15px; margin: 10px 0;
        border-radius: 10px 0 0 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. محرك البيانات (Data Engine)
def load_system_data():
    default = {
        "name": "", "lv": 1, "xp": 0, "initialized": False, "lang": "en",
        "h": 175, "w": 80, "age": 25, "gender": "Male", "goal": "Bulk"
    }
    if os.path.exists("monarch_nexus_v2.json"):
        with open("monarch_nexus_v2.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return {**default, **data}
    return default

if 'system' not in st.session_state:
    st.session_state.system = load_system_data()
data = st.session_state.system

# 4. ترجمة النظام
strings = {
    'en': {
        'awaken': 'AWAKENING FORM', 'start': 'ARISE', 'name': 'NAME', 'age': 'AGE', 
        'gender': 'GENDER', 'male': 'MALE', 'female': 'FEMALE', 'h': 'HEIGHT (cm)', 
        'w': 'WEIGHT (kg)', 'goal': 'OBJECTIVE', 'bulk': 'BULK', 'cut': 'CUT',
        'status': 'STATUS', 'quest': 'DAILY QUEST LOG', 'complete': 'QUEST COMPLETE'
    },
    'ar': {
        'awaken': 'صحوة اللاعب', 'start': 'ابدأ الارتقاء', 'name': 'الاسم', 'age': 'السن', 
        'gender': 'الجنس', 'male': 'ذكر', 'female': 'أنثى', 'h': 'الطول (سم)', 
        'w': 'الوزن (كجم)', 'goal': 'الهدف', 'bulk': 'تضخيم', 'cut': 'تنشيف',
        'status': 'الحالة', 'quest': 'سجل المهمات اليومية', 'complete': 'إتمام المهمة'
    }
}

# أيقونة اللغة المصغرة في القائمة الجانبية (The Fix!)
with st.sidebar:
    lang = st.selectbox("🌐", ["en", "ar"], index=0 if data['lang'] == 'en' else 1)
    if lang != data['lang']:
        data['lang'] = lang
        st.rerun()
L = strings[data['lang']]

# --- المرحلة 1: الصحوة (Initial Setup) ---طلبك الأساسي
if not data['initialized']:
    st.markdown(f"<h1 style='text-align:center;'>{L['awaken']}</h1>", unsafe_allow_html=True)
    with st.container():
        # استخدام columns لتنظيم الشكل الاحترافي للموبايل
        c1, c2 = st.columns(2)
        u_name = c1.text_input(L['name'], placeholder="Input name...")
        u_age = c2.number_input(L['age'], 15, 60, 25) # تم تعديل الـ NumberInput لإخفاء الأزرار البدائية
        
        u_gender = st.selectbox(L['gender'], [L['male'], L['female']])
        
        # تحويل مدخلات الطول والوزن لـ Sliders لشكل احترافي فشخ كأنك ف 2026
        u_height = st.slider(L['h'], 140, 210, 175)
        u_weight = st.slider(L['w'], 40, 180, 80)
        
        u_goal = st.selectbox(L['goal'], [L['bulk'], L['cut']])
        
        if st.button(L['start']):
            if u_name:
                data.update({
                    "name": u_name.upper(), "age": u_age, "gender": u_gender,
                    "h": u_height, "w": u_weight, "goal": u_goal, "initialized": True
                })
                with open("monarch_nexus_v2.json", "w", encoding="utf-8") as f: json.dump(data, f)
                st.rerun()
            else:
                st.error("Player name is required.")
    st.stop()

# --- المرحلة 2: NEXUS (The Real Monarch UI) ---
# كارت الحالة - Status Window
st.markdown(f"""
    <div class="status-window">
        <div style='display:flex; justify-content:space-between; color:#58a6ff; font-weight:bold;'>
            <span>{L['status']}</span>
            <span>RANK: E</span>
        </div>
        <h1 style='color:white; margin:10px 0;'>{data['name']}</h1>
        <p style='margin:0; color:#888;'>LEVEL. {data['lv']}</p>
        <div style='background:#111; height:6px; width:100%; margin-top:15px;'>
            <div style='background:#00d4ff; height:100%; width:{data['xp']}%; box-shadow:0 0 15px #00d4ff;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# الـ Body Map Simulation والتمارين الاحترافية
st.write(f"### [ {L['quest']} ]")
exercise_db = {
    'CHEST': [("Incline Barbell Press", "4x8"), ("Cable Flys", "3x15")],
    'BACK': [("Pull Ups", "4x10"), ("Deadlifts", "3x5")],
    'SHOULDERS': [("Military Press", "4x8"), ("Lateral Raises", "3x20")],
    'LEGS': [("Squats", "4x8"), ("Leg Extensions", "4x12")]
}

target = st.selectbox("SELECT TARGET", ["...", "CHEST", "BACK", "SHOULDERS", "LEGS"], label_visibility="collapsed")

if target != "...":
    st.write(f"#### 📜 QUEST: {target}")
    for ex, reps in exercise_db[target]:
        st.markdown(f"""<div class='ex-card'>
            <b>{ex}</b><br>
            <span style='color:#00d4ff;'>{reps}</span>
        </div>""", unsafe_allow_html=True)
    
    if st.button(L['complete']):
        data['xp'] += 35
        if data['xp'] >= 100:
            data['xp'] = 0; data['lv'] += 1; st.balloons()
        with open("monarch_nexus_v2.json", "w", encoding="utf-8") as f: json.dump(data, f)
        st.rerun()

# القائمة الجانبية للتصفير
with st.sidebar:
    st.write("### SYSTEM OVERRIDE")
    if st.button("RESET DATA"):
        if os.path.exists("monarch_nexus_v2.json"): os.remove("monarch_nexus_v2.json")
        st.session_state.clear(); st.rerun()
