import streamlit as st
from datetime import datetime

# 1. الواجهة المظلمة المطلقة (Void HUD - No White)
st.set_page_config(page_title="SYSTEM HUD", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    /* منع اللون الأبيض في كل مكان */
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    header, footer, [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }
    
    /* تعديل الـ Tabs */
    .stTabs [data-baseweb="tab-list"] { background-color: #000 !important; }
    .stTabs [data-baseweb="tab"] { color: #00d4ff !important; background: #000 !important; border: none !important; }
    .stTabs [aria-selected="true"] { border-bottom: 2px solid #ff00ff !important; }

    /* تعديل صناديق الإدخال */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="base-input"], div[role="listbox"] {
        background-color: #050505 !important; border: 1px solid #00d4ff44 !important; color: #00d4ff !important;
    }
    
    .system-window {
        background: rgba(0, 15, 30, 0.9); border: 2px solid #00d4ff;
        padding: 20px; border-radius: 5px; margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
    }
    
    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 2px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 5px; padding: 15px !important;
    }
    .stButton > button:hover { background: rgba(0, 212, 255, 0.1) !important; box-shadow: 0 0 30px #00d4ff; }
    
    label { color: #555 !important; font-size: 11px !important; }
    input { color: #00d4ff !important; background: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة البيانات واللغة
if 'lang' not in st.session_state: st.session_state.lang = 'AR'
if 'history' not in st.session_state: st.session_state.history = []
if 'level' not in st.session_state: st.session_state.level = 1
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'step' not in st.session_state: st.session_state.step = 'awakening'

# نصوص الواجهة
TEXTS = {
    'AR': {
        'init': 'إعداد النظام (SYSTEM SCAN)', 'id': 'معرف اللاعب', 'gen': 'الجنس', 
        'male': 'ذكر (Hunter)', 'female': 'أنثى (Huntress)', 'path': 'المسار التدريبي',
        'inj': 'مسح الإصابات (القيود)', 'arise': 'نهوض (ARISE)', 'quest': 'المهمة اليومية',
        'log': 'سجل اللاعب', 'comp': 'إتمام المهمة', 'skip': '⚠️ تخطي: ', 'alt': 'البديل: '
    },
    'EN': {
        'init': 'SYSTEM INITIALIZATION', 'id': 'PLAYER ID', 'gen': 'GENDER', 
        'male': 'MALE (Hunter)', 'female': 'FEMALE (Huntress)', 'path': 'TRAINING PATH',
        'inj': 'INJURY SCAN', 'arise': 'ARISE', 'quest': 'DAILY QUEST',
        'log': 'PLAYER LOG', 'comp': 'COMPLETE MISSION', 'skip': '⚠️ SKIP: ', 'alt': 'ALT: '
    }
}
T = TEXTS[st.session_state.lang]

# قاعدة بيانات التمارين الكاملة (PPL & Bro Split)
TRAINER_DB = {
    "PPL (Push/Pull/Legs)": {
        "Push": [
            {"AR": "بنش برس بار مستوي", "EN": "Barbell Bench Press", "i": "Shoulder", "alt": "Floor Press"},
            {"AR": "تجميع دمبل مائل علوي", "EN": "Incline DB Press", "i": "Shoulder", "alt": "Low Incline Hex"},
            {"AR": "عسكري بار واقف", "EN": "Military Press", "i": "Shoulder", "alt": "Landmine Press"},
            {"AR": "رفرفة جانبي دمبل", "EN": "Lateral Raises", "i": "Shoulder", "alt": "Cable Lateral"},
            {"AR": "تراي كابل مسطرة", "EN": "Tricep Pushdowns", "i": "Elbow", "alt": "Diamond Pushups"},
            {"AR": "تراي دمبل خلف الرأس", "EN": "Overhead Extension", "i": "Elbow", "alt": "Kickbacks"}
        ],
        "Pull": [
            {"AR": "رفعة ميتة (Deadlift)", "EN": "Deadlifts", "i": "Back", "alt": "Rack Pulls"},
            {"AR": "عقلة واسع", "EN": "Wide Pullups", "i": "Shoulder", "alt": "Lat Pulldown"},
            {"AR": "سحب بار ظهر", "EN": "Barbell Rows", "i": "Back", "alt": "T-Bar Row"},
            {"AR": "رفرفة خلفي دمبل", "EN": "Rear Delt Flys", "i": "Shoulder", "alt": "Face Pulls"},
            {"AR": "باي بار مستقيم", "EN": "Barbell Curls", "i": "Elbow", "alt": "Preacher Curls"},
            {"AR": "باي شاكوش", "EN": "Hammer Curls", "i": "Elbow", "alt": "Cable Curls"}
        ],
        "Legs": [
            {"AR": "سكوات بار خلفي", "EN": "Back Squats", "i": "Knee", "alt": "Box Squat"},
            {"AR": "ليج برس", "EN": "Leg Press", "i": "Knee", "alt": "Goblet Squat"},
            {"AR": "رفرفة رجلي أمامي", "EN": "Leg Extension", "i": "Knee", "alt": "Sissy Squat"},
            {"AR": "خلفيات ماكينة", "EN": "Hamstring Curls", "i": "Knee", "alt": "RDL"},
            {"AR": "سمانة واقف", "EN": "Standing Calf Raise", "i": "Ankle", "alt": "Seated Calf"}
        ]
    },
    "Bro Split": {
        "Chest": [{"AR": "بنش مستوي", "EN": "Flat Bench", "i": "Shoulder", "alt": "Floor Press"}, {"AR": "بنش مائل", "EN": "Incline Bench", "i": "Shoulder", "alt": "Incline DB"}],
        "Back": [{"AR": "عقلة", "EN": "Pullups", "i": "Back", "alt": "Pulldown"}, {"AR": "سحب عالي", "EN": "Lat Pulldown", "i": "Back", "alt": "Rows"}],
        "Shoulders": [{"AR": "ضغط بار", "EN": "Military Press", "i": "Shoulder", "alt": "Landmine"}, {"AR": "رفرفة", "EN": "Lateral Raise", "i": "Shoulder", "alt": "Cable"}],
        "Arms": [{"AR": "باي بار", "EN": "BB Curls", "i": "Elbow", "alt": "Dumbbell"}, {"AR": "تراي كابل", "EN": "Pushdowns", "i": "Elbow", "alt": "Dips"}]
    }
}

# تبديل اللغة
if st.sidebar.button("🌐 AR/EN"):
    st.session_state.lang = 'EN' if st.session_state.lang == 'AR' else 'AR'
    st.rerun()

# --- المرحلة الأولى: Awakening (التسجيل الكامل) ---
if st.session_state.step == 'awakening':
    st.markdown(f'<div class="system-window" style="text-align:center;"><h2>{T["init"]}</h2></div>', unsafe_allow_html=True)
    
    u_id = st.text_input(T['id'], placeholder="ADAM...")
    
    col_g, col_p = st.columns(2)
    u_gen = col_g.selectbox(T['gen'], [T['male'], T['female']])
    u_path = col_p.selectbox(T['path'], list(TRAINER_DB.keys()))
    
    u_inj = st.multiselect(T['inj'], ["Shoulder", "Back", "Knee", "Elbow", "Ankle"])
    
    col_w, col_h = st.columns(2)
    u_w = col_w.number_input("WEIGHT (KG)", value=80)
    u_h = col_h.number_input("HEIGHT (CM)", value=175)

    if st.button(T['arise']):
        if u_id:
            bmi = round(u_w / ((u_h/100)**2), 1)
            rank = "S-RANK" if 20 <= bmi <= 25 else "A-RANK"
            st.session_state.player = {"id": u_id, "gender": u_gen, "path": u_path, "inj": u_inj, "rank": rank, "bmi": bmi}
            st.session_state.step = 'status'
            st.rerun()

# --- المرحلة الثانية: Combat HUD (المدرب المدمج) ---
elif st.session_state.step == 'status':
    p = st.session_state.player
    st.markdown(f"**PLAYER:** {p['id'].upper()} | **{p['gender']}** | **LVL:** {st.session_state.level} | **{p['rank']}**")
    
    tab1, tab2 = st.tabs([T['quest'], T['log']])

    with tab1:
        zones = list(TRAINER_DB[p['path']].keys())
        target = st.selectbox("ZONE", zones)
        
        st.markdown(f"<div class='system-window'><b>MISSION: {target.upper()}</b></div>", unsafe_allow_html=True)
        
        exs = TRAINER_DB[p['path']][target]
        checks = 0
        active_exs = 0
        
        for i, ex in enumerate(exs):
            name = ex[st.session_state.lang]
            if ex['i'] in p['inj']:
                st.markdown(f"<small style='color:#ff4b4b;'>{T['skip']} {name}</small><br><small style='color:#00ffaa;'>{T['alt']} {ex['alt']}</small>", unsafe_allow_html=True)
                if st.checkbox(f"⚔️ {ex['alt']} (Safe)", key=f"alt_{i}"): checks += 1
                active_exs += 1
            else:
                if st.checkbox(f"⚔️ {name}", key=f"q_{i}"): checks += 1
                active_exs += 1
        
        if st.button(T['comp']):
            if checks == active_exs:
                st.session_state.history.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "task": target})
                st.session_state.xp += 34
                if st.session_state.xp >= 100:
                    st.session_state.level += 1
                    st.session_state.xp = 0
                st.rerun()
            else:
                st.error("المهمة لم تكتمل!")

    with tab2:
        st.markdown(f"### 📜 {T['log']}")
        for log in reversed(st.session_state.history):
            st.markdown(f"<p style='border-bottom:1px solid #111; font-size:12px;'>[{log['time']}] {log['task']} - COMPLETED</p>", unsafe_allow_html=True)

    if st.sidebar.button("TERMINATE"):
        st.session_state.step = 'awakening'
        st.rerun()
