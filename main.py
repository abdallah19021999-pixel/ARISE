import streamlit as st

# 1. نظام الواجهة الاحترافية (True Black & Neon HUD)
st.set_page_config(page_title="SYSTEM HUD", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&family=Cairo:wght@400;700&display=swap');
    .stApp { background: #000 !important; color: #00d4ff !important; font-family: 'Cairo', sans-serif; }
    header, footer { display: none !important; }

    /* توهج نيون احترافي لصندوق التنبيه */
    .system-notification {
        border: 2px solid #00d4ff; padding: 25px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.4), inset 0 0 10px rgba(0, 212, 255, 0.1);
        margin-bottom: 30px;
    }

    /* تدمير الرمادي في كل الخانات (بما فيها الإصابات والوزن) */
    input, div[data-baseweb="input"], .stSelectbox div, .stMultiSelect div, div[role="combobox"] {
        background-color: #000000 !important; 
        color: #00d4ff !important; 
        border: 1px solid #00d4ff44 !important;
    }
    
    /* جعل تاجات الإصابات سوداء نيون */
    .stMultiSelect span { background-color: #00d4ff15 !important; color: #00d4ff !important; border: 1px solid #00d4ff33; }

    /* إخفاء الزوائد (الزائد والناقص) */
    [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }

    /* كروت التمارين */
    .exercise-card {
        background: rgba(0, 212, 255, 0.04); border-left: 5px solid #00d4ff;
        padding: 15px; margin: 12px 0; border-radius: 4px;
    }
    .details { color: #ff00ff; font-family: 'Orbitron'; font-size: 13px; font-weight: 600; }

    label { color: #666 !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة واللغة
if 'lang' not in st.session_state: st.session_state.lang = 'AR'
if 'step' not in st.session_state: st.session_state.step = 'awakening'

U = {
    'EN': {'notify': 'SYSTEM NOTIFICATION', 'warn': '[WARNING: YOU HAVE BECOME A PLAYER]', 'arise': 'ARISE', 'sets': 'Sets', 'reps': 'Reps', 'rest': 'Rest'},
    'AR': {'notify': 'إشعار النظام', 'warn': '[تحذير: لقد أصبحت لاعباً الآن]', 'arise': 'نهوض', 'sets': 'مجموعات', 'reps': 'عدات', 'rest': 'راحة'}
}[st.session_state.lang]

# 3. الأنظمة التدريبية (الترسانة الكاملة)
DB = {
    "PPL (Push/Pull/Legs)": {
        "PUSH": [
            {"name": "Bench Press", "sets": 4, "reps": "8-10", "rest": "90s", "inj": "Shoulder"},
            {"name": "Incline DB Press", "sets": 3, "reps": "10-12", "rest": "60s", "inj": "Shoulder"},
            {"name": "Military Press", "sets": 3, "reps": "8-10", "rest": "90s", "inj": "Shoulder"},
            {"name": "Lateral Raise", "sets": 4, "reps": "15", "rest": "45s", "inj": "Shoulder"},
            {"name": "Tricep Pushdown", "sets": 3, "reps": "12-15", "rest": "45s", "inj": "Elbow"}
        ],
        "PULL": [
            {"name": "Deadlift", "sets": 3, "reps": "5", "rest": "180s", "inj": "Back"},
            {"name": "Lat Pulldown", "sets": 4, "reps": "10-12", "rest": "60s", "inj": "Shoulder"},
            {"name": "Barbell Row", "sets": 4, "reps": "8-10", "rest": "90s", "inj": "Back"},
            {"name": "Bicep Curls", "sets": 3, "reps": "12", "rest": "45s", "inj": "Elbow"}
        ],
        "LEGS": [
            {"name": "Back Squat", "sets": 4, "reps": "6-8", "rest": "120s", "inj": "Knee"},
            {"name": "Leg Press", "sets": 3, "reps": "12-15", "rest": "60s", "inj": "Knee"},
            {"name": "Calf Raise", "sets": 4, "reps": "15-20", "rest": "45s", "inj": "Ankle"}
        ]
    },
    "Bro Split (PRO)": {
        "CHEST": [{"name": "Flat Bench", "sets": 4, "reps": "10", "rest": "90s", "inj": "Shoulder"}],
        "BACK": [{"name": "Seated Row", "sets": 4, "reps": "12", "rest": "60s", "inj": "Back"}]
    },
    "Upper/Lower Body": {
        "UPPER": [{"name": "Bench Press", "sets": 3, "reps": "8-10", "rest": "90s", "inj": "Shoulder"}],
        "LOWER": [{"name": "Squat", "sets": 3, "reps": "8-10", "rest": "120s", "inj": "Knee"}]
    }
}

# --- Phase 1: Awakening (إدخال البيانات) ---
if st.session_state.step == 'awakening':
    st.markdown(f'<div class="system-notification"><h1>{U["notify"]}</h1><p style="color:#ff00ff; font-weight:bold;">{U["warn"]}</p></div>', unsafe_allow_html=True)
    
    u_id = st.text_input("PLAYER NAME", placeholder="ADAM...")
    
    col1, col2 = st.columns(2)
    # رجعنا تحديد الجنس والمسار كما طلبت
    u_gen = col1.selectbox("GENDER", ["MALE (Hunter)", "FEMALE (Huntress)"])
    u_path = col2.selectbox("TRAINING PATH", list(DB.keys()))
    
    u_inj = st.multiselect("INJURY SCAN", ["Shoulder", "Back", "Knee", "Elbow", "Ankle"])
    
    cw, ch = st.columns(2)
    # بروتوكول السواد المطلق للوزن والطول
    u_w = cw.text_input("WEIGHT (KG)", "80")
    u_h = ch.text_input("HEIGHT (CM)", "175")

    if st.button(U['arise']):
        if u_id:
            st.session_state.player = {"name": u_id, "gen": u_gen, "path": u_path, "injuries": u_inj}
            st.session_state.step = 'mission'
            st.rerun()

# --- Phase 2: Combat HUD (عرض التمارين) ---
elif st.session_state.step == 'mission':
    p = st.session_state.player
    st.markdown(f"### ⚡ PLAYER: {p['name'].upper()} | ROLE: {p['gen']}")
    
    day = st.selectbox("SELECT MISSION SESSION", list(DB[p['path']].keys()))
    st.write("---")
    
    for ex in DB[p['path']][day]:
        if ex['inj'] in p['injuries']:
            st.markdown(f"<div class='exercise-card' style='border-color:#ff0055;'><p style='color:#ff0055; margin:0;'>⚠️ BLOCKED: {ex['name']} (Injury Detected)</p></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="exercise-card">
            <span style="font-weight:bold;">⚔️ {ex['name']}</span><br>
            <span class="details">{ex['sets']} {U['sets']} x {ex['reps']} {U['reps']} | ⏱️ {ex['rest']} {U['rest']}</span></div>""", unsafe_allow_html=True)
            st.checkbox(f"Task Complete", key=ex['name'])

    if st.sidebar.button("RESET SYSTEM"):
        st.session_state.step = 'awakening'
        st.rerun()
