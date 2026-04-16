import streamlit as st
import time

# 1. نظام الهوية البصرية السيادية (Sovereign HUD Design)
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
    .exercise-card:hover { transform: scale(1.01) translateX(10px); background: rgba(0, 212, 255, 0.15); }
    .alt-card {
        background: rgba(255, 0, 255, 0.07); backdrop-filter: blur(10px); 
        border: 1px solid rgba(255, 0, 255, 0.3); border-left: 5px solid #ff00ff;
        padding: 20px; margin: 15px 0; border-radius: 4px;
    }
    input, .stSelectbox div, .stMultiSelect div {
        background-color: rgba(0, 0, 0, 0.8) !important; color: #00d4ff !important; 
        border: 1px solid #00d4ff44 !important;
    }
    label { color: #666 !important; font-size: 11px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة والمخزن (State & Inventory Management)
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

# 3. قاعدة البيانات الإمبراطورية (7 تمارين لكل حصة في الـ 3 أنظمة)
DB = {
    "PPL (Push/Pull/Legs)": {
        "PULL (Back/Biceps)": [
            {"name": "Deadlift", "sets": 3, "reps": "5", "inj": "Lower Back", "alt": "Lat Pulldown"},
            {"name": "Barbell Rows", "sets": 4, "reps": "8", "inj": "Lower Back", "alt": "Chest Supported Rows"},
            {"name": "Lat Pulldown", "sets": 4, "reps": "12", "inj": "Shoulder Blade", "alt": "Seated Rows"},
            {"name": "Face Pulls", "sets": 3, "reps": "15", "inj": "Rear Shoulder", "alt": "Reverse Pec Deck"},
            {"name": "Single Arm Row", "sets": 3, "reps": "12", "inj": "Lower Back", "alt": "Seated Machine Row"},
            {"name": "Barbell Curls", "sets": 3, "reps": "12", "inj": "Wrist/Forearm", "alt": "Hammer Curls"},
            {"name": "Preacher Curls", "sets": 3, "reps": "12", "inj": "Elbow Joint", "alt": "Concentration Curls"}
        ],
        "PUSH (Chest/Shoulder/Triceps)": [
            {"name": "Bench Press", "sets": 4, "reps": "8", "inj": "Front Shoulder", "alt": "Floor Press"},
            {"name": "Overhead Press", "sets": 3, "reps": "10", "inj": "Side Shoulder", "alt": "Landmine Press"},
            {"name": "Incline DB Press", "sets": 3, "reps": "12", "inj": "Front Shoulder", "alt": "Incline Machine Press"},
            {"name": "Lateral Raises", "sets": 4, "reps": "15", "inj": "Side Shoulder", "alt": "Cable Lateral Raise"},
            {"name": "Tricep Pushdown", "sets": 3, "reps": "15", "inj": "Elbow Joint", "alt": "Diamond Pushups"},
            {"name": "Skullcrushers", "sets": 3, "reps": "12", "inj": "Elbow Joint", "alt": "Single Arm Extension"},
            {"name": "Dips", "sets": 3, "reps": "Max", "inj": "Front Shoulder", "alt": "Tricep Machine Dip"}
        ],
        "LEGS (Quads/Hams/Calves)": [
            {"name": "Back Squat", "sets": 4, "reps": "8", "inj": "Knee Joint", "alt": "Leg Press"},
            {"name": "RDL", "sets": 3, "reps": "12", "inj": "Lower Back", "alt": "Leg Curls"},
            {"name": "Leg Extension", "sets": 3, "reps": "15", "inj": "Knee Joint", "alt": "Step Ups"},
            {"name": "Leg Curls", "sets": 3, "reps": "15", "inj": "Knee Joint", "alt": "Glute Bridges"},
            {"name": "Bulgarian Split Squat", "sets": 3, "reps": "10", "inj": "Knee Joint", "alt": "Goblet Squats"},
            {"name": "Calf Raises", "sets": 4, "reps": "20", "inj": "Ankle", "alt": "Seated Calf Raise"},
            {"name": "Plank", "sets": 3, "reps": "60s", "inj": "Lower Back", "alt": "Deadbug"}
        ]
    },
    "Bro Split (Elite)": {
        "CHEST": [
            {"name": "Flat Bench", "sets": 4, "reps": "10", "inj": "Front Shoulder", "alt": "Floor Press"},
            {"name": "Incline Bench", "sets": 3, "reps": "10", "inj": "Front Shoulder", "alt": "Incline Flys"},
            {"name": "Decline Bench", "sets": 3, "reps": "12", "inj": "Front Shoulder", "alt": "Pushups"},
            {"name": "DB Flys", "sets": 3, "reps": "15", "inj": "Front Shoulder", "alt": "Cable Cross"},
            {"name": "Cable Cross", "sets": 3, "reps": "15", "inj": "Front Shoulder", "alt": "Pec Deck"},
            {"name": "Pushups", "sets": 3, "reps": "Max", "inj": "Wrist/Forearm", "alt": "Chest Press Machine"},
            {"name": "Pullover", "sets": 3, "reps": "12", "inj": "Shoulder Blade", "alt": "Machine Flys"}
        ],
        "BACK": [
            {"name": "Deadlift", "sets": 3, "reps": "5", "inj": "Lower Back", "alt": "Lat Pulldown"},
            {"name": "T-Bar Row", "sets": 4, "reps": "10", "inj": "Lower Back", "alt": "Chest Supported Row"},
            {"name": "Lat Pulldown", "sets": 3, "reps": "12", "inj": "Shoulder Blade", "alt": "Seated Row"},
            {"name": "Pullups", "sets": 3, "reps": "Max", "inj": "Shoulder Blade", "alt": "Lat Pulldown"},
            {"name": "Seated Row", "sets": 3, "reps": "12", "inj": "Lower Back", "alt": "Lat Pulldown"},
            {"name": "Straight Arm Pulldown", "sets": 3, "reps": "15", "inj": "Rear Shoulder", "alt": "Face Pulls"},
            {"name": "Back Extensions", "sets": 3, "reps": "15", "inj": "Lower Back", "alt": "Bird Dog"}
        ]
    },
    "Upper/Lower Body": {
        "UPPER": [
            {"name": "Bench Press", "sets": 4, "reps": "8", "inj": "Front Shoulder", "alt": "Floor Press"},
            {"name": "Rows", "sets": 4, "reps": "8", "inj": "Lower Back", "alt": "Chest Supported Rows"},
            {"name": "Military Press", "sets": 3, "reps": "10", "inj": "Side Shoulder", "alt": "Landmine Press"},
            {"name": "Lat Pulldowns", "sets": 3, "reps": "12", "inj": "Shoulder Blade", "alt": "Seated Rows"},
            {"name": "Lateral Raises", "sets": 3, "reps": "15", "inj": "Side Shoulder", "alt": "Face Pulls"},
            {"name": "Curls", "sets": 3, "reps": "12", "inj": "Wrist/Forearm", "alt": "Hammer Curls"},
            {"name": "Extensions", "sets": 3, "reps": "12", "inj": "Elbow Joint", "alt": "Pushdowns"}
        ],
        "LOWER": [
            {"name": "Squats", "sets": 4, "reps": "8", "inj": "Knee Joint", "alt": "Leg Press"},
            {"name": "RDL", "sets": 4, "reps": "10", "inj": "Lower Back", "alt": "Leg Curls"},
            {"name": "Leg Press", "sets": 3, "reps": "12", "inj": "Knee Joint", "alt": "Goblet Squats"},
            {"name": "Leg Extensions", "sets": 3, "reps": "15", "inj": "Knee Joint", "alt": "Lunges"},
            {"name": "Leg Curls", "sets": 3, "reps": "15", "inj": "Knee Joint", "alt": "Glute Bridges"},
            {"name": "Calf Raises", "sets": 4, "reps": "20", "inj": "Ankle", "alt": "Seated Calf Raise"},
            {"name": "Plank", "sets": 3, "reps": "60s", "inj": "Lower Back", "alt": "Deadbug"}
        ]
    }
}

# --- Stage 1: Awakening (Data Collection) ---
if st.session_state.step == 'awakening':
    st.markdown('<div class="system-title"><h1>SYSTEM AWAKENING</h1></div>', unsafe_allow_html=True)
    
    u_id = st.text_input("PLAYER NAME", placeholder="Enter your identity...")
    c1, c2 = st.columns(2)
    u_gen = c1.selectbox("GENDER", ["MALE (Hunter)", "FEMALE (Huntress)"])
    u_path = c2.selectbox("TRAINING PATH", list(DB.keys()))
    
    u_inj = st.multiselect("INJURY SCAN", ["Front Shoulder", "Side Shoulder", "Rear Shoulder", "Lower Back", "Shoulder Blade", "Knee Joint", "Elbow Joint", "Wrist/Forearm", "Ankle"])
    
    col_w, col_h = st.columns(2)
    u_w = col_w.text_input("WEIGHT (KG)", "80")
    u_h = col_h.text_input("HEIGHT (CM)", "175")

    if st.button("ARISE"):
        if u_id:
            st.session_state.player = {"name": u_id, "gen": u_gen, "path": u_path, "inj": u_inj}
            st.session_state.step = 'mission'
            st.rerun()

# --- Stage 2: Mission HUD (Training Environment) ---
elif st.session_state.step == 'mission':
    p = st.session_state.player
    
    # Status HUD
    st.markdown(f"""
        <div style='display:flex; justify-content:space-between; align-items:baseline;'>
            <h2 style='font-family:Orbitron; color:#ff00ff; margin:0;'>LVL. {st.session_state.level}</h2>
            <div style='text-align:right;'><b>PLAYER:</b> {p['name'].upper()}<br><small style='color:#888;'>{p['path']}</small></div>
        </div>
        <div class='xp-bar-container'><div class='xp-bar-fill' style='width:{st.session_state.xp}%;'></div></div>
    """, unsafe_allow_html=True)

    day = st.selectbox("SELECT MISSION", list(DB[p['path']].keys()))
    st.write("---")

    for ex in DB[p['path']][day]:
        injured = ex['inj'] in p['inj']
        ex_name = ex['alt'] if injured else ex['name']
        
        # Display Exercise Card
        st.markdown(f"""<div class="{'alt-card' if injured else 'exercise-card'}">
            <span style="font-weight:bold;">{'🔄 ' if injured else '⚔️ '}{ex_name}</span><br>
            <span style="color:#ff00ff; font-family:'Orbitron'; font-size:12px;">{ex['sets']} SETS x {ex['reps']} REPS</span>
            {f"<br><small style='color:#ff00ff;'>ADAPTED FOR {ex['inj']}</small>" if injured else ""}
        </div>""", unsafe_allow_html=True)

        col_inv, col_timer = st.columns([2, 1])
        
        # 1. Weight Inventory Tracking
        w_key = f"w_{ex_name}"
        prev_w = st.session_state.inventory.get(w_key, "0")
        new_w = col_inv.text_input(f"Record Weight (Prev: {prev_w}kg)", key=f"rec_{ex_name}")
        if new_w != "0" and new_w != prev_w: st.session_state.inventory[w_key] = new_w

        # 2. Advanced Rest Timer
        if col_timer.button(f"⏱️ Start Rest", key=f"btn_{ex_name}"):
            with st.empty():
                for i in range(60, 0, -1):
                    st.write(f"⌛ Remaining: {i}s")
                    time.sleep(1)
                st.write("🔥 MISSION READY!")
                st.balloons()

        # 3. Task Completion (XP)
        if st.checkbox("Checkpoint Cleared (+15 XP)", key=f"chk_{ex_name}"):
            add_xp(15)

    if st.sidebar.button("RESET SYSTEM"):
        st.session_state.step = 'awakening'
        st.rerun()
