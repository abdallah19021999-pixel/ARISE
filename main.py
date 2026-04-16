import streamlit as st
import json
import os

# 1. إعدادات النظام - Solo Leveling Elite
st.set_page_config(page_title="ARISE: MONARCH SYSTEM", page_icon="⚡", layout="centered")

# 2. السيطرة المطلقة على الـ CSS (قتل اللون الأبيض)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');

    /* خلفية التطبيق */
    .stApp {
        background-color: #00050a;
        background-image: radial-gradient(circle at center, #001a33 0%, #00050a 100%);
        color: #e0f2ff;
    }

    /* إجبار القوائم المنسدلة والمدخلات على اللون الأسود النيون */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, .stSelectbox div {
        background-color: #0d1117 !important;
        border: 1px solid #00d4ff !important;
        color: #00d4ff !important;
    }
    
    /* القائمة التي تظهر عند الضغط (Dropdown List) */
    ul[role="listbox"] {
        background-color: #0d1117 !important;
        border: 1px solid #00d4ff !important;
    }
    li[role="option"] {
        background-color: #0d1117 !important;
        color: #00d4ff !important;
    }
    li[role="option"]:hover {
        background-color: #00d4ff !important;
        color: #000 !important;
    }

    /* القائمة الجانبية (Sidebar) */
    section[data-testid="stSidebar"] {
        background-color: #050a0f !important;
        border-right: 1px solid #00d4ff33;
    }

    /* كارت الحالة (Status Window) */
    .status-window {
        border: 2px solid #00d4ff;
        background: rgba(0, 20, 40, 0.9);
        padding: 20px;
        box-shadow: 0 0 25px #00d4ff44;
        margin-bottom: 25px;
        border-radius: 5px;
        font-family: 'Orbitron', sans-serif;
    }

    /* أزرار العضلات */
    .stButton > button {
        width: 100%; height: 50px; background: #000; color: #00d4ff;
        border: 1px solid #00d4ff; font-family: 'Orbitron', sans-serif;
        transition: 0.4s; font-weight: bold;
    }
    .stButton > button:hover {
        background: #00d4ff; color: #000; box-shadow: 0 0 20px #00d4ff;
    }

    /* نصوص العناوين */
    h1, h2, h3, p, label {
        color: #e0f2ff !important;
        font-family: 'Cairo', sans-serif;
        text-shadow: 0 0 10px #00d4ff66;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات (تحميل وحفظ)
def load_data():
    default = {
        "name": "HUNTER", "age": 25, "gender": "Male", "h": 175, "w": 80, 
        "goal": "Bulk", "bmi": 26.1, "lv": 1, "xp": 0, "initialized": False, "lang": "en"
    }
    if os.path.exists("monarch_final.json"):
        try:
            with open("monarch_final.json", "r", encoding="utf-8") as f:
                saved = json.load(f)
                return {**default, **saved}
        except: return default
    return default

if 'user' not in st.session_state:
    st.session_state.user = load_data()
user = st.session_state.user

# 4. نظام اللغات
strings = {
    'en': {
        'awaken': 'PLAYER AWAKENING', 'name': 'CODE NAME', 'age': 'AGE', 'gender': 'GENDER',
        'male': 'MALE', 'female': 'FEMALE', 'goal': 'OBJECTIVE', 'bulk': 'HYPERTROPHY (Bulk)', 
        'cut': 'DEFINITION (Cut)', 'status': 'PLAYER STATUS', 'quest': 'DAILY QUEST LOG', 
        'complete': 'FINISH QUEST', 'bmi_label': 'BMI ANALYSIS'
    },
    'ar': {
        'awaken': 'صحوة اللاعب', 'name': 'الاسم الكودي', 'age': 'السن', 'gender': 'الجنس',
        'male': 'ذكر', 'female': 'أنثى', 'goal': 'الهدف التدريبي', 'bulk': 'تضخيم عضلي', 
        'cut': 'تنشيف / حرق دهون', 'status': 'حالة اللاعب', 'quest': 'سجل المهمات اليومية', 
        'complete': 'إتمام المهمة', 'bmi_label': 'تحليل كتلة الجسم'
    }
}

# أيقونة اللغة المصغرة في القائمة الجانبية
with st.sidebar:
    lang = st.selectbox("🌐", ["en", "ar"], index=0 if user['lang'] == 'en' else 1)
    if lang != user['lang']:
        user['lang'] = lang
        st.rerun()
L = strings[user['lang']]

# 5. شاشة إدخال البيانات (الصحوة)
if not user['initialized']:
    st.markdown(f"<h1 style='text-align:center;'>{L['awaken']}</h1>", unsafe_allow_html=True)
    with st.container():
        u_name = st.text_input(L['name'])
        c1, c2 = st.columns(2)
        u_age = c1.number_input(L['age'], 15, 60, 25)
        u_gender = c2.selectbox(L['gender'], [L['male'], L['female']])
        u_height = st.number_input("Height (cm)", 120, 220, 175)
        u_weight = st.number_input("Weight (kg)", 40, 200, 80)
        u_goal = st.selectbox(L['goal'], [L['bulk'], L['cut']])
        
        if st.button("ARISE"):
            bmi_val = round(u_weight / ((u_height/100)**2), 1)
            user.update({
                "name": u_name.upper(), "age": u_age, "gender": u_gender,
                "h": u_height, "w": u_weight, "goal": u_goal, "bmi": bmi_val,
                "initialized": True
            })
            with open("monarch_final.json", "w", encoding="utf-8") as f: json.dump(user, f)
            st.rerun()
    st.stop()

# 6. لوحة التحكم الرئيسية (Nexus Dashboard)
st.markdown(f"""
    <div class="status-window">
        <div style='display:flex; justify-content:space-between; font-size:12px;'>
            <span style='color:#00d4ff;'>{L['status']}</span>
            <span style='color:#ffcc00;'>RANK: E</span>
        </div>
        <h2 style='margin:10px 0;'>{user['name']}</h2>
        <div style='display:flex; justify-content:space-between; font-size:14px; color:#888;'>
            <span>LV. {user['lv']}</span>
            <span>{L['bmi_label']}: {user['bmi']}</span>
        </div>
        <div style='background:#111; height:6px; width:100%; margin-top:15px; border-radius:10px;'>
            <div style='background:#00d4ff; height:100%; width:{user['xp']}%; box-shadow:0 0 15px #00d4ff;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 7. المهمات والتمارين الاحترافية
st.write(f"### [ {L['quest']} ]")
exercise_db = {
    'CHEST': [("Incline Barbell Press", "4x8"), ("Flat DB Press", "4x10"), ("Cable Flys", "3x15")],
    'BACK': [("Deadlifts", "3x5"), ("Pull Ups", "4xMax"), ("Barbell Rows", "4x10")],
    'SHOULDERS': [("Military Press", "4x8"), ("Lateral Raises", "4x20"), ("Arnold Press", "3x10")],
    'LEGS': [("Squats", "4x8"), ("Leg Press", "3x12"), ("Leg Extensions", "4x15")]
}

target = st.selectbox("SELECT TARGET", ["...", "CHEST", "BACK", "SHOULDERS", "LEGS"], label_visibility="collapsed")

if target != "...":
    st.write(f"#### 📜 QUEST: {target}")
    for ex, reps in exercise_db[target]:
        st.info(f"**{ex}** - {reps}")
    
    if st.button(L['complete']):
        user['xp'] += 35
        if user['xp'] >= 100:
            user['xp'] = 0; user['lv'] += 1; st.balloons()
        with open("monarch_final.json", "w", encoding="utf-8") as f: json.dump(user, f)
        st.rerun()
