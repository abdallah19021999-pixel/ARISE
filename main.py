import streamlit as st
import time

# 1. إعدادات النظام والبصمة البصرية (Solo Leveling HUD)
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

    /* تأثير الـ Scanlines الرقمي */
    .stApp::before {
        content: " "; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.1) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0.01), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.01));
        background-size: 100% 4px, 3px 100%; z-index: -1; pointer-events: none;
    }

    /* شريط الـ XP المتوهج */
    .xp-bar-container {
        width: 100%; background-color: rgba(0, 212, 255, 0.1);
        border: 1px solid #00d4ff; height: 12px; border-radius: 6px; margin: 10px 0;
    }
    .xp-bar-fill {
        height: 100%; background: linear-gradient(90deg, #00d4ff, #00fbff);
        box-shadow: 0 0 15px #00d4ff; border-radius: 6px; transition: width 0.5s ease;
    }

    /* كروت التمارين (Glassmorphism) */
    .exercise-card {
        background: rgba(0, 212, 255, 0.05); backdrop-filter: blur(5px);
        border: 1px solid rgba(0, 212, 255, 0.2); border-left: 5px solid #00d4ff;
        padding: 15px; margin: 10px 0; border-radius: 4px;
        transition: 0.3s;
    }
    .exercise-card:hover { transform: translateX(8px); background: rgba(0, 212, 255, 0.1); }

    .alt-card {
        background: rgba(255, 0, 255, 0.05); border-left: 5px solid #ff00ff;
        padding: 15px; margin: 10px 0; border-radius: 4px; border: 1px solid rgba(255, 0, 255, 0.2);
    }

    /* إخفاء الرمادي والزوائد */
    input, .stNumberInput div { background-color: #000 !important; color: #00d4ff !important; border: 1px solid #00d4ff33 !important; }
    [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }
    label { color: #888 !important; font-size: 10px !important; letter-spacing: 2px; }
    
    .level-text { font-family: 'Orbitron'; font-size: 24px; color: #ff00ff; text-shadow: 0 0 10px #ff00ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة (Leveling & Inventory Logic)
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'level' not in st.session_state: st.session_state.level = 1
if 'inventory' not in st.session_state: st.session_state.inventory = {}
if 'step' not in st.session_state: st.session_state.step = 'awakening'

def add_xp(amount):
    st.session_state.xp += amount
    if st.session_state.xp >= 100:
        st.session_state.level += 1
        st.session_state.xp = 0
        st.toast(f"🏆 LEVEL UP! REACHED LEVEL {st.session_state.level}", icon="🔥")

# 3. قاعدة البيانات الشاملة (التمارين والبدائل)
DB = {
    "PPL (Standard)": {
        "PUSH": [
            {"name": "Bench Press", "sets": 4, "reps": "8-10", "inj": "Front Shoulder", "alt": "Floor Press"},
            {"name": "Military Press", "sets": 3, "reps": "10", "inj": "Side Shoulder", "alt": "Landmine Press"},
            {"name": "Tricep Pushdown", "sets": 3, "reps": "15", "inj": "Elbow Joint", "alt": "Diamond Pushups"}
        ],
        "PULL": [
            {"name": "Deadlift", "sets": 3, "reps": "5", "inj": "Lower Back", "alt": "Lat Pulldowns"},
            {"name": "Barbell Rows", "sets": 4, "reps": "10", "inj": "Lower Back", "alt": "Chest Supported Rows"}
        ]
    }
}

# --- Phase 1: Awakening ---
if st.session_state.step == 'awakening':
    st.markdown("<h1 style='text-align:center; font-family:Orbitron;'>SYSTEM AWAKENING</h1>", unsafe_allow_html=True)
    
    u_id = st.text_input("PLAYER NAME", placeholder="Enter your name...")
    c1, c2 = st.columns(2)
    u_gen = c1.selectbox("GENDER", ["MALE (Hunter)", "FEMALE (Huntress)"])
    u_path = c2.selectbox("TRAINING PATH", list(DB.keys()))
    
    u_inj = st.multiselect("INJURY SCAN", ["Front Shoulder", "Side Shoulder", "Lower Back", "Knee Joint", "Elbow Joint"])
    
    col_w, col_h = st.columns(2)
    u_w = col_w.text_input("WEIGHT (KG)", "80")
    u_h = col_h.text_input("HEIGHT (CM)", "175")

    if st.button("ARISE"):
        if u_id:
            st.session_state.player = {"name": u_id, "gen": u_gen, "path": u_path, "inj": u_inj}
            st.session_state.step = 'mission'
            st.rerun()

# --- Phase 2: Mission HUD ---
elif st.session_state.step == 'mission':
    p = st.session_state.player
    
    # رأس الصفحة (Status Bar)
    st.markdown(f"""
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div class='level-text'>LVL. {st.session_state.level}</div>
            <div style='text-align: right;'><b>PLAYER:</b> {p['name'].upper()}<br><small>{p['gen']}</small></div>
        </div>
        <div class='xp-bar-container'><div class='xp-bar-fill' style='width: {st.session_state.xp}%;'></div></div>
    """, unsafe_allow_html=True)

    day = st.selectbox("MISSION TYPE", list(DB[p['path']].keys()))
    st.write("---")

    for ex in DB[p['path']][day]:
        is_injured = ex['inj'] in p['inj']
        ex_name = ex['alt'] if is_injured else ex['name']
        card_class = "alt-card" if is_injured else "exercise-card"
        
        st.markdown(f"""<div class="{card_class}">
            <b style="font-size:18px;">{'🔄 ' if is_injured else '⚔️ '}{ex_name}</b><br>
            <span style="color:#ff00ff; font-family:Orbitron; font-size:12px;">{ex['sets']} SETS x {ex['reps']} REPS</span>
        </div>""", unsafe_allow_html=True)
        
        col_inv, col_timer = st.columns([2, 1])
        
        # 1. نظام الـ Inventory (تتبع الوزن)
        weight_key = f"weight_{ex_name}"
        prev_weight = st.session_state.inventory.get(weight_key, "0")
        current_weight = col_inv.text_input(f"Current Weight (Prev: {prev_weight}kg)", key=f"in_{ex_name}")
        
        if current_weight != "0" and current_weight != prev_weight:
            st.session_state.inventory[weight_key] = current_weight

        # 2. عداد الراحة (Rest Timer)
        if col_timer.button(f"⏱️ Rest", key=f"btn_{ex_name}"):
            with st.empty():
                for i in range(60, 0, -1):
                    st.write(f"⌛ Rest: {i}s")
                    time.sleep(1)
                st.write("✅ Ready!")
                st.balloons()

        # 3. الـ Checkpoint (كسب XP)
        if st.checkbox("Task Completed (+20 XP)", key=f"chk_{ex_name}"):
            add_xp(2) # كل تمرين يعطي زيادة بسيطة، والتحفيز عند النهاية

    if st.sidebar.button("LOGOUT / RESET"):
        st.session_state.step = 'awakening'
        st.rerun()
