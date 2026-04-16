import streamlit as st
from datetime import datetime

# 1. تثبيت الواجهة المظلمة (The Absolute HUD)
st.set_page_config(page_title="SYSTEM HUD", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    header, footer, [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }
    
    .system-window {
        background: rgba(0, 20, 40, 0.5); border: 2px solid #00d4ff;
        padding: 20px; border-radius: 5px; margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.1);
    }
    
    .injury-alert { color: #ff4b4b; font-size: 12px; font-weight: bold; }
    .safe-alt { color: #00ffaa; font-size: 11px; }

    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background: #050505 !important; border: 1px solid #00d4ff33 !important; color: #00d4ff !important;
    }
    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 2px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 5px; padding: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الذاكرة والأنظمة
if 'history' not in st.session_state: st.session_state.history = []
if 'level' not in st.session_state: st.session_state.level = 1
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'step' not in st.session_state: st.session_state.step = 'awakening'

# 3. قاعدة بيانات المدرب (The Trainer's Secret Archive)
TRAINER_DB = {
    "PPL": {
        "Push (دفع)": [
            {"n": "Barbell Bench Press", "i": "Shoulder", "alt": "Floor Press (Safe for Shoulders)"},
            {"n": "Incline Dumbbell Press", "i": "Shoulder", "alt": "Low Incline Hex Press"},
            {"n": "Military Press", "i": "Shoulder", "alt": "Landmine Press (Safe for Shoulders)"},
            {"n": "Dips (Chest Focus)", "i": "Shoulder", "alt": "Pushups with Handles"},
            {"n": "Cable Flys", "i": "Shoulder", "alt": "Pec Deck Machine"},
            {"n": "Lateral Raises", "i": "Shoulder", "alt": "Cable Lateral (Constant Tension)"},
            {"n": "Tricep Pushdowns", "i": "Elbow", "alt": "Diamond Pushups"}
        ],
        "Pull (سحب)": [
            {"n": "Pullups (Wide)", "i": "Shoulder", "alt": "Lat Pulldown (Neutral Grip)"},
            {"n": "Deadlifts", "i": "Back", "alt": "Rack Pulls (Less Back Stress)"},
            {"n": "Barbell Rows", "i": "Back", "alt": "Chest Supported Rows"},
            {"n": "Seated Cable Rows", "i": "Back", "alt": "Single Arm DB Row"},
            {"n": "Face Pulls", "i": "Shoulder", "alt": "Band Pull-aparts"},
            {"n": "Hammer Curls", "i": "Elbow", "alt": "Concentration Curls"},
            {"n": "Barbell Bicep Curls", "i": "Elbow", "alt": "Preacher Curls"}
        ],
        "Legs (أرجل)": [
            {"n": "Back Squats", "i": "Knee", "alt": "Box Squats (Knee Safe)"},
            {"n": "Leg Press", "i": "Knee", "alt": "Goblet Squats"},
            {"n": "Walking Lunges", "i": "Knee", "alt": "Bulgarian Split Squat"},
            {"n": "Leg Extensions", "i": "Knee", "alt": "Sissy Squats (Bodyweight)"},
            {"n": "Hamstring Curls", "i": "Knee", "alt": "Stiff Leg Deadlift"},
            {"n": "Standing Calf Raises", "i": "Ankle", "alt": "Seated Calf Raises"}
        ]
    }
}

# --- المرحلة الأولى: Awakening HUD ---
if st.session_state.step == 'awakening':
    st.markdown('<div class="system-window" style="text-align:center;"><h2>SYSTEM INITIALIZATION</h2></div>', unsafe_allow_html=True)
    
    u_id = st.text_input("PLAYER ID", placeholder="ADAM...")
    col_g, col_p = st.columns(2)
    u_gen = col_g.selectbox("GENDER", ["MALE (Hunter)", "FEMALE (Huntress)"])
    u_path = col_p.selectbox("PATH", ["PPL"])
    
    u_inj = st.multiselect("INJURY SCAN (القيود)", ["Shoulder", "Back", "Knee", "Elbow", "Ankle"])
    
    cw, ch = st.columns(2)
    u_w = cw.number_input("WEIGHT", value=80)
    u_h = ch.number_input("HEIGHT", value=175)

    if st.button("ARISE"):
        if u_id:
            bmi = round(u_w / ((u_h/100)**2), 1)
            rank = "S-RANK" if 20 <= bmi <= 25 else "A-RANK"
            st.session_state.player = {"id": u_id, "gender": u_gen, "path": u_path, "inj": u_inj, "rank": rank}
            st.session_state.step = 'status'
            st.rerun()

# --- المرحلة الثانية: THE COMBAT HUD ---
elif st.session_state.step == 'status':
    p = st.session_state.player
    st.markdown(f"**PLAYER:** {p['id'].upper()} | **{p['rank']}** | **LVL:** {st.session_state.level}")
    
    tab1, tab2 = st.tabs(["DAILY QUEST", "PLAYER LOG"])

    with tab1:
        zones = list(TRAINER_DB[p['path']].keys())
        target = st.selectbox("ZONE PROTOCOL", zones)
        
        st.markdown(f"<div class='system-window'><b>MISSION: {target.upper()}</b></div>", unsafe_allow_html=True)
        
        exs = TRAINER_DB[p['path']][target]
        total_active = 0
        checks = 0
        
        for i, ex in enumerate(exs):
            # نظام المدرب الذكي للتعامل مع الإصابات
            if ex['i'] in p['inj']:
                st.markdown(f"<span class='injury-alert'>⚠️ SKIP: {ex['n']}</span> <br> <span class='safe-alt'>[مدربك يقترح البديل الآمن: {ex['alt']}]</span>", unsafe_allow_html=True)
                if st.checkbox(f"⚔️ {ex['alt']} (Safe Alternative)", key=f"alt_{i}"): checks += 1
                total_active += 1
            else:
                if st.checkbox(f"⚔️ {ex['n']}", key=f"q_{i}"): checks += 1
                total_active += 1
        
        if st.button("COMPLETE MISSION"):
            if checks == total_active:
                st.session_state.history.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "task": target})
                st.session_state.xp += 34
                if st.session_state.xp >= 100:
                    st.session_state.level += 1
                    st.session_state.xp = 0
                st.rerun()
            else:
                st.error("المهمة لم تكتمل! المدرب يراقبك.. أنهِ جميع التمارين.")

    with tab2:
        st.markdown("### 📜 PREVIOUS RECORDS")
        for log in reversed(st.session_state.history):
            st.markdown(f"<p style='font-size:12px; border-bottom:1px solid #111;'>[{log['time']}] {log['task']} - COMPLETED</p>", unsafe_allow_html=True)

    if st.sidebar.button("TERMINATE"):
        st.session_state.step = 'awakening'
        st.rerun()
