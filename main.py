import streamlit as st
from datetime import datetime

# 1. تصميم الواجهة (The Monarch HUD - Bold Edition)
st.set_page_config(page_title="THE SYSTEM", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Cairo:wght@700;900&display=swap');
    
    .stApp { background: #000000 !important; color: #00d4ff !important; font-family: 'Cairo', 'Orbitron' !important; }
    header, footer { display: none !important; }

    /* إخفاء أزرار الزيادة والنقصان */
    button[step="1"], button[aria-label="Step up"], button[aria-label="Step down"] { display: none !important; }

    /* تصميم إشعار النظام (SYSTEM NOTIFICATION) - مطابق تماماً */
    .system-notification {
        background: rgba(0, 0, 0, 1); 
        border: 4px solid #00d4ff; /* حدود سميكة */
        padding: 30px; 
        text-align: center; 
        margin-bottom: 30px;
        box-shadow: 0 0 20px #00d4ff, inset 0 0 10px #00d4ff;
    }
    
    .system-notification h1 { font-family: 'Orbitron'; font-weight: 900; letter-spacing: 5px; margin: 0; color: #00d4ff; }
    .warning-text { color: #ff00ff; font-weight: bold; font-size: 18px; margin-top: 10px; }

    /* إجبار الخانات على السواد والخط العريض */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[role="listbox"], 
    li[role="option"], input, .stNumberInput div {
        background-color: #000000 !important; 
        color: #00d4ff !important; 
        border: 2px solid #00d4ff !important; /* حدود عريضة */
        font-weight: bold !important;
    }

    /* الأزرار الكبيرة */
    .stButton > button {
        width: 100%; background: #00d4ff11 !important; color: #00d4ff !important;
        border: 3px solid #00d4ff !important; font-family: 'Orbitron'; font-weight: 900;
        letter-spacing: 5px; padding: 20px !important; text-transform: uppercase;
    }
    .stButton > button:hover { background: #00d4ff33 !important; box-shadow: 0 0 30px #00d4ff; }
    
    label { color: #00d4ff !important; font-weight: 900 !important; font-size: 14px !important; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة النظام واللغة
if 'lang' not in st.session_state: st.session_state.lang = 'AR'
if 'step' not in st.session_state: st.session_state.step = 'awakening'

# زر تبديل اللغة (Top Right)
col_l1, col_l2 = st.columns([5, 1.5])
if col_l2.button("🌐 AR/EN"):
    st.session_state.lang = 'EN' if st.session_state.lang == 'AR' else 'AR'
    st.rerun()

UI = {
    'EN': {
        'notify': 'SYSTEM NOTIFICATION', 'warn': '[WARNING: YOU HAVE BECOME A PLAYER]',
        'id': 'PLAYER ID', 'gen': 'GENDER', 'path': 'SELECT TRAINING PATH', 'inj': 'INJURY SCAN',
        'arise': 'ARISE', 'quest': 'DAILY QUEST', 'comp': 'COLLECT REWARD'
    },
    'AR': {
        'notify': 'إشعار النظام', 'warn': '[تحذير: لقد أصبحت لاعباً الآن]',
        'id': 'معرف اللاعب', 'gen': 'الجنس', 'path': 'اختر مسار التدريب', 'inj': 'مسح الإصابات',
        'arise': 'نهوض', 'quest': 'المهمة اليومية', 'comp': 'تحصيل المكافأة'
    }
}
U = UI[st.session_state.lang]

# 3. قاعدة بيانات كل أنظمة التمرين
DB = {
    "PPL (Push/Pull/Legs)": {
        "Push": [{"AR": "بنش برس", "EN": "Bench Press", "i": "Shoulder"}, {"AR": "تجميع مائل", "EN": "Incline Press", "i": "Shoulder"}, {"AR": "عسكري بار", "EN": "Military Press", "i": "Shoulder"}, {"AR": "تراي كابل", "EN": "Tricep Push", "i": "Elbow"}],
        "Pull": [{"AR": "رفعة ميتة", "EN": "Deadlift", "i": "Back"}, {"AR": "عقلة", "EN": "Pullups", "i": "Shoulder"}, {"AR": "منشار دمبل", "EN": "DB Row", "i": "Back"}, {"AR": "باي بار", "EN": "Barbell Curls", "i": "Elbow"}],
        "Legs": [{"AR": "سكوات", "EN": "Squat", "i": "Knee"}, {"AR": "ليج برس", "EN": "Leg Press", "i": "Knee"}, {"AR": "خلفيات", "EN": "Hamstrings", "i": "Knee"}]
    },
    "Bro Split (Single Muscle)": {
        "Chest": [{"AR": "بنش برس", "EN": "Flat Bench", "i": "Shoulder"}, {"AR": "تجميع دمبل", "EN": "DB Flys", "i": "Shoulder"}],
        "Back": [{"AR": "سحب عالي", "EN": "Lat Pulldown", "i": "Back"}, {"AR": "سحب أرضي", "EN": "Seated Row", "i": "Back"}],
        "Legs": [{"AR": "سكوات", "EN": "Squats", "i": "Knee"}],
        "Shoulders": [{"AR": "ضغط دمبل", "EN": "DB Press", "i": "Shoulder"}, {"AR": "رفرفة", "EN": "Lat Raise", "i": "Shoulder"}],
        "Arms": [{"AR": "باي بار", "EN": "BB Curls", "i": "Elbow"}, {"AR": "تراي فرنسي", "EN": "French Press", "i": "Elbow"}]
    },
    "Upper/Lower Body": {
        "Upper": [{"AR": "بنش برس", "EN": "Bench Press", "i": "Shoulder"}, {"AR": "سحب عالي", "EN": "Lat Pulldown", "i": "Back"}],
        "Lower": [{"AR": "سكوات", "EN": "Squat", "i": "Knee"}, {"AR": "رفعة ميتة", "EN": "Deadlift", "i": "Back"}]
    }
}

# --- المرحلة الأولى: Awakening ---
if st.session_state.step == 'awakening':
    st.markdown(f'<div class="system-notification"><h1>{U["notify"]}</h1><p class="warning-text">{U["warn"]}</p></div>', unsafe_allow_html=True)
    
    u_id = st.text_input(U['id'], placeholder="NAME...")
    col1, col2 = st.columns(2)
    u_gen = col1.selectbox(U['gen'], ["MALE (Hunter)", "FEMALE (Huntress)"])
    u_path = col2.selectbox(U['path'], list(DB.keys()))
    
    u_inj = st.multiselect(U['inj'], ["Shoulder", "Back", "Knee", "Elbow", "Ankle"])
    
    cw, ch = st.columns(2)
    u_w = cw.number_input("WEIGHT (KG)", min_value=10, value=80)
    u_h = ch.number_input("HEIGHT (CM)", min_value=100, value=175)

    if st.button(U['arise']):
        if u_id:
            st.session_state.player = {"id": u_id, "path": u_path, "inj": u_inj, "rank": "S-RANK"}
            st.session_state.step = 'status'
            st.rerun()

# --- المرحلة الثانية: Combat HUD ---
elif st.session_state.step == 'status':
    p = st.session_state.player
    st.markdown(f"### ⚔️ {U['quest']} | {p['id'].upper()} [{p['rank']}]")
    
    zone = st.selectbox("ZONE", list(DB[p['path']].keys()))
    for i, ex in enumerate(DB[p['path']][zone]):
        name = ex[st.session_state.lang]
        if ex['i'] in p['inj']:
            st.markdown(f"<p style='color:#ff0055;'>❌ [STRICT SKIP] {name}</p>", unsafe_allow_html=True)
        else:
            st.checkbox(f"⚔️ {name}", key=f"ex_{i}")
    
    if st.button(U['comp']):
        st.balloons()
        st.success("MISSION COMPLETE. REWARD DELIVERED.")

    if st.sidebar.button("TERMINATE"):
        st.session_state.step = 'awakening'
        st.rerun()
