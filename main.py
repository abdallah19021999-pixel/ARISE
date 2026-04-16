import streamlit as st
from datetime import datetime

# 1. تثبيت الهوية البصرية (The Great Monarch HUD)
st.set_page_config(page_title="THE SYSTEM", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    /* منع اللون الأبيض نهائياً */
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    header, footer, [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }

    /* تصميم نوافذ النظام (Glass HUD) */
    .system-window {
        background: rgba(0, 20, 40, 0.4); border: 2px solid #00d4ff;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
        padding: 25px; border-radius: 5px; margin-bottom: 25px;
    }

    /* تعديل شكل المدخلات لتناسب اللعبة */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {
        background-color: #050505 !important; border: 1px solid #00d4ff44 !important; color: #00d4ff !important;
    }
    input { color: #00d4ff !important; background: transparent !important; font-family: 'Orbitron'; }

    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 2px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 5px;
        padding: 15px !important; text-transform: uppercase; transition: 0.3s;
    }
    .stButton > button:hover { background: rgba(0, 212, 255, 0.1) !important; box-shadow: 0 0 30px #00d4ff; }
    
    label { color: #333 !important; font-size: 11px !important; }
    </style>
    """, unsafe_allow_html=True)

# إدارة الذاكرة
if 'history' not in st.session_state: st.session_state.history = []
if 'level' not in st.session_state: st.session_state.level = 1
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'step' not in st.session_state: st.session_state.step = 'awakening'

# قاعدة بيانات التمارين والحماية
EX_DATA = {
    "PPL": {
        "Push": [{"n": "Bench Press", "i": "Shoulder"}, {"n": "Lateral Raise", "i": "Shoulder"}, {"n": "Triceps", "i": "Elbow"}],
        "Pull": [{"n": "Lat Pulldown", "i": "Shoulder"}, {"n": "Deadlift", "i": "Back"}, {"n": "Bicep Curls", "i": "Elbow"}],
        "Legs": [{"n": "Squat", "i": "Knee"}, {"n": "Leg Press", "i": "Knee"}, {"n": "Calf Raises", "i": "Ankle"}]
    }
}

# --- المرحلة الأولى: Awakening (HUD Registration) ---
if st.session_state.step == 'awakening':
    st.markdown('<div class="system-window" style="text-align:center;"><h3>SYSTEM NOTIFICATION</h3><p>[تحذير: أنت على وشك أن تصبح لاعباً]</p></div>', unsafe_allow_html=True)
    
    u_id = st.text_input("PLAYER ID", placeholder="ADAM...")
    
    col1, col2 = st.columns(2)
    u_gen = col1.selectbox("GENDER", ["MALE (Hunter)", "FEMALE (Huntress)"])
    u_path = col2.selectbox("PATH", ["PPL", "Bro Split"])
    
    u_inj = st.multiselect("INJURY SCAN", ["Shoulder", "Back", "Knee", "Elbow", "Ankle"])
    
    cw, ch = st.columns(2)
    u_w = cw.number_input("WEIGHT", value=80)
    u_h = ch.number_input("HEIGHT", value=175)

    if st.button("ARISE"):
        if u_id:
            bmi = round(u_w / ((u_h/100)**2), 1)
            rank = "S-RANK" if 20 <= bmi <= 25 else "A-RANK"
            st.session_state.player = {"id": u_id, "gender": u_gen, "path": u_path, "injuries": u_inj, "rank": rank, "bmi": bmi}
            st.session_state.step = 'status'
            st.rerun()

# --- المرحلة الثانية: STATUS WINDOW (The True HUD) ---
elif st.session_state.step == 'status':
    p = st.session_state.player
    
    # نافذة الرتبة والحالة (Status Bar)
    st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
            <div style="font-family:Orbitron; border-left:3px solid #00d4ff; padding-left:10px;">
                <h2 style="margin:0;">{p['id'].upper()}</h2>
                <small>{p['gender']} | {p['rank']}</small>
            </div>
            <div style="text-align:right;">
                <p style="margin:0; font-family:Orbitron;">LVL. {st.session_state.level}</p>
                <p style="font-size:10px; color:#ff00ff;">XP: {st.session_state.xp}/100</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["DAILY QUEST", "PLAYER LOG"])

    with tab1:
        # نظام المهام المفلتر بناءً على الإصابة
        zone = st.selectbox("ZONE", ["Push", "Pull", "Legs"])
        st.markdown(f"<div class='system-window'><b>MISSION: {zone.upper()} PROTOCOL</b></div>", unsafe_allow_html=True)
        
        exs = EX_DATA["PPL"][zone]
        active_exs = 0
        checks = 0
        
        for i, ex in enumerate(exs):
            if ex['i'] in p['injuries']:
                st.markdown(f"<p style='color:#555;'><del>⚔️ {ex['n']}</del> [إصابة {ex['i']}]</p>", unsafe_allow_html=True)
            else:
                if st.checkbox(f"⚔️ {ex['n']}", key=f"q_{i}"): checks += 1
                active_exs += 1
        
        if st.button("COMPLETE QUEST"):
            if checks == active_exs and active_exs > 0:
                st.session_state.history.append({"time": datetime.now().strftime("%H:%M"), "task": zone})
                st.session_state.xp += 34
                if st.session_state.xp >= 100:
                    st.session_state.level += 1
                    st.session_state.xp = 0
                st.rerun()

    with tab2:
        st.markdown("### 📜 PREVIOUS RECORDS")
        for log in reversed(st.session_state.history):
            st.markdown(f"<p style='font-size:12px; border-bottom:1px solid #111;'>[{log['time']}] {log['task']} - COMPLETED</p>", unsafe_allow_html=True)

    if st.sidebar.button("TERMINATE"):
        st.session_state.step = 'awakening'
        st.rerun()
