import streamlit as st
import json
import os

# 1. إعدادات النظام
st.set_page_config(page_title="ARISE: MONARCH SYSTEM", page_icon="⚡", layout="centered")

# 2. تصميم الواجهة (The Dark Abyss UI) - لا وجود للون الأبيض
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');

    .stApp {
        background-color: #00050a;
        background-image: radial-gradient(circle at center, #001a33 0%, #00050a 100%);
        color: #e0f2ff;
    }

    /* إخفاء اللون الأبيض من كل المدخلات */
    div[data-baseweb="input"], div[data-baseweb="select"], .stSelectbox div {
        background-color: #0d1117 !important;
        border: 1px solid #00d4ff !important;
        color: #00d4ff !important;
    }
    
    div[role="listbox"] { background-color: #0d1117 !important; }
    p, label, span { color: #e0f2ff !important; font-family: 'Cairo', sans-serif; }
    
    /* كارت الحالة النيون */
    .status-window {
        border: 2px solid #00d4ff;
        background: rgba(0, 20, 40, 0.9);
        padding: 20px;
        box-shadow: 0 0 25px #00d4ff44;
        margin-bottom: 25px;
        border-radius: 5px;
    }

    /* أزرار العضلات */
    .stButton > button {
        width: 100%; height: 50px; background: #000; color: #00d4ff;
        border: 1px solid #00d4ff; font-family: 'Orbitron', sans-serif;
        transition: 0.4s; margin-bottom: 10px;
    }
    .stButton > button:hover {
        background: #00d4ff; color: #000; box-shadow: 0 0 20px #00d4ff;
    }

    /* كروت التمارين */
    .ex-card {
        background: rgba(0, 212, 255, 0.05);
        border-right: 4px solid #00d4ff;
        padding: 12px; margin: 8px 0;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات
def load_data():
    if os.path.exists("monarch_v3.json"):
        with open("monarch_v3.json", "r", encoding="utf-8") as f: return json.load(f)
    return {"initialized": False, "lang": "en"}

if 'user' not in st.session_state:
    st.session_state.user = load_data()
user = st.session_state.user

# 4. ترجمة الواجهة
strings = {
    'en': {
        'awaken': 'PLAYER AWAKENING', 'name': 'NAME', 'age': 'AGE', 'gender': 'GENDER',
        'male': 'MALE', 'female': 'FEMALE', 'goal': 'GOAL', 'bulk': 'BULK', 'cut': 'CUT',
        'status': 'STATUS', 'quest': 'DAILY QUESTS', 'complete': 'COMPLETE', 'bmi': 'BMI STATUS'
    },
    'ar': {
        'awaken': 'صحوة اللاعب', 'name': 'الاسم', 'age': 'السن', 'gender': 'الجنس',
        'male': 'ذكر', 'female': 'أنثى', 'goal': 'الهدف', 'bulk': 'تضخيم', 'cut': 'تنشيف',
        'status': 'الحالة', 'quest': 'المهمات اليومية', 'complete': 'إتمام المهمة', 'bmi': 'حالة الجسم'
    }
}

# أيقونة اللغة المصغرة في الـ Sidebar
with st.sidebar:
    lang = st.selectbox("🌐", ["en", "ar"], index=0 if user.get('lang') == 'en' else 1, label_visibility="collapsed")
    if lang != user.get('lang'):
        user['lang'] = lang
        st.rerun()
L = strings[user['lang']]

# 5. شاشة إدخال البيانات (الصحوة)
if not user['initialized']:
    st.markdown(f"<h1 style='text-align:center; color:#00d4ff;'>{L['awaken']}</h1>", unsafe_allow_html=True)
    with st.form("init_form"):
        u_name = st.text_input(L['name'])
        u_age = st.number_input(L['age'], 15, 60, 25)
        u_gender = st.radio(L['gender'], [L['male'], L['female']], horizontal=True)
        u_height = st.number_input("Height (cm)", 120, 220, 175)
        u_weight = st.number_input("Weight (kg)", 40, 200, 80)
        u_goal = st.selectbox(L['goal'], [L['bulk'], L['cut']])
        
        if st.form_submit_button("ARISE"):
            bmi = round(u_weight / ((u_height/100)**2), 1)
            user.update({
                "name": u_name.upper(), "age": u_age, "gender": u_gender,
                "h": u_height, "w": u_weight, "goal": u_goal, "bmi": bmi,
                "lv": 1, "xp": 0, "initialized": True
            })
            with open("monarch_v3.json", "w", encoding="utf-8") as f: json.dump(user, f)
            st.rerun()
    st.stop()

# 6. الواجهة الرئيسية (The System Dashboard)
st.markdown(f"""
    <div class="status-window">
        <div style='display:flex; justify-content:space-between;'>
            <span style='color:#00d4ff; font-weight:bold;'>{L['status']}</span>
            <span style='color:#ffcc00;'>RANK: E</span>
        </div>
        <h2 style='margin:10px 0;'>{user['name']}</h2>
        <p style='margin:0; font-size:14px; color:#888;'>LV. {user['lv']} | {L['bmi']}: {user['bmi']}</p>
        <div style='background:#111; height:6px; width:100%; margin-top:15px; border-radius:10px;'>
            <div style='background:#00d4ff; height:100%; width:{user['xp']}%; box-shadow:0 0 15px #00d4ff;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# اختيار العضلات والتمارين المتقدمة
st.write(f"### [ {L['quest']} ]")
col1, col2 = st.columns(2)

exercise_db = {
    'CHEST': [("Incline DB Press", "4x10"), ("Cable Flys", "3x15"), ("Dips", "3x12")],
    'BACK': [("Deadlift", "3x5"), ("Lat Pulldown", "4x12"), ("T-Bar Row", "3x10")],
    'SHOULDERS': [("Military Press", "4x8"), ("Lat Raises", "4x20"), ("Face Pulls", "3x15")],
    'LEGS': [("Squats", "4x8"), ("Leg Press", "3x12"), ("Lying Curls", "4x15")]
}

with col1:
    if st.button("🛡️ CHEST"): st.session_state.target = 'CHEST'
    if st.button("🦾 SHOULDERS"): st.session_state.target = 'SHOULDERS'
with col2:
    if st.button("⚔️ BACK"): st.session_state.target = 'BACK'
    if st.button("🦵 LEGS"): st.session_state.target = 'LEGS'

if 'target' in st.session_state:
    target = st.session_state.target
    st.write(f"#### 📜 CURRENT TARGET: {target}")
    for ex, reps in exercise_db[target]:
        st.markdown(f"<div class='ex-card'><b>{ex}</b><br><small>{reps}</small></div>", unsafe_allow_html=True)
    
    if st.button(L['complete']):
        user['xp'] += 40
        if user['xp'] >= 100:
            user['xp'] = 0; user['lv'] += 1; st.balloons()
        with open("monarch_v3.json", "w", encoding="utf-8") as f: json.dump(user, f)
        st.rerun()
