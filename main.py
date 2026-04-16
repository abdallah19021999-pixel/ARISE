import streamlit as st
from datetime import datetime

# 1. بروتوكول السواد المطلق (Absolute Void Injection)
st.set_page_config(page_title="SYSTEM HUD", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    header, footer { display: none !important; }

    /* استهداف دقيق لتدمير اللون الأبيض في الخانات */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[role="listbox"], 
    li[role="option"], div[data-baseweb="base-input"], input, .stNumberInput div {
        background-color: #000000 !important; 
        color: #00d4ff !important; 
        border: 1px solid #00d4ff66 !important;
    }
    
    /* نافذة إشعار النظام (The Iconic Box) */
    .system-notification {
        background: transparent; border: 2px solid #00d4ff;
        padding: 40px; text-align: center; margin-bottom: 30px;
        box-shadow: inset 0 0 15px rgba(0, 212, 255, 0.2), 0 0 15px rgba(0, 212, 255, 0.2);
    }
    
    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 4px;
        padding: 10px !important; text-transform: uppercase;
    }
    .stButton > button:hover { background: rgba(0, 212, 255, 0.1) !important; box-shadow: 0 0 20px #00d4ff; }
    
    label { color: #333 !important; font-size: 10px !important; }
    .warning-text { color: #00d4ff; font-family: 'Orbitron'; font-size: 14px; letter-spacing: 2px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic & Language Setup
if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'step' not in st.session_state: st.session_state.step = 'awakening'
if 'history' not in st.session_state: st.session_state.history = []

# تبديل اللغة في السايد بار
if st.sidebar.button("🌐 SWITCH LANGUAGE"):
    st.session_state.lang = 'AR' if st.session_state.lang == 'EN' else 'EN'
    st.rerun()

# نصوص الهوية الرسمية بناءً على الصور
UI = {
    'EN': {
        'notify': 'SYSTEM NOTIFICATION',
        'warn': '[WARNING: YOU HAVE BECOME A PLAYER]',
        'id': 'PLAYER NAME', 'gen': 'GENDER', 'path': 'CHOOSE YOUR PATH',
        'inj': 'INJURY SCAN', 'arise': 'ARISE'
    },
    'AR': {
        'notify': 'إشعار النظام',
        'warn': '[تحذير: لقد أصبحت لاعباً الآن]',
        'id': 'اسم اللاعب', 'gen': 'الجنس', 'path': 'اختر مسارك',
        'inj': 'مسح الإصابات', 'arise': 'نهوض'
    }
}
U = UI[st.session_state.lang]

# قاعدة التمارين الكاملة (تلبية لطلب تعدد الأنظمة)
DB = {
    "PPL (Push/Pull/Legs)": {
        "Push": [{"AR": "بنش برس", "EN": "Bench Press", "i": "Shoulder", "alt": "Floor Press"}, {"AR": "تراي كابل", "EN": "Tricep Push", "i": "Elbow", "alt": "Diamond"}],
        "Pull": [{"AR": "رفعة ميتة", "EN": "Deadlift", "i": "Back", "alt": "Rack Pull"}, {"AR": "عقلة", "EN": "Pullups", "i": "Shoulder", "alt": "Pulldown"}],
        "Legs": [{"AR": "سكوات", "EN": "Squat", "i": "Knee", "alt": "Box Squat"}]
    },
    "Bro Split": {
        "Chest": [{"AR": "تجميع دمبل", "EN": "DB Press", "i": "Shoulder", "alt": "Pushups"}],
        "Back": [{"AR": "سحب أرضي", "EN": "Seated Row", "i": "Back", "alt": "Pulldown"}]
    }
}

# --- المرحلة الأولى: Awakening ---
if st.session_state.step == 'awakening':
    st.markdown(f"""
        <div class="system-notification">
            <h1 style="font-family: 'Orbitron'; color:#00d4ff; margin:0;">{U['notify']}</h1>
            <p class="warning-text">{U['warn']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    u_id = st.text_input(U['id'], placeholder="ADAM...")
    col1, col2 = st.columns(2)
    u_gen = col1.selectbox(U['gen'], ["MALE (Hunter)", "FEMALE (Huntress)"])
    u_path = col2.selectbox(U['path'], list(DB.keys()))
    
    u_inj = st.multiselect(U['inj'], ["Shoulder", "Back", "Knee", "Elbow", "Ankle"])
    
    cw, ch = st.columns(2)
    u_w = cw.number_input("WEIGHT", value=80)
    u_h = ch.number_input("HEIGHT", value=175)

    if st.button(U['arise']):
        if u_id:
            st.session_state.player = {"id": u_id, "path": u_path, "inj": u_inj, "rank": "A-RANK"}
            st.session_state.step = 'status'
            st.rerun()

# --- المرحلة الثانية: HUD (كمل بنفس النمط) ---
elif st.session_state.step == 'status':
    p = st.session_state.player
    st.markdown(f"**PLAYER:** {p['id'].upper()} | **{p['rank']}**")
    
    zone = st.selectbox("MISSION AREA", list(DB[p['path']].keys()))
    for ex in DB[p['path']][zone]:
        st.checkbox(f"⚔️ {ex[st.session_state.lang]}")
    
    if st.sidebar.button("TERMINATE"):
        st.session_state.step = 'awakening'
        st.rerun()
