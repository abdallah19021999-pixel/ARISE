import streamlit as st
import json
import os

# 1. إعدادات النظام - Solo Leveling Edition
st.set_page_config(page_title="ARISE SYSTEM", page_icon="⚡", layout="centered")

# 2. تصميم الواجهة (The Monarch CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');

    .stApp {
        background-color: #00050a;
        background-image: radial-gradient(circle at center, #001a33 0%, #00050a 100%);
        color: #e0f2ff;
    }
    
    /* تعديل لون شريط البحث والمدخلات */
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: #0d1117 !important;
        border: 1px solid #00d4ff !important;
    }
    input { color: #00d4ff !important; background-color: #0d1117 !important; }
    
    /* كارت الحالة - Status Window */
    .status-window {
        border: 2px solid #00d4ff;
        background: rgba(0, 20, 40, 0.9);
        border-radius: 2px;
        padding: 20px;
        box-shadow: 0 0 20px #00d4ff44;
        margin-bottom: 25px;
        font-family: 'Orbitron', sans-serif;
    }

    /* أزرار العضلات - System Nodes */
    .stButton > button {
        width: 100%; height: 55px; background: #000; color: #00d4ff;
        border: 1px solid #00d4ff; font-family: 'Orbitron', sans-serif;
        font-weight: bold; letter-spacing: 2px; transition: 0.5s; margin-bottom: 12px;
    }
    .stButton > button:hover {
        background: #00d4ff; color: #000; box-shadow: 0 0 30px #00d4ff;
    }

    /* صناديق التمارين المتقدمة */
    .exercise-card {
        background: rgba(0, 212, 255, 0.05);
        border-left: 4px solid #00d4ff;
        padding: 15px; margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات واللغات
strings = {
    'en': {
        'awaken': 'SYSTEM INITIALIZATION', 'start': 'ACCEPT CONTRACT', 'name': 'HUNTER NAME',
        'status': 'STATUS', 'lv': 'LEVEL', 'rank': 'RANK', 'quest': 'DAILY QUESTS',
        'complete': 'COMPLETE QUEST', 'chest': 'CHEST', 'back': 'BACK', 'legs': 'LEGS',
        'shoulders': 'SHOULDERS', 'arms': 'ARMS', 'search': 'SEARCH EXERCISES...'
    },
    'ar': {
        'awaken': 'بدء تشغيل النظام', 'start': 'قبول العقد', 'name': 'اسم الصياد',
        'status': 'الحالة', 'lv': 'المستوى', 'rank': 'الرتبة', 'quest': 'المهمات اليومية',
        'complete': 'إتمام المهمة', 'chest': 'الصدر', 'back': 'الظهر', 'legs': 'الأرجل',
        'shoulders': 'الكتف', 'arms': 'الذراع', 'search': 'بحث عن التمارين...'
    }
}

# تمارين احترافية (قاعدة بيانات شاملة)
exercise_db = {
    'CHEST': [
        ("Incline Bench Press", "4 Sets x 8-10 Reps"),
        ("Flat Dumbbell Flys", "3 Sets x 12 Reps"),
        ("Weighted Dips", "3 Sets x 10 Reps"),
        ("Cable Crossovers", "4 Sets x 15 Reps"),
        ("Push-ups (Diamond)", "3 Sets x Failure")
    ],
    'BACK': [
        ("Deadlifts", "4 Sets x 5 Reps"),
        ("Pull-ups (Wide Grip)", "4 Sets x 10 Reps"),
        ("Bent Over Rows", "3 Sets x 12 Reps"),
        ("Lat Pulldowns", "4 Sets x 12 Reps"),
        ("Face Pulls", "3 Sets x 15 Reps")
    ],
    'SHOULDERS': [
        ("Military Press", "4 Sets x 8 Reps"),
        ("Lateral Raises", "4 Sets x 15 Reps"),
        ("Front Raises", "3 Sets x 12 Reps"),
        ("Reverse Flys", "3 Sets x 15 Reps"),
        ("Arnold Press", "3 Sets x 10 Reps")
    ],
    'LEGS': [
        ("Barbell Squats", "4 Sets x 8 Reps"),
        ("Leg Press", "3 Sets x 12 Reps"),
        ("Leg Extensions", "4 Sets x 15 Reps"),
        ("Hamstring Curls", "4 Sets x 15 Reps"),
        ("Calf Raises", "4 Sets x 20 Reps")
    ],
    'ARMS': [
        ("Barbell Curls", "3 Sets x 10 Reps"),
        ("Hammer Curls", "3 Sets x 12 Reps"),
        ("Tricep Pushdowns", "4 Sets x 12 Reps"),
        ("Skull Crushers", "3 Sets x 10 Reps"),
        ("Preacher Curls", "3 Sets x 12 Reps")
    ]
}

# 4. محرك البيانات
def load_data():
    if os.path.exists("monarch_data.json"):
        with open("monarch_data.json", "r") as f: return json.load(f)
    return {"name": "", "lv": 1, "xp": 0, "initialized": False, "lang": "en"}

if 'user' not in st.session_state:
    st.session_state.user = load_data()
user = st.session_state.user
L = strings[user['lang']]

# 5. شاشة الصحوة (Awakening)
if not user['initialized']:
    st.markdown(f"<h1 style='text-align:center;'>{L['awaken']}</h1>", unsafe_allow_html=True)
    with st.form("init"):
        name = st.text_input(L['name'])
        lang_choice = st.selectbox("SYSTEM LANGUAGE", ["en", "ar"])
        if st.form_submit_button(L['start']):
            user.update({"name": name.upper(), "lang": lang_choice, "initialized": True})
            with open("monarch_data.json", "w") as f: json.dump(user, f)
            st.rerun()
    st.stop()

# 6. الواجهة الرئيسية (The Nexus)
st.markdown(f"""
    <div class="status-window">
        <div style='display:flex; justify-content:space-between;'>
            <h2 style='margin:0;'>{L['status']}</h2>
            <h2 style='color:#00d4ff; margin:0;'>LV. {user['lv']}</h2>
        </div>
        <p style='color:#888; margin:5px 0;'>PLAYER: {user['name']}</p>
        <div style='background:#111; height:4px; width:100%; margin-top:10px;'>
            <div style='background:#00d4ff; height:100%; width:{user['xp']}%; box-shadow:0 0 10px #00d4ff;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# نظام البحث واختيار العضلات
st.write(f"### [ {L['quest']} ]")
search = st.text_input(L['search'], label_visibility="collapsed")

col1, col2 = st.columns(2)
with col1:
    if st.button(f"🦾 {L['shoulders']}"): st.session_state.target = 'SHOULDERS'
    if st.button(f"🛡️ {L['chest']}"): st.session_state.target = 'CHEST'
with col2:
    if st.button(f"⚔️ {L['back']}"): st.session_state.target = 'BACK'
    if st.button(f"🦵 {L['legs']}"): st.session_state.target = 'LEGS'

# عرض التمارين المتقدمة
if 'target' in st.session_state:
    target = st.session_state.target
    st.write(f"#### 📜 CURRENT TARGET: {target}")
    
    for ex, sets in exercise_db[target]:
        if search.lower() in ex.lower():
            st.markdown(f"""
                <div class="exercise-card">
                    <span style='color:#00d4ff; font-weight:bold;'>{ex}</span><br>
                    <span style='font-size:12px; color:#888;'>{sets}</span>
                </div>
                """, unsafe_allow_html=True)
    
    if st.button(L['complete']):
        user['xp'] += 35
        if user['xp'] >= 100:
            user['xp'] = 0
            user['lv'] += 1
            st.balloons()
        with open("monarch_data.json", "w") as f: json.dump(user, f)
        st.rerun()

# الإعدادات
with st.sidebar:
    st.write("### SYSTEM OVERRIDE")
    if st.button("RESET ALL"):
        os.remove("monarch_data.json")
        st.session_state.clear()
        st.rerun()
