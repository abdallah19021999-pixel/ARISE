import streamlit as st

# 1. نظام الأنيميشن والنيون المتطور (Dynamic Motion HUD)
st.set_page_config(page_title="SYSTEM HUD", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&family=Cairo:wght@400;700&display=swap');
    
    .stApp { background: #000000 !important; color: #00d4ff !important; font-family: 'Cairo', sans-serif; }
    header, footer { display: none !important; }

    /* أنيميشن الكلمات (Breathing & Glow) */
    @keyframes glowPulse {
        0% { text-shadow: 0 0 5px #00d4ff, 0 0 10px #00d4ff; }
        50% { text-shadow: 0 0 20px #00d4ff, 0 0 30px #00d4ff; opacity: 0.8; }
        100% { text-shadow: 0 0 5px #00d4ff, 0 0 10px #00d4ff; }
    }

    .system-title {
        font-family: 'Orbitron'; color: #00d4ff; text-align: center;
        animation: glowPulse 3s infinite ease-in-out; letter-spacing: 3px;
    }

    /* تحريك الكروت عند التفاعل */
    .exercise-card {
        background: rgba(0, 212, 255, 0.05); border-left: 5px solid #00d4ff;
        padding: 15px; margin: 15px 0; border-radius: 4px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .exercise-card:hover { 
        background: rgba(0, 212, 255, 0.15); 
        transform: scale(1.02) translateX(10px);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
    }

    /* تدمير الرمادي المطلق في كل المدخلات */
    input, div[data-baseweb="input"], .stSelectbox div, .stMultiSelect div {
        background-color: #000 !important; color: #00d4ff !important;
        border: 1px solid #00d4ff44 !important;
    }
    .stMultiSelect span { background-color: #00d4ff15 !important; border: 1px solid #00d4ff33; }
    
    [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }
    label { color: #666 !important; font-size: 11px !important; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# 2. اللغات والأنظمة
if 'step' not in st.session_state: st.session_state.step = 'awakening'

# 3. قاعدة بيانات الإصابات "التفصيلية" (Deep Anatomy Scan)
# كل تمرين مربوط بإصابته المحددة بدقة
DB = {
    "PPL (Push/Pull/Legs)": {
        "PUSH": [
            {"name": "Bench Press", "sets": 4, "reps": "8-10", "inj": "Front Shoulder"},
            {"name": "Incline DB Press", "sets": 3, "reps": "12", "inj": "Front Shoulder"},
            {"name": "Military Press", "sets": 3, "reps": "10", "inj": "Side Shoulder"},
            {"name": "Skullcrushers", "sets": 3, "reps": "12", "inj": "Elbow Joint"},
            {"name": "Tricep Pushdown", "sets": 3, "reps": "15", "inj": "Elbow Joint"}
        ],
        "PULL": [
            {"name": "Deadlift", "sets": 3, "reps": "5", "inj": "Lower Back"},
            {"name": "Barbell Rows", "sets": 4, "reps": "8-10", "inj": "Lower Back"},
            {"name": "Lat Pulldown", "sets": 4, "reps": "12", "inj": "Latissimus (Lats)"},
            {"name": "Face Pulls", "sets": 3, "reps": "15", "inj": "Rear Shoulder"},
            {"name": "Barbell Curls", "sets": 3, "reps": "12", "inj": "Wrist/Forearm"}
        ],
        "LEGS": [
            {"name": "Back Squat", "sets": 4, "reps": "8", "inj": "Knee Joint"},
            {"name": "RDL", "sets": 3, "reps": "12", "inj": "Lower Back"},
            {"name": "Leg Extension", "sets": 3, "reps": "15", "inj": "Knee Joint"},
            {"name": "Calf Raise", "sets": 4, "reps": "20", "inj": "Ankle/Achilles"}
        ]
    },
    "Bro Split (Legacy)": {"CHEST": [{"name": "Chest Flys", "sets": 4, "reps": "15", "inj": "Front Shoulder"}]},
    "Upper/Lower (Power)": {"UPPER": [{"name": "Pullups", "sets": 3, "reps": "Max", "inj": "Shoulder Blade"}]}
}

# --- Phase 1: Awakening (Data Input) ---
if st.session_state.step == 'awakening':
    st.markdown('<div class="system-title"><h1>SYSTEM NOTIFICATION</h1></div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#ff00ff; animation: glowPulse 2s infinite;">[WARNING: YOU HAVE BECOME A PLAYER]</p>', unsafe_allow_html=True)
    
    u_id = st.text_input("PLAYER NAME", placeholder="ADAM...")
    c1, c2 = st.columns(2)
    u_gen = c1.selectbox("GENDER", ["MALE (Hunter)", "FEMALE (Huntress)"])
    u_path = c2.selectbox("TRAINING PATH", list(DB.keys())) # تنوع الأنظمة
    
    # تفصيل الإصابات لكل الجسم كما طلبت
    u_inj = st.multiselect("DETAILED INJURY SCAN", [
        "Front Shoulder", "Side Shoulder", "Rear Shoulder", "Shoulder Blade",
        "Lower Back", "Upper Back", "Latissimus (Lats)",
        "Elbow Joint", "Wrist/Forearm", "Knee Joint", "Ankle/Achilles"
    ])
    
    cw, ch = st.columns(2)
    u_w = cw.text_input("WEIGHT (KG)", "80")
    u_h = ch.text_input("HEIGHT (CM)", "175")

    if st.button("ARISE"):
        if u_id:
            st.session_state.player = {"name": u_id, "gen": u_gen, "path": u_path, "inj": u_inj}
            st.session_state.step = 'mission'
            st.rerun()

# --- Phase 2: Mission HUD (Dynamic Action) ---
elif st.session_state.step == 'mission':
    p = st.session_state.player
    st.markdown(f"### ⚡ PLAYER: {p['name'].upper()} | ROLE: {p['gen']}")
    
    day = st.selectbox("SELECT MISSION SESSION", list(DB[p['path']].keys()))
    st.write("---")
    
    for ex in DB[p['path']][day]:
        # تفاعل ذكي مع الإصابة المحددة
        if ex['inj'] in p['inj']:
            st.markdown(f"""<div class='exercise-card' style='border-color:#ff0055; opacity:0.5;'>
            <span style='color:#ff0055; font-weight:bold;'>❌ RESTRICTED: {ex['inj']} INJURY DETECTED</span><br>
            <b style='text-decoration: line-through;'>{ex['name']}</b></div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="exercise-card">
            <span style="font-weight:bold; letter-spacing:1px;">⚔️ {ex['name']}</span><br>
            <span style="color:#ff00ff; font-family:'Orbitron'; font-size:12px;">{ex['sets']} SETS x {ex['reps']} REPS</span>
            </div>""", unsafe_allow_html=True)
            st.checkbox(f"Mission Task Clear", key=ex['name'])

    if st.sidebar.button("RESET SYSTEM"):
        st.session_state.step = 'awakening'
        st.rerun()
