import streamlit as st

# 1. تثبيت الهوية البصرية (The Monarch Void - Zero White)
st.set_page_config(page_title="SYSTEM", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    
    /* الخانات الزجاجية بدون أبيض وبدون أزرار زائد/ناقص */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {
        background-color: rgba(0, 20, 40, 0.4) !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        color: #00d4ff !important;
    }
    input { color: #00d4ff !important; background: transparent !important; }
    
    /* إخفاء أزرار الزائد والناقص نهائياً */
    button[step="1"], button[step="-1"], [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] {
        display: none !important;
    }

    .system-card {
        background: rgba(0, 30, 60, 0.15);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 212, 255, 0.1);
        padding: 25px;
        text-align: center;
        border-radius: 2px;
        margin-bottom: 30px;
    }

    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 7px;
        padding: 15px !important; margin-top: 20px; text-transform: uppercase;
    }
    .stButton > button:hover { background: rgba(0, 212, 255, 0.1) !important; box-shadow: 0 0 30px #00d4ff; }

    /* تنسيق التمارين (The Quests) */
    .st-emotion-cache-p4mowd { background-color: #050505 !important; border: 1px solid rgba(0, 212, 255, 0.1) !important; }

    header, footer {visibility: hidden !important;}
    label { color: #444 !important; font-family: 'Orbitron'; font-size: 10px !important; letter-spacing: 2px; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة (System State)
if 'step' not in st.session_state:
    st.session_state.step = 'awakening'

# --- المرحلة الأولى: Awakening (بوابة الدخول للنظام) ---
if st.session_state.step == 'awakening':
    st.markdown("""
        <div class="system-card">
            <h2 style="font-family:Orbitron; letter-spacing:5px; margin:0;">SYSTEM NOTIFICATION</h2>
            <div style="width: 50px; height: 1px; background: #00d4ff; margin: 15px auto; opacity: 0.5;"></div>
            <p style="font-family:Cairo; color:#666; font-size:14px;">[تحذير: أنت على وشك الدخول إلى نظام الصحوة]</p>
            <p style="font-family:Cairo; color:#00d4ff; font-size:16px;">أدخل بياناتك لتحديد رتبتك كلاعب</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        u_name = st.text_input("PLAYER IDENTIFICATION", placeholder="ENTER NAME...")
        
        col1, col2, col3 = st.columns(3)
        u_age = col1.number_input("AGE", step=1, value=25)
        u_weight = col2.number_input("WEIGHT (KG)", step=1, value=80)
        u_height = col3.number_input("HEIGHT (CM)", step=1, value=175)
        
        u_injury = st.multiselect("INJURY SCAN (IF ANY)", ["NONE", "SHOULDER", "LOWER BACK", "KNEE", "WRIST"], default=["NONE"])
        u_goal = st.selectbox("PLAYER OBJECTIVE", ["HYPERTROPHY (BULK)", "DEFINITION (CUT)"])
        
        if st.button("ARISE"):
            if u_name:
                bmi = round(u_weight / ((u_height/100)**2), 1)
                st.session_state.player = {
                    "name": u_name, "bmi": bmi, "goal": u_goal, "injury": u_injury
                }
                st.session_state.step = 'dashboard'
                st.rerun()

# --- المرحلة الثانية: Status Window (نافذة الحالة) ---
elif st.session_state.step == 'dashboard':
    p = st.session_state.player
    st.markdown(f"""
        <div style='text-align:center; margin-bottom:40px;'>
            <p style='font-family:Orbitron; color:#00d4ff; font-size:10px; letter-spacing:10px;'>STATUS WINDOW</p>
            <h1 style='font-family:Orbitron; font-size:45px; margin:0;'>{p['name'].upper()}</h1>
            <div style="width: 100px; height: 1px; background: #00d4ff; margin: 10px auto; opacity: 0.3;"></div>
            <p style='color:#333; font-family:Orbitron; font-size:12px;'>BMI: {p['bmi']} | OBJECTIVE: {p['goal']}</p>
        </div>
    """, unsafe_allow_html=True)

    muscle = st.selectbox("SELECT DAILY QUEST (TARGET)", ["CHEST", "BACK", "LEGS", "SHOULDERS", "ARMS"])

    # نظام التمارين الذكي (يستجيب للإصابة)
    def get_elite_workout(muscle_group, injuries):
        db = {
            "CHEST": ["Bench Press (4x10)", "Incline DB Press (3x12)", "Dips (3xMax)", "Cable Flys (3x15)"],
            "BACK": ["Deadlifts (4x6)", "Weighted Pull-ups (4xMax)", "Seated Rows (3x12)", "Lat Pulldowns (3x10)"],
            "LEGS": ["Squats (4x8)", "Leg Press (3x12)", "Leg Extensions (4x15)", "Hamstring Curls (3x12)"],
            "SHOULDERS": ["Military Press (4x10)", "Lateral Raises (4x15)", "Rear Delt Flys (3x12)"],
            "ARMS": ["Barbell Curls (4x10)", "Skull Crushers (4x12)", "Hammer Curls (3x12)", "Tricep Pushdowns (3x15)"]
        }
        workout = db[muscle_group].copy()
        
        if "SHOULDER" in injuries:
            if muscle_group == "CHEST": workout[0] = "Floor Press (Safe ROM)"; workout[2] = "Neutral Grip Pushups"
        if "LOWER BACK" in injuries:
            if muscle_group == "BACK": workout[0] = "Chest-Supported Rows"
        if "KNEE" in injuries and muscle_group == "LEGS":
            workout[0] = "Box Squats (High)"; workout[1] = "Glute Bridges"
            
        return workout

    current_workout = get_elite_workout(muscle, p['injury'])

    st.markdown("<p style='font-family:Orbitron; color:#00d4ff; font-size:12px; letter-spacing:3px;'>ACTIVE QUESTS</p>", unsafe_allow_html=True)
    with st.expander(f"⚔️ {muscle} PROTOCOL", expanded=True):
        for ex in current_workout:
            st.checkbox(ex)

    if st.button("LOGOUT"):
        st.session_state.step = 'awakening'
        st.rerun()
