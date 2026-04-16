import streamlit as st

# 1. نظام الخلفية السينمائية والنيون (Solo Leveling Cinematic HUD)
st.set_page_config(page_title="SYSTEM HUD", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&family=Cairo:wght@400;700&display=swap');
    
    /* خلفية سولو ليفلينج: تدرج احترافي متحرك */
    .stApp {
        background: radial-gradient(circle at center, #001525 0%, #000000 100%) !important;
        background-attachment: fixed;
        color: #00d4ff !important;
        font-family: 'Cairo', sans-serif;
    }

    /* إضافة طبقة خفيفة من الخطوط الرقمية (Scanlines) لإعطاء تأثير الشاشة */
    .stApp::before {
        content: " ";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.2) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.02));
        background-size: 100% 4px, 3px 100%;
        z-index: -1;
        pointer-events: none;
    }

    header, footer { display: none !important; }

    /* توهج العنوان والرسائل */
    @keyframes glowPulse {
        0% { text-shadow: 0 0 5px #00d4ff, 0 0 10px #00d4ff; }
        50% { text-shadow: 0 0 20px #00d4ff, 0 0 30px #00d4ff; opacity: 0.9; }
        100% { text-shadow: 0 0 5px #00d4ff, 0 0 10px #00d4ff; }
    }

    .system-title {
        font-family: 'Orbitron'; color: #00d4ff; text-align: center;
        animation: glowPulse 3s infinite ease-in-out; letter-spacing: 4px;
        background: rgba(0, 212, 255, 0.05); padding: 20px; border-radius: 10px;
    }

    /* كروت التمارين الزجاجية (Glassmorphism) */
    .exercise-card {
        background: rgba(0, 212, 255, 0.07);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-left: 5px solid #00d4ff;
        padding: 18px; margin: 15px 0; border-radius: 4px;
        transition: all 0.3s ease;
    }
    .exercise-card:hover { 
        background: rgba(0, 212, 255, 0.15); 
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(0, 212, 255, 0.3);
    }

    /* كارت البديل (Safe Mode) بلون البوابة البنفسجية */
    .alt-card {
        background: rgba(255, 0, 255, 0.07);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 0, 255, 0.3);
        border-left: 5px solid #ff00ff;
        padding: 18px; margin: 15px 0; border-radius: 4px;
    }

    /* تدمير الرمادي المطلق */
    input, div[data-baseweb="input"], .stSelectbox div, .stMultiSelect div {
        background-color: rgba(0, 0, 0, 0.8) !important; color: #00d4ff !important;
        border: 1px solid #00d4ff44 !important;
    }
    
    [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }
    label { color: #888 !important; font-size: 11px !important; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic & Database (تطوير البدائل والأنظمة)
if 'step' not in st.session_state: st.session_state.step = 'awakening'

DB = {
    "PPL (Push/Pull/Legs)": {
        "PUSH": [
            {"name": "Bench Press", "sets": 4, "reps": "8-10", "inj": "Front Shoulder", "alt": "Floor Press"},
            {"name": "Military Press", "sets": 3, "reps": "10", "inj": "Side Shoulder", "alt": "Landmine Press"},
            {"name": "Tricep Pushdown", "sets": 3, "reps": "15", "inj": "Elbow Joint", "alt": "Single Arm Extensions"}
        ],
        "PULL": [
            {"name": "Deadlift", "sets": 3, "reps": "5", "inj": "Lower Back", "alt": "Lat Pulldowns (Strict)"},
            {"name": "Barbell Rows", "sets": 4, "reps": "10", "inj": "Lower Back", "alt": "Chest Supported Rows"},
            {"name": "Hammer Curls", "sets": 3, "reps": "12", "inj": "Wrist/Forearm", "alt": "Spider Curls"}
        ],
        "LEGS": [
            {"name": "Back Squat", "sets": 4, "reps": "8", "inj": "Knee Joint", "alt": "Leg Press"},
            {"name": "RDL", "sets": 3, "reps": "12", "inj": "Lower Back", "alt": "Leg Curls"}
        ]
    }
}

# --- Phase 1: Awakening ---
if st.session_state.step == 'awakening':
    st.markdown('<div class="system-title"><h1>SYSTEM NOTIFICATION</h1></div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#ff00ff; animation: glowPulse 2s infinite; font-weight:bold;">[WARNING: YOU HAVE BECOME A PLAYER]</p>', unsafe_allow_html=True)
    
    u_id = st.text_input("PLAYER NAME", placeholder="ADAM...")
    c1, c2 = st.columns(2)
    u_gen = c1.selectbox("GENDER", ["MALE (Hunter)", "FEMALE (Huntress)"])
    u_path = c2.selectbox("TRAINING PATH", list(DB.keys()))
    
    u_inj = st.multiselect("DETAILED INJURY SCAN", [
        "Front Shoulder", "Side Shoulder", "Rear Shoulder", "Lower Back", 
        "Upper Back", "Elbow Joint", "Wrist/Forearm", "Knee Joint", "Ankle"
    ])
    
    cw, ch = st.columns(2)
    u_w = cw.text_input("WEIGHT (KG)", "80")
    u_h = ch.text_input("HEIGHT (CM)", "175")

    if st.button("ARISE"):
        if u_id:
            st.session_state.player = {"name": u_id, "gen": u_gen, "path": u_path, "inj": u_inj}
            st.session_state.step = 'mission'
            st.rerun()

# --- Phase 2: Mission HUD ---
elif st.session_state.step == 'mission':
    p = st.session_state.player
    st.markdown(f"### ⚡ PLAYER: {p['name'].upper()} | ROLE: {p['gen']}")
    
    day = st.selectbox("SELECT MISSION SESSION", list(DB[p['path']].keys()))
    st.write("---")
    
    for ex in DB[p['path']][day]:
        if ex['inj'] in p['inj']:
            st.markdown(f"""<div class='alt-card'>
            <span style='color:#ff00ff; font-weight:bold;'>🔄 ADAPTATION: {ex['inj']}</span><br>
            <span style='font-size:18px; color:#00d4ff;'>⚔️ {ex['alt']}</span><br>
            <span style='font-size:12px; opacity:0.8;'>{ex['sets']} SETS x {ex['reps']} REPS</span></div>""", unsafe_allow_html=True)
            st.checkbox(f"Mission Task Clear", key=ex['alt'])
        else:
            st.markdown(f"""<div class="exercise-card">
            <span style="font-weight:bold; letter-spacing:1px;">⚔️ {ex['name']}</span><br>
            <span style="color:#ff00ff; font-family:'Orbitron'; font-size:12px;">{ex['sets']} SETS x {ex['reps']} REPS</span>
            </div>""", unsafe_allow_html=True)
            st.checkbox(f"Mission Task Clear", key=ex['name'])

    if st.sidebar.button("RESET SYSTEM"):
        st.session_state.step = 'awakening'
        st.rerun()
