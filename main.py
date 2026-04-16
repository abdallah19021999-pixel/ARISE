import streamlit as st
import time

# 1. الواجهة السيادية الأصلية (The Sovereign HUD)
st.set_page_config(page_title="SYSTEM HUD", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at center, #001525 0%, #000000 100%) !important;
        background-attachment: fixed;
        color: #00d4ff !important;
        font-family: 'Cairo', sans-serif;
    }

    .stApp::before {
        content: " "; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.15) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.02));
        background-size: 100% 4px, 3px 100%; z-index: -1; pointer-events: none;
    }

    @keyframes glowPulse {
        0% { text-shadow: 0 0 5px #00d4ff; opacity: 0.8; }
        50% { text-shadow: 0 0 20px #00d4ff, 0 0 30px #00fbff; opacity: 1; }
        100% { text-shadow: 0 0 5px #00d4ff; opacity: 0.8; }
    }

    .system-title {
        font-family: 'Orbitron'; color: #00d4ff; text-align: center;
        animation: glowPulse 3s infinite ease-in-out; letter-spacing: 4px;
        background: rgba(0, 212, 255, 0.05); padding: 20px; border: 1px solid rgba(0, 212, 255, 0.1); border-radius: 10px;
    }

    .xp-bar-container {
        width: 100%; background: rgba(0, 212, 255, 0.05);
        border: 1px solid #00d4ff44; height: 10px; border-radius: 5px; margin: 15px 0;
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

    input, .stNumberInput div, .stSelectbox div, .stMultiSelect div {
        background-color: rgba(0, 0, 0, 0.8) !important; color: #00d4ff !important; border: 1px solid #00d4ff44 !important;
    }
    
    [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }
    label { color: #666 !important; font-size: 11px !important; letter-spacing: 1px; }
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

# 3. الـ 3 مسارات التدريبية كاملة (The 3 Paths)
DB = {
    "PPL (Push/Pull/Legs)": {
        "PUSH": [
            {"name": "Bench Press", "sets": 4, "reps": "8-10", "inj": "Front Shoulder", "alt": "Floor Press"},
            {"name": "Military Press", "sets": 3, "reps": "10", "inj": "Side Shoulder", "alt": "Landmine Press"},
            {"name": "Tricep Pushdown", "sets": 3, "reps": "15", "inj": "Elbow Joint", "alt": "Diamond Pushups"}
        ],
        "PULL": [
            {"name": "Deadlift", "sets": 3, "reps": "5", "inj": "Lower Back", "alt": "Lat Pulldowns"},
            {"name": "Barbell Rows", "sets": 4, "reps": "10", "inj": "Lower Back", "alt": "Chest Supported Rows"}
        ],
        "LEGS": [
            {"name": "Back Squat", "sets": 4, "reps": "8", "inj": "Knee Joint", "alt": "Leg Press"}
        ]
    },
    "Bro Split (Classic)": {
        "CHEST": [{"name": "Flat Bench", "sets": 4, "reps": "10", "inj": "Front Shoulder", "alt": "Floor Press"}],
        "BACK": [{"name": "Seated Rows", "sets": 4, "reps": "12", "inj": "Lower Back", "alt": "Chest Supported Rows"}],
        "LEGS": [{"name": "Leg Press", "sets": 4, "reps": "15", "inj": "Knee Joint", "alt": "Goblet Squats"}]
    },
    "Upper/Lower Body": {
        "UPPER": [{"name": "Rows", "sets": 4, "reps": "10", "inj": "Lower Back", "alt": "Lat Pulldowns"}],
        "LOWER": [{"name": "Squats", "sets": 4, "reps": "8", "inj": "Knee Joint", "alt": "Leg Extensions"}]
    }
}

# --- Stage 1: Awakening ---
if st.session_state.step == 'awakening':
    st.markdown('<div class="system-title"><h1>SYSTEM NOTIFICATION</h1></div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#ff00ff; font-weight:bold;">[WARNING: YOU HAVE BECOME A PLAYER]</p>', unsafe_allow_html=True)
    
    u_id = st.text_input("PLAYER NAME", placeholder="Enter your name...")
    c1, c2 = st.columns(2)
    u_gen = c1.selectbox("GENDER", ["MALE (Hunter)", "FEMALE (Huntress)"])
    u_path = c2.selectbox("TRAINING PATH", list(DB.keys())) # الـ 3 مسارات هنا
    
    u_inj = st.multiselect("DETAILED INJURY SCAN", ["Front Shoulder", "Side Shoulder", "Lower Back", "Knee Joint", "Elbow Joint"])
    
    cw, ch = st.columns(2)
    u_w = cw.text_input("WEIGHT (KG)", "80")
    u_h = ch.text_input("HEIGHT (CM)", "175")

    if st.button("ARISE"):
        if u_id:
            st.session_state.player = {"name": u_id, "gen": u_gen, "path": u_path, "inj": u_inj}
            st.session_state.step = 'mission'
            st.rerun()

# --- Stage 2: Mission HUD ---
elif st.session_state.step == 'mission':
    p = st.session_state.player
    st.markdown(f"<div style='display:flex; justify-content:space-between;'><h2 style='color:#ff00ff; margin:0;'>LVL. {st.session_state.level}</h2><b>PLAYER:</b> {p['name'].upper()}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='xp-bar-container'><div class='xp-bar-fill' style='width:{st.session_state.xp}%;'></div></div>", unsafe_allow_html=True)

    day = st.selectbox("SELECT SESSION", list(DB[p['path']].keys()))
    st.write("---")

    for ex in DB[p['path']][day]:
        injured = ex['inj'] in p['inj']
        ex_name = ex['alt'] if injured else ex['name']
        
        st.markdown(f"""<div class="{'alt-card' if injured else 'exercise-card'}">
            <span style="font-weight:bold;">{'🔄 ' if injured else '⚔️ '}{ex_name}</span><br>
            <span style="color:#ff00ff; font-family:'Orbitron'; font-size:12px;">{ex['sets']} SETS x {ex['reps']} REPS</span>
        </div>""", unsafe_allow_html=True)

        col_inv, col_timer = st.columns([2, 1])
        weight_key = f"w_{ex_name}"
        prev_w = st.session_state.inventory.get(weight_key, "0")
        new_w = col_inv.text_input(f"Weight (Last: {prev_w}kg)", key=f"in_{ex_name}")
        if new_w != "0" and new_w != prev_w: st.session_state.inventory[weight_key] = new_w

        if col_timer.button(f"⏱️ Rest", key=f"t_{ex_name}"):
            with st.empty():
                for i in range(60, 0, -1):
                    st.write(f"⌛ {i}s")
                    time.sleep(1)
                st.write("🔥 GO!")

        if st.checkbox("Complete Mission (+20 XP)", key=f"c_{ex_name}"):
            add_xp(20)

    if st.sidebar.button("RESET"):
        st.session_state.step = 'awakening'
        st.rerun()
