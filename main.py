import streamlit as st
import json
import os

# 1. إعدادات الصفحة - Mobile First
st.set_page_config(page_title="ARISE SYSTEM", page_icon="⚡", layout="centered")

# 2. الواجهة البصرية (The System UI) - مستوحاة من الصور التي أرفقتها
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    .stApp {
        background-color: #00050a;
        background-image: radial-gradient(circle at center, #001529 0%, #00050a 100%);
        color: #e0f2ff;
        font-family: 'Orbitron', sans-serif;
    }

    /* كارت الحالة الاحترافي - Status Window */
    .status-window {
        border: 2px solid #00d4ff;
        background: rgba(0, 20, 40, 0.8);
        border-radius: 5px;
        padding: 20px;
        box-shadow: 0 0 15px #00d4ff66, inset 0 0 10px #00d4ff33;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    
    .status-window::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, #00d4ff, transparent);
    }

    /* أزرار العضلات - Interactive Body Nodes */
    .stButton > button {
        width: 100%;
        background: rgba(0, 40, 80, 0.6);
        color: #00d4ff;
        border: 1px solid #00d4ff;
        border-radius: 0px;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 2px;
        transition: 0.4s;
        height: 50px;
        margin-bottom: 10px;
    }

    .stButton > button:hover {
        background: #00d4ff;
        color: #000;
        box-shadow: 0 0 20px #00d4ff;
    }

    /* الـ Progress Bar النيون */
    .stProgress > div > div > div > div {
        background-color: #00d4ff;
        box-shadow: 0 0 10px #00d4ff;
    }

    /* صناديق المهام - Quest Logs */
    .quest-item {
        border-left: 3px solid #00d4ff;
        background: rgba(0, 212, 255, 0.05);
        padding: 10px;
        margin: 5px 0;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات الذكية
def load_system_data():
    default = {
        "name": "HUNTER", "lv": 1, "xp": 0, "rank": "E",
        "job": "None", "title": "Wolf Assassin",
        "str": 10, "agi": 10, "vit": 10, "int": 10,
        "initialized": False, "lang": "en"
    }
    if os.path.exists("system_save.json"):
        with open("system_save.json", "r") as f:
            data = json.load(f)
            return {**default, **data}
    return default

if 'system' not in st.session_state:
    st.session_state.system = load_system_data()
data = st.session_state.system

# 4. شاشة الصحوة (The Awakening) - تسجيل الدخول لأول مرة
if not data['initialized']:
    st.markdown("<h1 style='text-align:center; color:#00d4ff;'>SYSTEM INITIALIZATION</h1>", unsafe_allow_html=True)
    with st.form("awakening"):
        name = st.text_input("ENTER PLAYER NAME", placeholder="...")
        if st.form_submit_button("ACCEPT THE CONTRACT"):
            if name:
                data.update({"name": name.upper(), "initialized": True})
                with open("system_save.json", "w") as f: json.dump(data, f)
                st.rerun()
    st.stop()

# 5. الواجهة الرئيسية (STATUS WINDOW)
st.markdown(f"""
    <div class="status-window">
        <h3 style='margin:0; text-align:center; border-bottom:1px solid #00d4ff33; padding-bottom:10px;'>STATUS</h3>
        <div style='display:flex; justify-content:space-between; margin-top:15px;'>
            <div>
                <p style='color:#888; font-size:12px; margin:0;'>NAME: {data['name']}</p>
                <p style='color:#00d4ff; font-size:24px; margin:0;'>LV. {data['lv']}</p>
            </div>
            <div style='text-align:right;'>
                <p style='color:#888; font-size:12px; margin:0;'>JOB: {data['job']}</p>
                <p style='color:#ffcc00; font-size:18px; margin:0;'>TITLE: {data['title']}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# شريط الخبرة
st.progress(data['xp']/100)
st.write(f"<p style='font-size:10px; text-align:right;'>XP: {data['xp']}/100</p>", unsafe_allow_html=True)

# 6. نظام اختيار العضلات - (Visual Body Selection)
st.write("### [ SELECT TARGET MUSCLE ]")
col1, col2 = st.columns(2)

workout_map = {
    "CHEST": [("Bench Press", 20), ("Chest Flys", 15)],
    "BACK": [("Deadlift", 25), ("Lat Pulldown", 15)],
    "SHOULDERS": [("OHP", 20), ("Lateral Raises", 10)],
    "LEGS": [("Squats", 30), ("Leg Press", 20)],
    "ARMS": [("Bicep Curls", 10), ("Tricep Pushdowns", 10)]
}

with col1:
    if st.button("🦾 SHOULDERS"): st.session_state.target = "SHOULDERS"
    if st.button("🛡️ CHEST"): st.session_state.target = "CHEST"
    if st.button("🐍 ARMS"): st.session_state.target = "ARMS"
with col2:
    if st.button("⚔️ BACK"): st.session_state.target = "BACK"
    if st.button("🦵 LEGS"): st.session_state.target = "LEGS"
    if st.button("🧘 RECOVERY"): st.session_state.target = "RECOVERY"

# عرض كويست العضلة المختارة
if 'target' in st.session_state and st.session_state.target != "RECOVERY":
    target = st.session_state.target
    st.markdown(f"#### 📜 QUEST LOG: {target}")
    total_potential_xp = 0
    for ex, xp in workout_map[target]:
        st.markdown(f"<div class='quest-item'>{ex} <span style='float:right; color:#00d4ff;'>+{xp} XP</span></div>", unsafe_allow_html=True)
        total_potential_xp += xp
    
    if st.button(f"COMPLETE {target} QUEST"):
        data['xp'] += total_potential_xp
        if data['xp'] >= 100:
            data['xp'] = 0
            data['lv'] += 1
            st.balloons()
        with open("system_save.json", "w") as f: json.dump(data, f)
        st.rerun()

# القائمة الجانبية للإعدادات
with st.sidebar:
    st.markdown("### SYSTEM SETTINGS")
    if st.button("RESET ALL DATA"):
        if os.path.exists("system_save.json"): os.remove("system_save.json")
        st.session_state.clear()
        st.rerun()
