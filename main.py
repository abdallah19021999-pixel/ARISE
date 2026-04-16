import streamlit as st

# 1. بروتوكول التصميم المحترف (Neon Pro HUD)
st.set_page_config(page_title="SYSTEM HUD", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&family=Cairo:wght@400;700&display=swap');
    .stApp { background: #000 !important; color: #00d4ff !important; font-family: 'Orbitron', 'Cairo'; }
    header, footer { display: none !important; }

    /* توهج نيون احترافي للصندوق */
    .system-notification {
        border: 1px solid #00d4ff; padding: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3); margin-bottom: 30px;
    }

    /* إخفاء الزائد والناقص وسواد الخانات */
    [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }
    input, div[data-baseweb="input"], .stSelectbox div {
        background-color: #000 !important; color: #00d4ff !important;
        border: 1px solid #00d4ff33 !important;
    }
    label { color: #444 !important; font-size: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة واللغة
if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'step' not in st.session_state: st.session_state.step = 'awakening'

U = {
    'EN': {'notify': 'SYSTEM NOTIFICATION', 'warn': '[WARNING: YOU HAVE BECOME A PLAYER]', 'arise': 'ARISE'},
    'AR': {'notify': 'إشعار النظام', 'warn': '[تحذير: لقد أصبحت لاعباً الآن]', 'arise': 'نهوض'}
}[st.session_state.lang]

# 3. قاعدة بيانات ذكية (Smart Exercise Engine)
# التمارين متصنفة حسب نوع الحركة والعضلة المصابة
DB = {
    "PPL (Push/Pull/Legs)": {
        "PUSH": [
            {"name": "Bench Press", "target": "Chest", "inj": "Shoulder", "alt": "Floor Press"},
            {"name": "Military Press", "target": "Shoulder", "inj": "Shoulder", "alt": "Landmine Press"},
            {"name": "Tricep Pushdown", "target": "Triceps", "inj": "Elbow", "alt": "Diamond Pushups"}
        ],
        "PULL": [
            {"name": "Deadlift", "target": "Back", "inj": "Back", "alt": "Leg Curls"},
            {"name": "Barbell Row", "target": "Back", "inj": "Back", "alt": "Face Pulls"},
            {"name": "Bicep Curls", "target": "Biceps", "inj": "Elbow", "alt": "Hammer Curls"}
        ],
        "LEGS": [
            {"name": "Back Squat", "target": "Quads", "inj": "Knee", "alt": "Leg Press"},
            {"name": "Leg Extension", "target": "Quads", "inj": "Knee", "alt": "Goblet Squat"}
        ]
    },
    "Bro Split": {
        "CHEST": [{"name": "Flat Bench", "target": "Chest", "inj": "Shoulder", "alt": "Pushups"}],
        "BACK": [{"name": "Lat Pulldown", "target": "Back", "inj": "Back", "alt": "Pullover"}]
    }
}

# --- واجهة البداية ---
if st.session_state.step == 'awakening':
    col_l1, col_l2 = st.columns([5, 1])
    if col_l2.button("🌐"):
        st.session_state.lang = 'AR' if st.session_state.lang == 'EN' else 'EN'
        st.rerun()

    st.markdown(f'<div class="system-notification"><h1>{U["notify"]}</h1><p style="color:#ff00ff;">{U["warn"]}</p></div>', unsafe_allow_html=True)
    
    name = st.text_input("PLAYER NAME", placeholder="ADAM...")
    path = st.selectbox("TRAINING PATH", list(DB.keys()))
    injuries = st.multiselect("INJURY SCAN", ["Shoulder", "Back", "Knee", "Elbow"])
    
    col_w, col_h = st.columns(2)
    weight = col_w.text_input("WEIGHT", "80")
    height = col_h.text_input("HEIGHT", "175")

    if st.button(U['arise']):
        if name:
            st.session_state.player = {"name": name, "path": path, "injuries": injuries}
            st.session_state.step = 'active_mission'
            st.rerun()

# --- واجهة المهام التفاعلية (The Live HUD) ---
elif st.session_state.step == 'active_mission':
    p = st.session_state.player
    st.markdown(f"### ⚡ PLAYER: {p['name'].upper()}")
    
    # تفاعل 1: اختيار اليوم بناءً على النظام المختار
    day = st.selectbox("SELECT CURRENT SESSION", list(DB[p['path']].keys()))
    
    st.markdown(f"**CURRENT MISSION: {day} DAY**")
    st.write("---")
    
    # تفاعل 2: فلترة التمارين بناءً على الإصابات تلقائياً
    for ex in DB[p['path']][day]:
        if ex['inj'] in p['injuries']:
            # لو العضلة مصابة، يظهر البديل فوراً مع تحذير
            st.markdown(f"⚠️ **{ex['name']}** [BLOCKED BY INJURY]")
            st.checkbox(f"⚔️ SAFE ALT: {ex['alt']}", key=ex['alt'])
        else:
            # لو سليم، يظهر التمرين العادي
            st.checkbox(f"⚔️ {ex['name']}", key=ex['name'])

    if st.button("COMPLETE MISSION"):
        st.success("STATUS UPDATED! +50 XP")
    
    if st.sidebar.button("RESET SYSTEM"):
        st.session_state.step = 'awakening'
        st.rerun()
