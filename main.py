import streamlit as st
from datetime import datetime

# 1. تدمير اللون الأبيض (True Black HUD)
st.set_page_config(page_title="SYSTEM HUD", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    /* الخلفية والنصوص */
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    
    /* إخفاء الهيدر وأدوات التحكم البيضاء */
    header, footer, [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }

    /* تعديل الـ Tabs لتكون سوداء بالكامل */
    .stTabs [data-baseweb="tab-list"] { background-color: #000 !important; border-bottom: 1px solid #00d4ff33 !important; }
    .stTabs [data-baseweb="tab"] { background-color: #000 !important; color: #00d4ff !important; border: none !important; }
    .stTabs [aria-selected="true"] { border-bottom: 2px solid #ff00ff !important; }

    /* تعديل الحواف وصناديق الإدخال (No White Borders) */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="base-input"], div[role="listbox"] {
        background-color: #050505 !important; 
        border: 1px solid #00d4ff44 !important; 
        color: #00d4ff !important;
    }
    
    /* الأزرار */
    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 2px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 5px;
        padding: 15px !important; text-transform: uppercase;
    }
    .stButton > button:hover { background: rgba(0, 212, 255, 0.1) !important; box-shadow: 0 0 20px #00d4ff; }

    /* التنبيهات */
    .system-window {
        background: rgba(0, 10, 20, 0.8); border: 2px solid #00d4ff;
        padding: 20px; border-radius: 2px; margin-bottom: 20px;
    }
    
    label { color: #333 !important; font-size: 10px !important; }
    input { color: #00d4ff !important; background: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة واللغة
if 'lang' not in st.session_state: st.session_state.lang = 'AR'
if 'history' not in st.session_state: st.session_state.history = []
if 'level' not in st.session_state: st.session_state.level = 1
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'step' not in st.session_state: st.session_state.step = 'awakening'

# قاموس اللغة (Language Protocol)
TEXTS = {
    'AR': {
        'init': 'إعداد النظام', 'id': 'معرف اللاعب', 'gen': 'الجنس', 'male': 'ذكر (Hunter)', 'female': 'أنثى (Huntress)',
        'path': 'المسار', 'inj': 'مسح الإصابات', 'arise': 'نهوض (ARISE)', 'quest': 'المهمة اليومية', 'log': 'سجل اللاعب',
        'comp': 'إتمام المهمة', 'skip': '⚠️ تخطي: ', 'alt': 'البديل الآمن: '
    },
    'EN': {
        'init': 'SYSTEM INITIALIZATION', 'id': 'PLAYER ID', 'gen': 'GENDER', 'male': 'MALE (Hunter)', 'female': 'FEMALE (Huntress)',
        'path': 'PATH', 'inj': 'INJURY SCAN', 'arise': 'ARISE', 'quest': 'DAILY QUEST', 'log': 'PLAYER LOG',
        'comp': 'COMPLETE MISSION', 'skip': '⚠️ SKIP: ', 'alt': 'SAFE ALT: '
    }
}
T = TEXTS[st.session_state.lang]

# تبديل اللغة في الجانب
if st.sidebar.button("🌐 AR/EN"):
    st.session_state.lang = 'EN' if st.session_state.lang == 'AR' else 'AR'
    st.rerun()

# قاعدة بيانات التمارين (كاملة باللغتين)
TRAINER_DB = {
    "PPL": {
        "Push": [
            {"AR": "بنش برس بار", "EN": "Barbell Bench Press", "i": "Shoulder", "alt": "Floor Press"},
            {"AR": "تجميع دمبل مائل", "EN": "Incline DB Press", "i": "Shoulder", "alt": "Low Incline Hex"},
            {"AR": "عسكري بار", "EN": "Military Press", "i": "Shoulder", "alt": "Landmine Press"},
            {"AR": "تراي كابل", "EN": "Tricep Pushdowns", "i": "Elbow", "alt": "Diamond Pushups"},
            {"AR": "رفرفة جانبي", "EN": "Lateral Raises", "i": "Shoulder", "alt": "Cable Lateral"}
        ],
        "Pull": [
            {"AR": "عقلة واسع", "EN": "Wide Pullups", "i": "Shoulder", "alt": "Lat Pulldown (Neutral)"},
            {"AR": "رفعة ميتة", "EN": "Deadlifts", "i": "Back", "alt": "Rack Pulls"},
            {"AR": "سحب بار ظهر", "EN": "Barbell Rows", "i": "Back", "alt": "Chest Supported Rows"},
            {"AR": "باي بار", "EN": "Barbell Curls", "i": "Elbow", "alt": "Preacher Curls"}
        ]
    }
}

# --- المرحلة الأولى: Awakening ---
if st.session_state.step == 'awakening':
    st.markdown(f'<div class="system-window" style="text-align:center;"><h2>{T["init"]}</h2></div>', unsafe_allow_html=True)
    
    u_id = st.text_input(T['id'], placeholder="ADAM...")
    col_g, col_p = st.columns(2)
    u_gen = col_g.selectbox(T['gen'], [T['male'], T['female']])
    u_path = col_p.selectbox(T['path'], ["PPL"])
    
    u_inj = st.multiselect(T['inj'], ["Shoulder", "Back", "Knee", "Elbow", "Ankle"])
    
    cw, ch = st.columns(2)
    u_w = cw.number_input("WEIGHT", value=80)
    u_h = ch.number_input("HEIGHT", value=175)

    if st.button(T['arise']):
        if u_id:
            bmi = round(u_w / ((u_h/100)**2), 1)
            rank = "S-RANK" if 20 <= bmi <= 25 else "A-RANK"
            st.session_state.player = {"id": u_id, "gender": u_gen, "path": u_path, "inj": u_inj, "rank": rank}
            st.session_state.step = 'status'
            st.rerun()

# --- المرحلة الثانية: Combat HUD ---
elif st.session_state.step == 'status':
    p = st.session_state.player
    st.markdown(f"**PLAYER:** {p['id'].upper()} | **LVL:** {st.session_state.level} | **{p['rank']}**")
    
    tab1, tab2 = st.tabs([T['quest'], T['log']])

    with tab1:
        zones = list(TRAINER_DB[p['path']].keys())
        target = st.selectbox("ZONE", zones)
        
        exs = TRAINER_DB[p['path']][target]
        checks = 0
        
        for i, ex in enumerate(exs):
            ex_name = ex[st.session_state.lang]
            if ex['i'] in p['inj']:
                st.markdown(f"<span style='color:#ff4b4b;'>{T['skip']} {ex_name}</span><br><small style='color:#00ffaa;'>{T['alt']} {ex['alt']}</small>", unsafe_allow_html=True)
                if st.checkbox(f"⚔️ {ex['alt']} (Safe)", key=f"alt_{i}"): checks += 1
            else:
                if st.checkbox(f"⚔️ {ex_name}", key=f"q_{i}"): checks += 1
        
        if st.button(T['comp']):
            if checks > 0:
                st.session_state.history.append({"time": datetime.now().strftime("%H:%M"), "task": target})
                st.session_state.xp += 34
                if st.session_state.xp >= 100:
                    st.session_state.level += 1
                    st.session_state.xp = 0
                st.rerun()

    with tab2:
        for log in reversed(st.session_state.history):
            st.markdown(f"<p style='border-bottom:1px solid #111;'>[{log['time']}] {log['task']} - DONE</p>", unsafe_allow_html=True)

    if st.sidebar.button("TERMINATE"):
        st.session_state.step = 'awakening'
        st.rerun()
