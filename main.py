import streamlit as st

# 1. نظام السواد المطلق والنيون (True Solo Leveling HUD)
st.set_page_config(page_title="SYSTEM HUD", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&family=Cairo:wght@400;700&display=swap');
    .stApp { background: #000 !important; color: #00d4ff !important; font-family: 'Cairo', sans-serif; }
    header, footer { display: none !important; }

    .system-notification {
        border: 2px solid #00d4ff; padding: 25px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.4); margin-bottom: 30px;
    }
    
    .exercise-card {
        background: rgba(0, 212, 255, 0.03);
        border: 1px solid #00d4ff22; border-left: 5px solid #00d4ff;
        padding: 15px; margin: 12px 0; border-radius: 4px;
    }
    .details { color: #ff00ff; font-family: 'Orbitron'; font-size: 13px; font-weight: bold; }

    /* إخفاء الزائد والناقص وإجبار السواد */
    [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }
    input, div[data-baseweb="input"], .stSelectbox div {
        background-color: #000 !important; color: #00d4ff !important;
        border: 1px solid #00d4ff33 !important;
    }
    label { color: #666 !important; font-size: 11px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic & Language
if 'lang' not in st.session_state: st.session_state.lang = 'AR'
if 'step' not in st.session_state: st.session_state.step = 'awakening'

U = {
    'EN': {'notify': 'SYSTEM NOTIFICATION', 'warn': '[WARNING: YOU HAVE BECOME A PLAYER]', 'arise': 'ARISE', 'sets': 'Sets', 'reps': 'Reps', 'rest': 'Rest'},
    'AR': {'notify': 'إشعار النظام', 'warn': '[تحذير: لقد أصبحت لاعباً الآن]', 'arise': 'نهوض', 'sets': 'مجموعات', 'reps': 'عدات', 'rest': 'راحة'}
}[st.session_state.lang]

# 3. ترسانة التمارين الكاملة (The Full Pro Database)
DB = {
    "PPL (Push/Pull/Legs)": {
        "PUSH (Chest/Shoulders/Triceps)": [
            {"name": "Flat Bench Press", "sets": 4, "reps": "8-10", "rest": "90s", "inj": "Shoulder", "alt": "Floor Press"},
            {"name": "Incline DB Press", "sets": 3, "reps": "10-12", "rest": "60s", "inj": "Shoulder", "alt": "Hex Press"},
            {"name": "Military Press", "sets": 3, "reps": "8-10", "rest": "90s", "inj": "Shoulder", "alt": "Landmine Press"},
            {"name": "Cable Lateral Raise", "sets": 4, "reps": "15", "rest": "45s", "inj": "Shoulder", "alt": "DB Lateral Raise"},
            {"name": "Tricep Pushdown", "sets": 3, "reps": "12-15", "rest": "45s", "inj": "Elbow", "alt": "Diamond Pushups"},
            {"name": "Overhead Extension", "sets": 3, "reps": "12", "rest": "60s", "inj": "Elbow", "alt": "Dips"}
        ],
        "PULL (Back/Biceps/Rear Delts)": [
            {"name": "Deadlift", "sets": 3, "reps": "5", "rest": "180s", "inj": "Back", "alt": "Leg Curls"},
            {"name": "Weighted Pullups", "sets": 3, "reps": "Max", "rest": "90s", "inj": "Shoulder", "alt": "Lat Pulldown"},
            {"name": "Barbell Rows", "sets": 4, "reps": "8-10", "rest": "90s", "inj": "Back", "alt": "Seated Rows"},
            {"name": "Face Pulls", "sets": 3, "reps": "15-20", "rest": "45s", "inj": "Shoulder", "alt": "Rear Delt Flys"},
            {"name": "Barbell Curls", "sets": 3, "reps": "10-12", "rest": "60s", "inj": "Elbow", "alt": "Hammer Curls"},
            {"name": "Hammer Curls", "sets": 3, "reps": "12", "rest": "45s", "inj": "Elbow", "alt": "Cable Curls"}
        ],
        "LEGS (Quads/Hams/Calves)": [
            {"name": "Back Squat", "sets": 4, "reps": "6-8", "rest": "120s", "inj": "Knee", "alt": "Leg Press"},
            {"name": "Romanian Deadlift", "sets": 3, "reps": "10-12", "rest": "90s", "inj": "Back", "alt": "Hamstring Curls"},
            {"name": "Leg Press", "sets": 3, "reps": "12-15", "rest": "60s", "inj": "Knee", "alt": "Goblet Squats"},
            {"name": "Leg Extensions", "sets": 3, "reps": "15", "rest": "45s", "inj": "Knee", "alt": "Sissy Squats"},
            {"name": "Seated Calf Raise", "sets": 4, "reps": "15-20", "rest": "45s", "inj": "Ankle", "alt": "Donkey Calves"},
            {"name": "Walking Lunges", "sets": 3, "reps": "12/leg", "rest": "60s", "inj": "Knee", "alt": "Bulgarian Split"}
        ]
    }
}

# --- Phase 1: Awakening ---
if st.session_state.step == 'awakening':
    col1, col2 = st.columns([5, 1])
    if col2.button("🌐"):
        st.session_state.lang = 'EN' if st.session_state.lang == 'AR' else 'AR'
        st.rerun()

    st.markdown(f'<div class="system-notification"><h1>{U["notify"]}</h1><p style="color:#ff00ff; font-weight:bold;">{U["warn"]}</p></div>', unsafe_allow_html=True)
    
    name = st.text_input("PLAYER NAME", placeholder="ADAM...")
    path = st.selectbox("TRAINING PATH", list(DB.keys()))
    injuries = st.multiselect("INJURY SCAN", ["Shoulder", "Back", "Knee", "Elbow", "Ankle"])
    
    cw, ch = st.columns(2)
    weight = cw.text_input("WEIGHT (KG)", "80")
    height = ch.text_input("HEIGHT (CM)", "175")

    if st.button(U['arise']):
        if name:
            st.session_state.player = {"name": name, "path": path, "injuries": injuries}
            st.session_state.step = 'active_mission'
            st.rerun()

# --- Phase 2: Combat HUD ---
elif st.session_state.step == 'active_mission':
    p = st.session_state.player
    st.markdown(f"### ⚡ PLAYER: {p['name'].upper()}")
    
    day = st.selectbox("SELECT SESSION", list(DB[p['path']].keys()))
    st.write("---")
    
    for ex in DB[p['path']][day]:
        with st.container():
            if ex['inj'] in p['injuries']:
                st.markdown(f"""<div class="exercise-card" style="border-color:#ff0055;">
                <span style="color:#ff0055; font-weight:bold;">⚠️ BLOCKED: {ex['name']}</span><br>
                <span class="details">REPLACE WITH: {ex['alt']} | {ex['sets']}x{ex['reps']}</span></div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class="exercise-card">
                <span style="font-weight:bold; letter-spacing:1px;">⚔️ {ex['name']}</span><br>
                <span class="details">{ex['sets']} {U['sets']} × {ex['reps']} {U['reps']} | ⏱️ {ex['rest']} {U['rest']}</span></div>""", unsafe_allow_html=True)
            st.checkbox(f"Mission Task Complete", key=ex['name'])

    if st.button("COLLECT REWARDS"):
        st.balloons()
        st.success("STATUS UPDATED! STRENGTH +1")
