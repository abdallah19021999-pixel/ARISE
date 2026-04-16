import streamlit as st
import time

# 1. الواجهة السيادية (Sovereign HUD Design)
st.set_page_config(page_title="SYSTEM HUD", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at center, #001525 0%, #000000 100%) !important;
        background-attachment: fixed; color: #00d4ff !important; font-family: 'Cairo', sans-serif;
    }
    .stApp::before {
        content: " "; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.15) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.02));
        background-size: 100% 4px, 3px 100%; z-index: -1; pointer-events: none;
    }
    .system-title {
        font-family: 'Orbitron'; color: #00d4ff; text-align: center;
        text-shadow: 0 0 20px #00d4ff; background: rgba(0, 212, 255, 0.05); 
        padding: 20px; border: 1px solid rgba(0, 212, 255, 0.1); border-radius: 10px;
        animation: glowPulse 3s infinite ease-in-out; letter-spacing: 4px;
    }
    @keyframes glowPulse {
        0% { text-shadow: 0 0 5px #00d4ff; opacity: 0.8; }
        50% { text-shadow: 0 0 20px #00d4ff, 0 0 30px #00fbff; opacity: 1; }
        100% { text-shadow: 0 0 5px #00d4ff; opacity: 0.8; }
    }
    .xp-bar-container {
        width: 100%; background: rgba(0, 212, 255, 0.05); border: 1px solid #00d4ff44; 
        height: 10px; border-radius: 5px; margin: 15px 0;
    }
    .xp-bar-fill {
        height: 100%; background: linear-gradient(90deg, #00d4ff, #00fbff); 
        box-shadow: 0 0 15px #00d4ff; border-radius: 5px; transition: width 0.8s ease;
    }
    .exercise-card {
        background: rgba(0, 212, 255, 0.07); backdrop-filter: blur(10px); 
        border: 1px solid rgba(0, 212, 255, 0.2); border-left: 5px solid #00d4ff;
        padding: 20px; margin: 15px 0; border-radius: 4px; transition: 0.3s;
    }
    .alt-card {
        background: rgba(255, 0, 255, 0.07); backdrop-filter: blur(10px); 
        border: 1px solid rgba(255, 0, 255, 0.3); border-left: 5px solid #ff00ff;
        padding: 20px; margin: 15px 0; border-radius: 4px;
    }
    /* توحيد شكل المدخلات لتجنب اللون الأبيض */
    input, .stSelectbox div, .stMultiSelect div, [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0.8) !important; color: #00d4ff !important; 
    }
    label { color: #888 !important; font-size: 11px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'level' not in st.session_state: st.session_state.level = 1
if 'inventory' not in st.session_state: st.session_state.inventory = {}
if 'step' not in st.session_state: st.session_state.step = 'awakening'

def add_xp(amount):
    st.session_state.xp += amount
    if st.session_state.xp >= 100:
        st.session_state.level += 1
        st.session_state.xp = 0
        st.balloons()

# 3. قاعدة البيانات الإمبراطورية الكاملة (7 تمارين لكل حصة)
DB = {
    "PPL (Push/Pull/Legs)": {
        "PULL (Back/Biceps)": [
            {"name": "Deadlift", "sets": 3, "reps": "5", "inj": "Lower Back", "alt": "Lat Pulldown"},
            {"name": "Barbell Rows", "sets": 4, "reps": "8", "inj": "Lower Back", "alt": "Chest Supported Rows"},
            {"name": "Pull-ups", "sets": 3, "reps": "Max", "inj": "Shoulder Blade", "alt": "Lat Pulldown (Wide)"},
            {"name": "Seated Cable Rows", "sets": 3, "reps": "12", "inj": "Lower Back", "alt": "One Arm DB Row"},
            {"name": "Face Pulls", "sets": 3, "reps": "15", "inj": "Rear Shoulder", "alt": "Reverse Pec Deck"},
            {"name": "Barbell Curls", "sets": 3, "reps": "12", "inj": "Wrist/Forearm", "alt": "Hammer Curls"},
            {"name": "Hammer Curls", "sets": 3, "reps": "12", "inj": "Wrist/Forearm", "alt": "Concentration Curls"}
        ],
        "PUSH (Chest/Shoulder/Triceps)": [
            {"name": "Bench Press", "sets": 4, "reps": "8", "inj": "Front Shoulder", "alt": "Floor Press"},
            {"name": "Military Press", "sets": 3, "reps": "10", "inj": "Side Shoulder", "alt": "Landmine Press"},
            {"name": "Incline DB Press", "sets": 3, "reps": "12", "inj": "Front Shoulder", "alt": "Incline Machine Press"},
            {"name": "Lateral Raises", "sets": 4, "reps": "15", "inj": "Side Shoulder", "alt": "Cable Lateral Raise"},
            {"name": "Tricep Pushdown", "sets": 3, "reps": "15", "inj": "Elbow Joint", "alt": "Diamond Pushups"},
            {"name": "Chest Flys", "sets": 3, "reps": "15", "inj": "Front Shoulder", "alt": "Cable Cross-over"},
            {"name": "Dips", "sets": 3, "reps": "Max", "inj": "Front Shoulder", "alt": "Tricep Machine Dip"}
        ],
        "LEGS (Lower Body)": [
            {"name": "Back Squat", "sets": 4, "reps": "8", "inj": "Knee Joint", "alt": "Leg Press"},
            {"name": "RDL", "sets": 3, "reps": "12", "inj": "Lower Back", "alt": "Leg Curls"},
            {"name": "Leg Extension", "sets": 3, "reps": "15", "inj": "Knee Joint", "alt": "Step Ups"},
            {"name": "Leg Curls", "sets": 3, "reps": "15", "inj": "Knee Joint", "alt": "Glute Bridges"},
            {"name": "Bulgarian Split Squat", "sets": 3, "reps": "10", "inj": "Knee Joint", "alt": "Goblet Squats"},
            {"name": "Calf Raises", "sets": 4, "reps": "20", "inj": "Ankle", "alt": "Seated Calf Raise"},
            {"name": "Leg Press", "sets": 3, "reps": "12", "inj": "Knee Joint", "alt": "Lunges"}
        ]
    },
    "Bro Split (Classic)": {
        "BACK": [
            {"name": "Deadlift", "sets": 3, "reps": "5", "inj": "Lower Back", "alt": "Lat Pulldown"},
            {"name": "T-Bar Row", "sets": 4, "reps": "10", "inj": "Lower Back", "alt": "Chest Supported Row"},
            {"name": "Lat Pulldown", "sets": 4, "reps": "12", "inj": "Shoulder Blade", "alt": "Seated Row"},
            {"name": "One Arm DB Row", "sets": 3, "reps": "12", "inj": "Lower Back", "alt": "Machine Row"},
            {"name": "Seated Row", "sets": 3, "reps": "12", "inj": "Lower Back", "alt": "Lat Pulldown"},
            {"name": "Straight Arm Pulldown", "sets": 3, "reps": "15", "inj": "Rear Shoulder", "alt": "Face Pulls"},
            {"name": "Hyper Extensions", "sets": 3, "reps": "15", "inj": "Lower Back", "alt": "Plank"}
        ],
        "CHEST": [
            {"name": "Flat Bench Press", "sets": 4, "reps": "10", "inj": "Front Shoulder", "alt": "Floor Press"},
            {"name": "Incline DB Press", "sets": 4, "reps": "10", "inj": "Front Shoulder", "alt": "Incline Flys"},
            {"name": "Cable Cross", "sets": 3, "reps": "15", "inj": "Front Shoulder", "alt": "Pec Deck"},
            {"name": "Chest Press Machine", "sets": 3, "reps": "12", "inj": "Front Shoulder", "alt": "Pushups"},
            {"name": "Dips (Chest)", "sets": 3, "reps": "Max", "inj": "Front Shoulder", "alt": "Tricep Machine"},
            {"name": "DB Flys", "sets": 3, "reps": "15", "inj": "Front Shoulder", "alt": "Cable Cross High"},
            {"name": "Pushups", "sets": 3, "reps": "Max", "inj": "Wrist/Forearm", "alt": "Machine Flys"}
        ]
    }
}

# --- Stage 1: System Notification ---
if st.session_state.step == 'awakening':
    st.markdown('<div class="system-title"><h1>SYSTEM NOTIFICATION</h1></div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#ff00ff; font-weight:bold;">[WARNING: YOU HAVE BECOME A PLAYER]</p>', unsafe_allow_html=True)
    
    u_id = st.text_input("PLAYER NAME", placeholder="Enter identity...", key="p_name")
    u_path = st.selectbox("TRAINING PATH", list(DB.keys()), key="p_path")
    u_inj = st.multiselect("INJURY SCAN", ["Front Shoulder", "Side Shoulder", "Rear Shoulder", "Lower Back", "Shoulder Blade", "Knee Joint", "Elbow Joint", "Wrist/Forearm", "Ankle"], key="p_inj")
    
    if st.button("ARISE", key="arise_btn"):
        if u_id:
            st.session_state.player = {"name": u_id, "path": u_path, "inj": u_inj}
            st.session_state.step = 'mission'
            st.rerun()

# --- Stage 2: Mission HUD ---
elif st.session_state.step == 'mission':
    p = st.session_state.player
    st.markdown(f"<h2 style='color:#ff00ff; font-family:Orbitron;'>LVL. {st.session_state.level} | {p['name'].upper()}</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='xp-bar-container'><div class='xp-bar-fill' style='width:{st.session_state.xp}%;'></div></div>", unsafe_allow_html=True)

    day = st.selectbox("SELECT MISSION SESSION", list(DB[p['path']].keys()), key="m_day")
    st.write("---")

    for idx, ex in enumerate(DB[p['path']][day]):
        is_injured = ex['inj'] in p['inj']
        display_name = ex['alt'] if is_injured else ex['name']
        card_style = "alt-card" if is_injured else "exercise-card"
        
        # تصحيح قفلة الـ HTML لضمان نظافة الكارت
        st.markdown(f"""
            <div class="{card_style}">
                <span style="font-weight:bold; font-size:18px;">{'🔄 ' if is_injured else '⚔️ '}{display_name}</span><br>
                <span style="color:#ff00ff; font-family:'Orbitron'; font-size:12px;">{ex['sets']} SETS x {ex['reps']} REPS</span>
                {f"<br><small style='color:#ff00ff;'>ADAPTED FOR {ex['inj']}</small>" if is_injured else ""}
            </div>
        """, unsafe_allow_html=True)

        c_inv, c_tmr = st.columns([2, 1])
        
        # تتبع الوزن
        w_key = f"w_{p['path']}_{day}_{display_name}"
        prev = st.session_state.inventory.get(w_key, "0")
        new_v = c_inv.text_input(f"Weight (Prev: {prev}kg)", key=f"inp_{idx}")
        if new_v != "0" and new_v != prev: st.session_state.inventory[w_key] = new_v

        # التايمر
        if c_tmr.button(f"⏱️ Rest", key=f"t_{idx}"):
            with st.empty():
                for i in range(60, 0, -1):
                    st.write(f"⌛ {i}s")
                    time.sleep(1)
                st.write("🔥 GO!")

        if st.checkbox("Cleared (+15 XP)", key=f"chk_{idx}"):
            add_xp(15)

    if st.sidebar.button("RESET"):
        st.session_state.step = 'awakening'
        st.rerun()
