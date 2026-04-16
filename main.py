import streamlit as st
from datetime import datetime

# 1. نظام الـ HUD الأسطوري (Solo Leveling Identity)
st.set_page_config(page_title="THE SYSTEM", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    /* منع اللون الأبيض والسواد المطلق */
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    header, footer { display: none !important; }

    /* نوافذ النظام (System Windows) */
    .system-card {
        background: rgba(0, 10, 20, 0.85); border: 2px solid #00d4ff;
        border-left: 8px solid #00d4ff; padding: 20px; margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
    }
    
    .status-bar {
        font-family: 'Orbitron'; background: linear-gradient(90deg, #00d4ff22, transparent);
        padding: 10px; border-bottom: 1px solid #00d4ff; margin-bottom: 20px;
    }

    /* إجبار الخانات على السواد */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[role="listbox"], li[role="option"] {
        background-color: #000 !important; color: #00d4ff !important; border: 1px solid #00d4ff33 !important;
    }

    /* أزرار النظام (Quest Buttons) */
    .stButton > button {
        width: 100%; background: #00d4ff11 !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 3px;
        padding: 12px !important; text-transform: uppercase; transition: 0.3s;
    }
    .stButton > button:hover { background: #00d4ff33 !important; box-shadow: 0 0 20px #00d4ff; }
    
    .injury-tag { color: #ff0055; font-size: 11px; font-weight: bold; text-shadow: 0 0 5px #ff0055; }
    .safe-tag { color: #00ffaa; font-size: 11px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic & State
if 'lang' not in st.session_state: st.session_state.lang = 'AR'
if 'history' not in st.session_state: st.session_state.history = []
if 'level' not in st.session_state: st.session_state.level = 1
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'step' not in st.session_state: st.session_state.step = 'awakening'

# نصوص الهوية (System Identity)
TEXTS = {
    'AR': {
        'title': 'نظام تحسين الحالة (STATUS SYSTEM)',
        'id': 'معرف اللاعب', 'gen': 'الجنس (GENDER)', 'path': 'المسار المختاره',
        'inj': 'مسح الإصابات (INJURY SCAN)', 'arise': 'نهوض (ARISE)',
        'quest_title': 'مهمة اليوم: تدريب القوة', 'log': 'سجل الإنجازات',
        'comp': 'تحصيل المكافأة', 'skip': '[تم استبعاد التمرين]', 'alt': 'بديل النظام: '
    },
    'EN': {
        'title': 'STATUS SYSTEM (INITIALIZATION)',
        'id': 'PLAYER ID', 'gen': 'GENDER', 'path': 'SELECTED PATH',
        'inj': 'INJURY SCAN', 'arise': 'ARISE',
        'quest_title': 'DAILY QUEST: STRENGTH TRAINING', 'log': 'ACHIEVEMENT LOG',
        'comp': 'COLLECT REWARD', 'skip': '[EXERCISE EXCLUDED]', 'alt': 'SYSTEM ALT: '
    }
}
T = TEXTS[st.session_state.lang]

# تبديل اللغة
if st.sidebar.button("🌐 SYSTEM LANG"):
    st.session_state.lang = 'EN' if st.session_state.lang == 'AR' else 'AR'
    st.rerun()

# التمارين الكاملة
DB = {
    "PPL": {
        "Push": [
            {"AR": "بنش برس بار", "EN": "Barbell Bench Press", "i": "Shoulder", "alt": "Floor Press"},
            {"AR": "عسكري بار واقف", "EN": "Military Press", "i": "Shoulder", "alt": "Landmine Press"},
            {"AR": "رفرفة جانبي كابل", "EN": "Cable Lateral Raise", "i": "Shoulder", "alt": "Front Raise"},
            {"AR": "تراي كابل مسطرة", "EN": "Tricep Pushdowns", "i": "Elbow", "alt": "Diamond Pushups"}
        ],
        "Pull": [
            {"AR": "رفعة ميتة (Deadlift)", "EN": "Deadlifts", "i": "Back", "alt": "Rack Pulls"},
            {"AR": "عقلة واسع", "EN": "Wide Pullups", "i": "Shoulder", "alt": "Lat Pulldown"},
            {"AR": "باي بار مستقيم", "EN": "Barbell Curls", "i": "Elbow", "alt": "Hammer Curls"}
        ]
    }
}

# --- المرحلة الأولى: Awakening (HUD) ---
if st.session_state.step == 'awakening':
    st.markdown(f'<div class="system-card" style="text-align:center;"><h2>{T["title"]}</h2><p style="color:#ff00ff;">[تحذير: بمجرد القبول، لا يمكنك التراجع]</p></div>', unsafe_allow_html=True)
    
    u_id = st.text_input(T['id'], placeholder="ADAM...")
    col1, col2 = st.columns(2)
    u_gen = col1.selectbox(T['gen'], ["MALE (Hunter)", "FEMALE (Huntress)"])
    u_path = col2.selectbox(T['path'], list(DB.keys()))
    
    u_inj = st.multiselect(T['inj'], ["Shoulder", "Back", "Knee", "Elbow", "Ankle"])
    
    cw, ch = st.columns(2)
    u_w = cw.number_input("WEIGHT (KG)", value=80)
    u_h = ch.number_input("HEIGHT (CM)", value=175)

    if st.button(T['arise']):
        if u_id:
            bmi = round(u_w / ((u_h/100)**2), 1)
            rank = "S-RANK" if 20 <= bmi <= 25 else "A-RANK"
            st.session_state.player = {"id": u_id, "gen": u_gen, "path": u_path, "inj": u_inj, "rank": rank}
            st.session_state.step = 'status'
            st.rerun()

# --- المرحلة الثانية: Main Status HUD ---
elif st.session_state.step == 'status':
    p = st.session_state.player
    
    # Status Bar الأسطوري
    st.markdown(f"""
    <div class="status-bar">
        PLAYER: {p['id'].upper()} | LVL: {st.session_state.level} | RANK: {p['rank']} <br>
        <span style="font-size:10px; color:#ff00ff;">XP: {st.session_state.xp}/100 [||||||||||]</span>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs([T['quest_title'], T['log']])

    with tab1:
        target = st.selectbox("SELECT ZONE", list(DB[p['path']].keys()))
        st.markdown(f"<div class='system-card'><b>MISSION: {target.upper()}</b></div>", unsafe_allow_html=True)
        
        exs = DB[p['path']][target]
        for i, ex in enumerate(exs):
            name = ex[st.session_state.lang]
            if ex['i'] in p['inj']:
                st.markdown(f"<p class='injury-tag'>{T['skip']} {name}</p><p class='safe-tag'>{T['alt']} {ex['alt']}</p>", unsafe_allow_html=True)
                st.checkbox(f"⚔️ {ex['alt']} (Safe Protocol)", key=f"alt_{i}")
            else:
                st.checkbox(f"⚔️ {name}", key=f"q_{i}")
        
        if st.button(T['comp']):
            st.session_state.xp += 34
            if st.session_state.xp >= 100:
                st.session_state.level += 1
                st.session_state.xp = 0
            st.session_state.history.append({"time": datetime.now().strftime("%H:%M"), "task": target})
            st.rerun()

    with tab2:
        for log in reversed(st.session_state.history):
            st.markdown(f"<p style='color:#00ffaa; border-bottom:1px solid #111;'>[{log['time']}] {log['task']} - SUCCESS</p>", unsafe_allow_html=True)

    if st.sidebar.button("TERMINATE SESSION"):
        st.session_state.step = 'awakening'
        st.rerun()
