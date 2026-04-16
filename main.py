import streamlit as st

# 1. تثبيت الهوية البصرية (Black & Cyan - No White)
st.set_page_config(page_title="SYSTEM", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    
    /* الخانات الرقمية والنصية بدون أبيض وبدون أزرار زائد/ناقص */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, input {
        background-color: rgba(0, 20, 40, 0.4) !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        color: #00d4ff !important;
    }
    button[step="1"], button[step="-1"] { display: none !important; }

    /* تنسيق الكروت الزجاجية */
    .glass-card {
        background: rgba(0, 30, 60, 0.1);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 212, 255, 0.1);
        padding: 20px;
        text-align: center;
        border-radius: 8px;
        margin-bottom: 25px;
    }

    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 5px;
        padding: 15px !important; margin-top: 20px;
    }
    
    header, footer {visibility: hidden !important;}
    label { color: #555 !important; font-family: 'Orbitron'; font-size: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state:
    st.session_state.step = 'awakening'

# --- المرحلة الأولى: Awakening & Injury Report ---
if st.session_state.step == 'awakening':
    st.markdown('<div class="glass-card"><h2 style="font-family:Orbitron;">BIO-METRIC SCAN</h2><p style="font-family:Cairo; color:#444;">أدخل بياناتك وذكر أي إصابات حالية</p></div>', unsafe_allow_html=True)
    
    with st.container():
        u_name = st.text_input("IDENTIFICATION", placeholder="CODE NAME...")
        
        col1, col2, col3 = st.columns(3)
        u_age = col1.number_input("AGE", step=1, value=25)
        u_weight = col2.number_input("WEIGHT (KG)", step=1, value=80)
        u_height = col3.number_input("HEIGHT (CM)", step=1, value=175)
        
        # إضافة نظام الإصابات
        u_injury = st.multiselect("REPORT INJURIES (Optional)", ["NONE", "SHOULDER", "LOWER BACK", "KNEE", "WRIST"])
        u_goal = st.selectbox("OBJECTIVE", ["HYPERTROPHY (BULK)", "DEFINITION (CUT)"])
        
        bmi = round(u_weight / ((u_height/100)**2), 1)
        
        if st.button("ARISE"):
            if u_name:
                st.session_state.player = {
                    "name": u_name, "bmi": bmi, "goal": u_goal, "injury": u_injury
                }
                st.session_state.step = 'dashboard'
                st.rerun()

# --- المرحلة الثانية: Adaptive Workout System ---
elif st.session_state.step == 'dashboard':
    p = st.session_state.player
    st.markdown(f"<div style='text-align:center;'><h1 style='font-family:Orbitron;'>PLAYER: {p['name'].upper()}</h1><p style='color:#333;'>BMI: {p['bmi']} | INJURIES: {', '.join(p['injury'])}</p></div>", unsafe_allow_html=True)

    muscle = st.selectbox("SELECT TARGET", ["CHEST", "BACK", "LEGS", "SHOULDERS"])

    # بنك التمارين الذكي (يستجيب للإصابة)
    def get_safe_workout(muscle_group, injuries):
        base_workouts = {
            "CHEST": ["Bench Press", "Incline DB Press", "Dips", "Cable Flys"],
            "BACK": ["Deadlifts", "Pull-ups", "Seated Rows", "Lat Pulldowns"],
            "LEGS": ["Squats", "Leg Press", "Leg Extensions", "Lying Leg Curls"],
            "SHOULDERS": ["Military Press", "Lateral Raises", "Rear Delt Flys"]
        }
        
        workout = base_workouts[muscle_group].copy()
        
        # فلتر الإصابات
        if "SHOULDER" in injuries and muscle_group == "CHEST":
            workout[0] = "Floor Press (Limited ROM)" # بديل آمن للـ Bench Press
            workout[2] = "Push-ups (Neutral Grip)" # بديل للـ Dips
        if "LOWER BACK" in injuries and muscle_group == "BACK":
            workout[0] = "Chest-Supported Rows" # بديل للـ Deadlift
        if "KNEE" in injuries and muscle_group == "LEGS":
            workout[0] = "Box Squats (High)"
            workout[1] = "Glute Bridges"
            
        return workout

    current_workout = get_safe_workout(muscle, p['injury'])

    st.markdown("<p style='font-family:Orbitron; font-size:12px;'>ADAPTIVE QUEST PROTOCOL</p>", unsafe_allow_html=True)
    with st.expander(f"⚔️ {muscle} SESSION", expanded=True):
        if "NONE" not in p['injury'] and len(p['injury']) > 0:
            st.warning("⚠️ SYSTEM: Adaptive Exercises Enabled for your protection.")
        
        for ex in current_workout:
            st.checkbox(ex)

    if st.button("TERMINATE"):
        st.session_state.step = 'awakening'
        st.rerun()
