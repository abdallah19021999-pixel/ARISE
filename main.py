import streamlit as st
from datetime import datetime

# 1. بروتوكول تدمير الأبيض (True Void HUD)
st.set_page_config(page_title="SYSTEM HUD", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    /* الخلفية الأساسية */
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    header, footer { display: none !important; }

    /* إجبار الخانات والقوائم على السواد المطلق ومنع الأبيض */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[role="listbox"], 
    li[role="option"], div[data-baseweb="base-input"], input {
        background-color: #000000 !important; 
        color: #00d4ff !important; 
        border: 1px solid #00d4ff55 !important;
    }
    
    /* منع اللون الرمادي الفاتح في خانات الأرقام */
    div[data-testid="stNumberInput"] div {
        background-color: #000000 !important;
        border: none !important;
    }

    /* تعديل التابس (Tabs) */
    .stTabs [data-baseweb="tab-list"] { background-color: #000 !important; }
    .stTabs [data-baseweb="tab"] { color: #00d4ff !important; background: #000 !important; }
    .stTabs [aria-selected="true"] { border-bottom: 2px solid #ff00ff !important; }

    .system-card {
        background: rgba(0, 5, 15, 0.9); border: 2px solid #00d4ff;
        border-left: 10px solid #00d4ff; padding: 25px; margin-bottom: 20px;
    }
    
    .stButton > button {
        width: 100%; background: #00d4ff11 !important; color: #00d4ff !important;
        border: 2px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 5px;
    }
    .stButton > button:hover { background: #00d4ff33 !important; box-shadow: 0 0 25px #00d4ff; }
    
    label { color: #555 !important; font-size: 11px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة واللغة
if 'lang' not in st.session_state: st.session_state.lang = 'AR'
if 'step' not in st.session_state: st.session_state.step = 'awakening'
if 'level' not in st.session_state: st.session_state.level = 1
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'history' not in st.session_state: st.session_state.history = []

# قاموس النظام المتكامل
TEXTS = {
    'AR': {
        'title': 'نظام تحسين الحالة (STATUS SYSTEM)', 'id': 'معرف اللاعب', 
        'gen': 'الجنس', 'path': 'المسار التدريبي', 'inj': 'مسح الإصابات', 
        'arise': 'نهوض (ARISE)', 'quest': 'المهمة اليومية', 'log': 'سجل اللاعب',
        'comp': 'تحصيل المكافأة', 'skip': '[تم الاستبعاد]', 'alt': 'البديل الآمن: '
    },
    'EN': {
        'title': 'STATUS SYSTEM (REAWAKENED)', 'id': 'PLAYER ID', 
        'gen': 'GENDER', 'path': 'TRAINING PATH', 'inj': 'INJURY SCAN', 
        'arise': 'ARISE', 'quest': 'DAILY QUEST', 'log': 'PLAYER LOG',
        'comp': 'COLLECT REWARD', 'skip': '[EXCLUDED]', 'alt': 'SAFE ALT: '
    }
}
T = TEXTS[st.session_state.lang]

# تبديل اللغة
if st.sidebar.button("🌐 SWITCH LANGUAGE"):
    st.session_state.lang = 'EN' if st.session_state.lang == 'AR' else 'AR'
    st.rerun()

# أرشيف التمارين الكامل (تلبية لطلب تعدد الأنظمة)
DB = {
    "PPL (Push/Pull/Legs)": {
        "Push": [
            {"AR": "بنش برس بار", "EN": "Barbell Bench Press", "i": "Shoulder", "alt": "Floor Press"},
            {"AR": "عسكري بار واقف", "EN": "Military Press", "i": "Shoulder", "alt": "Landmine Press"},
            {"AR": "تراي كابل", "EN": "Tricep Pushdowns", "i": "Elbow", "alt": "Diamond Pushups"}
        ],
        "Pull": [
            {"AR": "رفعة ميتة", "EN": "Deadlifts", "i": "Back", "alt": "Rack Pulls"},
            {"AR": "عقلة واسع", "EN": "Wide Pullups", "i": "Shoulder", "alt": "Lat Pulldown"}
        ]
    },
    "Bro Split (Single Muscle)": {
        "Chest Day": [{"AR": "بنش مستوي", "EN": "Flat Bench", "i": "Shoulder", "alt": "Pushups"}],
        "Back Day": [{"AR": "سحب عالي", "EN": "Lat Pulldown", "i": "Back", "alt": "Rows"}]
    }
}

# --- المرحلة الأولى: Awakening ---
if st.session_state.step == 'awakening':
    st.markdown(f'<div class="system-card" style="text-align:center;"><h2>{T["title"]}</h2></div>', unsafe_allow_html=True)
    
    u_id = st.text_input(T['id'], placeholder="ADAM...")
    col1, col2 = st.columns(2)
    u_gen = col1.selectbox(T['gen'], ["MALE (Hunter)", "FEMALE (Huntress)"])
    u_path = col2.selectbox(T['path'], list(DB.keys()))
    
    u_inj = st.multiselect(T['inj'], ["Shoulder", "Back", "Knee", "Elbow", "Ankle"])
    
    cw, ch = st.columns(2)
    u_w = cw.number_input("WEIGHT", value=80)
    u_h = ch.number_input("HEIGHT", value=175)

    if st.button(T['arise']):
        if u_id:
            bmi = round(u_w / ((u_h/100)**2), 1)
            rank = "S-RANK" if 20 <= bmi <= 25 else "A-RANK"
            st.session_state.player = {"id": u_id, "gen": u_gen, "path": u_path, "inj": u_inj, "rank": rank}
            st.session_state.step = 'status'
            st.rerun()

# --- المرحلة الثانية: Main HUD ---
elif st.session_state.step == 'status':
    p = st.session_state.player
    st.markdown(f"**PLAYER:** {p['id'].upper()} | **LVL:** {st.session_state.level} | **{p['rank']}**")
    
    tab1, tab2 = st.tabs([T['quest'], T['log']])

    with tab1:
        zone = st.selectbox("SELECT ZONE", list(DB[p['path']].keys()))
        exs = DB[p['path']][zone]
        
        for i, ex in enumerate(exs):
            name = ex[st.session_state.lang]
            if ex['i'] in p['inj']:
                st.markdown(f"<p style='color:#ff0055;'>{T['skip']} {name}</p><small>{T['alt']} {ex['alt']}</small>", unsafe_allow_html=True)
                st.checkbox(f"⚔️ {ex['alt']}", key=f"alt_{i}")
            else:
                st.checkbox(f"⚔️ {name}", key=f"q_{i}")
        
        if st.button(T['comp']):
            st.session_state.xp += 34
            if st.session_state.xp >= 100:
                st.session_state.level += 1
                st.session_state.xp = 0
            st.session_state.history.append({"time": datetime.now().strftime("%H:%M"), "task": zone})
            st.rerun()

    if st.sidebar.button("TERMINATE"):
        st.session_state.step = 'awakening'
        st.rerun()
