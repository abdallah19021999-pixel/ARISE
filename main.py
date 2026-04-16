import streamlit as st
import json
import os

# 1. إعدادات النظام - Solo Leveling Elite
st.set_page_config(page_title="ARISE: MONARCH SYSTEM", page_icon="⚡", layout="centered")

# 2. تصميم الواجهة (The Dark Abyss UI) - القضاء على اللون الأبيض تماماً
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');

    .stApp {
        background-color: #00050a;
        background-image: radial-gradient(circle at center, #001a33 0%, #00050a 100%);
        color: #e0f2ff;
    }

    /* إخفاء اللون الأبيض من كل العناصر */
    div[data-baseweb="input"], div[data-baseweb="select"], .stSelectbox div, .stNumberInput div {
        background-color: #0d1117 !important;
        border: 1px solid #00d4ff !important;
        color: #00d4ff !important;
    }
    
    /* تعديل لون الخط في القوائم المنسدلة */
    div[role="listbox"] { background-color: #0d1117 !important; color: #00d4ff !important; }
    div[data-baseweb="popover"] { background-color: #0d1117 !important; }
    
    p, label, span, h1, h2, h3 { color: #e0f2ff !important; font-family: 'Cairo', sans-serif; }
    
    /* كارت الحالة الاحترافي */
    .status-window {
        border: 2px solid #00d4ff;
        background: rgba(0, 20, 40, 0.9);
        padding: 20px;
        box-shadow: 0 0 25px #00d4ff44;
        margin-bottom: 25px;
        border-radius: 5px;
        font-family: 'Orbitron', sans-serif;
    }

    /* أزرار العضلات النيون */
    .stButton > button {
        width: 100%; height: 50px; background: #000; color: #00d4ff;
        border: 1px solid #00d4ff; font-family: 'Orbitron', sans-serif;
        transition: 0.4s; margin-bottom: 10px; font-weight: bold;
    }
    .stButton > button:hover {
        background: #00d4ff; color: #000; box-shadow: 0 0 20px #00d4ff;
    }

    /* صناديق التمارين الاحترافية */
    .ex-card {
        background: rgba(0, 212, 255, 0.05);
        border-left: 4px solid #00d4ff;
        padding: 15px; margin: 10px 0;
        text-align: left;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات الذكية (تجنب الـ KeyError للأبد)
def load_data():
    default = {
        "name": "HUNTER", "age": 25, "gender": "Male", "h": 175, "w": 80, 
        "goal": "Bulk", "bmi": 26.1, "lv": 1, "xp": 0, "initialized": False, "lang": "en"
    }
    if os.path.exists("monarch_pro.json"):
        try:
            with open("monarch_pro.json", "r", encoding="utf-8") as f:
                saved = json.load(f)
                return {**default, **saved} # دمج البيانات لضمان عدم وجود Key ناقص
        except: return default
    return default

if 'user' not in st.session_state:
    st.session_state.user = load_data()
user = st.session_state.user

# 4. ترجمة النظام
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

# أيقونة لغة مصغرة جداً في الـ Sidebar
with st.sidebar:
    lang = st.selectbox("🌐", ["en", "ar"], index=0 if user['lang'] == 'en' else 1, label_visibility="collapsed")
    if lang != user['lang']:
        user['lang'] = lang
        st.rerun()
L = strings[user['lang']]

# 5. شاشة إدخال البيانات (الصحوة)
if not user['initialized']:
    st.markdown(f"<h1 style='text-align:center; color:#00d4ff;'>{L['awaken']}</h1>", unsafe_allow_html=True)
    with st.form("awakening_form"):
        u_name = st.text_input(L['name'])
        col_a, col_g = st.columns(2)
        u_age = col_a.number_input(L['age'], 15, 60, 25)
        u_gender = col_g.selectbox(L['gender'], [L['male'], L['female']])
        u_height = st.number_input("Height (cm)", 120, 220, 175)
        u_weight = st.number_input("Weight (kg)", 40, 200, 80)
        u_goal = st.selectbox(L['goal'], [L['bulk'], L['cut']])
        
        if st.form_submit_button("ARISE"):
            bmi_val = round(u_weight / ((u_height/100)**2), 1)
            user.update({
                "name": u_name.upper(), "age": u_age, "gender": u_gender,
                "h": u_height, "w": u_weight, "goal": u_goal, "bmi": bmi_val,
                "initialized": True
            })
            with open("monarch_pro.json", "w", encoding="utf-8") as f: json.dump(user, f)
            st.rerun()
    st.stop()

# 6. الواجهة الاحترافية (Status Dashboard)
st.markdown(f"""
    <div class="status-window">
        <div style='display:flex; justify-content:space-between; font-size:12px;'>
            <span style='color:#00d4ff;'>{L['status']}</span>
            <span style='color:#ffcc00;'>RANK: E</span>
        </div>
        <h2 style='margin:10px 0; color:white;'>{user['name']}</h2>
        <div style='display:flex; justify-content:space-between; font-size:14px; color:#888;'>
            <span>LV. {user['lv']}</span>
            <span>{L['bmi_label']}: {user.get('bmi', 'N/A')}</span>
        </div>
        <div style='background:#111; height:6px; width:100%; margin-top:15px; border-radius:10px;'>
            <div style='background:#00d4ff; height:100%; width:{user['xp']}%; box-shadow:0 0 15px #00d4ff;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 7. سجل المهمات (التمارين الاحترافية)
st.write(f"### [ {L['quest']} ]")
col1, col2 = st.columns(2)

exercise_db = {
    'CHEST': [("Incline Barbell Press", "4 Sets x 8 Reps"), ("Flat Dumbbell Press", "4 Sets x 10 Reps"), ("Cable Flys", "3 Sets x 15 Reps"), ("Dips (Weighted)", "3 Sets x 12 Reps")],
    'BACK': [("Deadlifts", "3 Sets x 5 Reps"), ("Pull Ups", "4 Sets x Failure"), ("Barbell Rows", "4 Sets x 10 Reps"), ("Lat Pulldowns", "4 Sets x 12 Reps")],
    'SHOULDERS': [("Overhead Press", "4 Sets x 8 Reps"), ("Lateral Raises", "4 Sets x 20 Reps"), ("Rear Delt Flys", "3 Sets x 15 Reps"), ("Arnold Press", "3 Sets x 10 Reps")],
    'LEGS': [("Barbell Squats", "4 Sets x 8 Reps"), ("Leg Press", "3 Sets x 12 Reps"), ("Leg Extensions", "4 Sets x 15 Reps"), ("Romanian Deadlift", "4 Sets x 10 Reps")]
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
    for ex, reps in exercise_db.get(target, []):
        st.markdown(f"<div class='ex-card'><b>{ex}</b><br><small style='color:#00d4ff;'>{reps}</small></div>", unsafe_allow_html=True)
    
    if st.button(f"🔥 {L['complete']}"):
        user['xp'] += 35
        if user['xp'] >= 100:
            user['xp'] = 0; user['lv'] += 1; st.balloons()
        with open("monarch_pro.json", "w", encoding="utf-8") as f: json.dump(user, f)
        st.rerun()

# تصفير النظام من الـ Sidebar
with st.sidebar:
    if st.button("SYSTEM RESET"):
        if os.path.exists("monarch_pro.json"): os.remove("monarch_pro.json")
        st.session_state.clear(); st.rerun()
