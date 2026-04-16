import streamlit as st
from datetime import datetime

# 1. إعدادات HUD (Zero White - Neon Warning System)
st.set_page_config(page_title="SYSTEM HUD", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    header, footer, [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }
    
    .system-card {
        background: rgba(0, 20, 40, 0.4); border: 1px solid rgba(0, 212, 255, 0.2);
        padding: 20px; border-radius: 2px; margin-bottom: 20px;
    }
    
    .injury-warn {
        color: #ffaa00; border: 1px solid #ffaa00; padding: 5px;
        font-size: 10px; border-radius: 2px; margin-left: 10px;
    }

    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {
        background-color: #050505 !important; border: 1px solid #00d4ff44 !important; color: #00d4ff !important;
    }
    input { color: #00d4ff !important; background: transparent !important; }

    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة البيانات والإصابات
if 'history' not in st.session_state: st.session_state.history = []
if 'level' not in st.session_state: st.session_state.level = 1
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'step' not in st.session_state: st.session_state.step = 'awakening'
if 'lang' not in st.session_state: st.session_state.lang = 'AR'

# قاعدة بيانات التمارين مع وسوم الإصابات
# "injury": العضو المتأثر بالتمرين
EXERCISES_DB = {
    "PPL": {
        "Push": [
            {"name": "Bench Press", "injury": "Shoulder"},
            {"name": "Incline DB Press", "injury": "Shoulder"},
            {"name": "Lateral Raises", "injury": "Shoulder"},
            {"name": "Tricep Pushdowns", "injury": "Elbow"},
            {"name": "Push-ups", "injury": "Wrist"}
        ],
        "Pull": [
            {"name": "Lat Pulldowns", "injury": "Shoulder"},
            {"name": "Deadlifts", "injury": "Back"},
            {"name": "Seated Rows", "injury": "Back"},
            {"name": "Bicep Curls", "injury": "Elbow"},
            {"name": "Face Pulls", "injury": "Shoulder"}
        ],
        "Legs": [
            {"name": "Squats", "injury": "Knee"},
            {"name": "Leg Press", "injury": "Knee"},
            {"name": "Leg Curls", "injury": "Knee"},
            {"name": "Calf Raises", "injury": "Ankle"},
            {"name": "Lunges", "injury": "Knee"}
        ]
    }
}

# أيقونة اللغة
if st.sidebar.button("🌐"):
    st.session_state.lang = 'EN' if st.session_state.lang == 'AR' else 'AR'
    st.rerun()

# --- المرحلة الأولى: Awakening (Scan) ---
if st.session_state.step == 'awakening':
    st.markdown('<div class="system-card" style="text-align:center;"><h1>SYSTEM SCAN</h1><p>تحديد الحالة الحيوية والقيود</p></div>', unsafe_allow_html=True)
    
    u_name = st.text_input("PLAYER ID")
    u_gender = st.selectbox("GENDER", ["MALE (Hunter)", "FEMALE (Huntress)"])
    u_split = st.selectbox("PATH", ["PPL"])
    
    # قسم الإصابات الجديد
    u_injuries = st.multiselect("INJURY SCAN (حدد الإصابات الحالية)", ["Shoulder", "Back", "Knee", "Elbow", "Wrist", "Ankle"])
    
    colw, colh = st.columns(2)
    u_w = colw.number_input("WEIGHT", value=80)
    u_h = colh.number_input("HEIGHT", value=175)

    if st.button("ARISE"):
        if u_name:
            st.session_state.player = {"name": u_name, "gender": u_gender, "split": u_split, "injuries": u_injuries}
            st.session_state.step = 'dashboard'
            st.rerun()

# --- المرحلة الثانية: Dashboard (Safe Training) ---
elif st.session_state.step == 'dashboard':
    p = st.session_state.player
    st.markdown(f"**PLAYER:** {p['name'].upper()} | **LVL:** {st.session_state.level}")
    
    tab1, tab2 = st.tabs(["DAILY QUEST", "PLAYER LOG"])

    with tab1:
        day_options = list(EXERCISES_DB[p['split']].keys())
        target_zone = st.selectbox("SELECT MISSION ZONE", day_options)
        
        st.markdown(f'<div class="system-card"><b>ACTIVE QUEST: {target_zone}</b></div>', unsafe_allow_html=True)
        
        exercises = EXERCISES_DB[p['split']][target_zone]
        
        completed_count = 0
        visible_exercises = 0
        
        for i, ex in enumerate(exercises):
            # نظام الفلترة الذكي
            if ex['injury'] in p['injuries']:
                # إذا كان التمرين يؤثر على إصابة اللاعب، يظهر تحذير ويتم تعطيل التمرين أو حثه على التغيير
                st.markdown(f"⚠️ <del>{ex['name']}</del> <span class='injury-warn'>عطلنا هذا التمرين بسبب إصابة الـ {ex['injury']}</span>", unsafe_allow_html=True)
            else:
                if st.checkbox(f"⚔️ {ex['name']}", key=f"ex_{i}"):
                    completed_count += 1
                visible_exercises += 1
        
        if st.button("COMPLETE QUEST"):
            if completed_count == visible_exercises and visible_exercises > 0:
                log_entry = {"date": datetime.now().strftime("%y-%m-%d %H:%M"), "task": target_zone}
                st.session_state.history.append(log_entry)
                st.session_state.xp += 34
                if st.session_state.xp >= 100:
                    st.session_state.level += 1
                    st.session_state.xp = 0
                st.rerun()
            else:
                st.error("المهمة لم تكتمل أو لا يوجد تمارين آمنة متاحة!")

    with tab2:
        for entry in reversed(st.session_state.history):
            st.markdown(f"**{entry['date']}** | {entry['task']} [SUCCESS]")

    if st.sidebar.button("TERMINATE"):
        st.session_state.step = 'awakening'
        st.rerun()
