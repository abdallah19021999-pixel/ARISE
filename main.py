import streamlit as st

# 1. تثبيت الهوية البصرية (Void Aesthetic - No White)
st.set_page_config(page_title="SYSTEM", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    
    /* الخانات الزجاجية */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="base-input"], div[data-testid="stMultiSelect"] {
        background-color: rgba(0, 20, 40, 0.4) !important;
        border: 1px solid rgba(0, 212, 255, 0.1) !important;
        color: #00d4ff !important;
    }
    input { color: #00d4ff !important; background: transparent !important; }
    
    /* إخفاء أزرار الزائد والناقص نهائياً */
    button[step="1"], button[step="-1"], [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] {
        display: none !important;
    }

    .system-notification {
        background: rgba(0, 30, 60, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 212, 255, 0.15);
        padding: 20px;
        text-align: center;
        border-radius: 4px;
        margin-bottom: 30px;
    }

    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 8px;
        padding: 18px !important; margin-top: 20px;
    }
    .stButton > button:hover { background: rgba(0, 212, 255, 0.1) !important; box-shadow: 0 0 40px #00d4ff; }

    header, footer {visibility: hidden !important;}
    label { color: #333 !important; font-family: 'Orbitron'; font-size: 10px !important; letter-spacing: 2px; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state:
    st.session_state.step = 'awakening'

# --- المرحلة الأولى: Awakening (تخصيص البروتوكول) ---
if st.session_state.step == 'awakening':
    st.markdown("""
        <div class="system-notification">
            <h2 style="font-family:Orbitron; letter-spacing:4px; margin:0;">SYSTEM INITIALIZATION</h2>
            <div style="width: 100px; height: 1px; background: #00d4ff; margin: 15px auto; opacity: 0.3;"></div>
            <p style="font-family:Cairo; color:#00d4ff;">اختر نظام التدريب المناسب لرتبتك</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        u_name = st.text_input("PLAYER IDENTIFICATION", placeholder="ENTER NAME...")
        
        col1, col2, col3 = st.columns(3)
        u_age = col1.number_input("AGE", step=1, value=25)
        u_weight = col2.number_input("WEIGHT (KG)", step=1, value=80)
        u_height = col3.number_input("HEIGHT (CM)", step=1, value=175)
        
        u_gender = st.selectbox("PLAYER GENDER", ["MALE", "FEMALE"])
        u_injury = st.multiselect("INJURY SCAN", ["NONE", "SHOULDER", "LOWER BACK", "KNEE", "WRIST"], default=["NONE"])
        
        # اختيار نظام التمرين
        u_split = st.selectbox("TRAINING PROTOCOL (SPLIT)", ["BODY PARTS (BRO SPLIT)", "PUSH PULL LEGS (PPL)", "UPPER LOWER", "FULL BODY"])
        u_goal = st.selectbox("PRIMARY OBJECTIVE", ["HYPERTROPHY (BULK)", "DEFINITION (CUT)"])
        
        if st.button("ARISE"):
            if u_name:
                bmi = round(u_weight / ((u_height/100)**2), 1)
                rank = "S-RANK" if 22 <= bmi <= 25 else "A-RANK" if bmi < 30 else "B-RANK"
                st.session_state.player = {
                    "name": u_name, "bmi": bmi, "goal": u_goal, 
                    "injury": u_injury, "gender": u_gender, "rank": rank, "split": u_split
                }
                st.session_state.step = 'dashboard'
                st.rerun()

# --- المرحلة الثانية: Status Window & Adaptive Quests ---
elif st.session_state.step == 'dashboard':
    p = st.session_state.player
    st.markdown(f"""
        <div style='text-align:center; margin-bottom:40px;'>
            <p style='font-family:Orbitron; color:#00d4ff; font-size:10px; letter-spacing:12px;'>STATUS WINDOW</p>
            <h1 style='font-family:Orbitron; font-size:45px; margin:0;'>{p['name'].upper()}</h1>
            <p style='color:#555; font-family:Orbitron;'>RANK: {p['rank']} | {p['split']}</p>
        </div>
    """, unsafe_allow_html=True)

    # تحديد خيارات العضلات بناءً على النظام المختار
    split_options = {
        "BODY PARTS (BRO SPLIT)": ["CHEST", "BACK", "LEGS", "SHOULDERS", "ARMS"],
        "PUSH PULL LEGS (PPL)": ["PUSH (Chest/Shoulder/Tri)", "PULL (Back/RearDelt/Bi)", "LEGS (Quads/Ham/Calves)"],
        "UPPER LOWER": ["UPPER BODY", "LOWER BODY"],
        "FULL BODY": ["FULL BODY SESSION"]
    }
    
    target = st.selectbox("SELECT ACTIVE ZONE", split_options[p['split']])

    # محرك التمارين الشامل (The Universal Engine)
    def get_universal_workout(target_zone, injuries, goal):
        db = {
            "CHEST": ["Bench Press", "Incline DB Press", "Dips", "Cable Flys"],
            "PUSH (Chest/Shoulder/Tri)": ["Flat Bench Press", "Overhead Press", "Incline Flys", "Tricep Pushdowns", "Lateral Raises"],
            "PULL (Back/RearDelt/Bi)": ["Deadlifts", "Pull-ups", "Barbell Rows", "Face Pulls", "Bicep Curls"],
            "LEGS (Quads/Ham/Calves)": ["Squats", "Leg Press", "Leg Curls", "Calf Raises"],
            "UPPER BODY": ["Bench Press", "Rows", "Shoulder Press", "Pull-ups", "Arm Isolation"],
            "LOWER BODY": ["Deadlifts", "Leg Extensions", "Hamstring Curls", "Calf Raises"],
            "FULL BODY SESSION": ["Squats", "Bench Press", "Rows", "Overhead Press", "Plank"],
            "BACK": ["Pull-ups", "Deadlifts", "Rows", "Lat Pulldowns"],
            "ARMS": ["Barbell Curls", "Skull Crushers", "Hammer Curls", "Dips"],
            "SHOULDERS": ["Military Press", "Lateral Raises", "Rear Delt Flys", "Front Raises"]
        }
        
        workout = db.get(target_zone, ["Rest Day Protocol"]).copy()
        
        # تعديلات الهدف (Rep Ranges)
        rep_scheme = " (6-8 Reps)" if goal == "HYPERTROPHY (BULK)" else " (12-15 Reps)"
        workout = [ex + rep_scheme for ex in workout]

        # فلتر الإصابات الذكي
        if "SHOULDER" in injuries:
            workout = ["Neutral Grip (Safe)" if "Press" in ex or "Dips" in ex else ex for ex in workout]
        if "LOWER BACK" in injuries:
            workout = ["Supported Movement" if "Deadlift" in ex or "Rows" in ex else ex for ex in workout]
        if "KNEE" in injuries:
            workout = ["Limited Range (Box)" if "Squat" in ex else ex for ex in workout]
            
        return workout

    current_workout = get_universal_workout(target, p['injury'], p['goal'])

    st.markdown("<p style='font-family:Orbitron; color:#00d4ff; font-size:12px; letter-spacing:4px;'>DAILY QUESTS</p>", unsafe_allow_html=True)
    with st.expander(f"⚔️ {target} PROTOCOL", expanded=True):
        if "NONE" not in p['injury'] and len(p['injury']) > 0:
            st.warning("SYSTEM: Injury Mitigation Active.")
        for ex in current_workout:
            st.checkbox(ex)

    if st.button("TERMINATE SESSION"):
        st.session_state.step = 'awakening'
        st.rerun()
