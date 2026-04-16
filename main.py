import streamlit as st
from datetime import datetime

# 1. الواجهة المظلمة المطلقة وتدمير الزوائد (True HUD)
st.set_page_config(page_title="THE SYSTEM", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    header, footer { display: none !important; }

    /* إخفاء أزرار الزائد والناقص نهائياً */
    button[step="1"], button[aria-label="Step up"], button[aria-label="Step down"] { display: none !important; }
    div[data-testid="stNumberInputStepUp"], div[data-testid="stNumberInputStepDown"] { display: none !important; }

    /* إجبار الخانات على السواد المطلق */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[role="listbox"], 
    li[role="option"], input, .stNumberInput div {
        background-color: #000000 !important; 
        color: #00d4ff !important; 
        border: 1px solid #00d4ff66 !important;
    }
    
    .system-notification {
        background: transparent; border: 2px solid #00d4ff;
        padding: 30px; text-align: center; margin-bottom: 20px;
        box-shadow: inset 0 0 15px rgba(0, 212, 255, 0.2);
    }
    
    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 3px;
    }
    .stButton > button:hover { background: rgba(0, 212, 255, 0.1) !important; box-shadow: 0 0 20px #00d4ff; }
    
    .quest-item { background: rgba(0, 212, 255, 0.05); padding: 10px; border-radius: 5px; margin: 5px 0; border: 1px solid #00d4ff22; }
    label { color: #444 !important; font-size: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة واللغة
if 'lang' not in st.session_state: st.session_state.lang = 'AR'
if 'step' not in st.session_state: st.session_state.step = 'awakening'
if 'history' not in st.session_state: st.session_state.history = []

# تبديل اللغة (زرار واضح في القمة)
col_l1, col_l2 = st.columns([4, 1])
if col_l2.button("🌐 AR/EN"):
    st.session_state.lang = 'EN' if st.session_state.lang == 'AR' else 'AR'
    st.rerun()

# القاموس
UI = {
    'EN': {
        'notify': 'SYSTEM NOTIFICATION', 'warn': '[WARNING: YOU HAVE BECOME A PLAYER]',
        'id': 'PLAYER ID', 'gen': 'GENDER', 'path': 'TRAINING PATH', 'inj': 'INJURY SCAN',
        'arise': 'ARISE', 'quest': 'DAILY QUEST', 'comp': 'COLLECT REWARD'
    },
    'AR': {
        'notify': 'إشعار النظام', 'warn': '[تحذير: لقد أصبحت لاعباً الآن]',
        'id': 'معرف اللاعب', 'gen': 'الجنس', 'path': 'المسار التدريبي', 'inj': 'مسح الإصابات',
        'arise': 'نهوض', 'quest': 'المهمة اليومية', 'comp': 'تحصيل المكافأة'
    }
}
U = UI[st.session_state.lang]

# قاعدة التمارين الكاملة (6 تمارين لكل حصة)
DB = {
    "PPL (Push/Pull/Legs)": {
        "Push (Chest/Shoulders/Triceps)": [
            {"AR": "بنش برس بار مستوي", "EN": "Barbell Bench Press", "i": "Shoulder", "alt": "Floor Press"},
            {"AR": "تجميع دمبل مائل", "EN": "Incline DB Press", "i": "Shoulder", "alt": "Hex Press"},
            {"AR": "عسكري بار واقف", "EN": "Military Press", "i": "Shoulder", "alt": "Landmine Press"},
            {"AR": "رفرفة جانبي كابل", "EN": "Cable Lateral Raise", "i": "Shoulder", "alt": "Dumbbell Lateral"},
            {"AR": "تراي كابل مسطرة", "EN": "Tricep Pushdowns", "i": "Elbow", "alt": "Diamond Pushups"},
            {"AR": "تراي دمبل خلف الرأس", "EN": "Overhead Extension", "i": "Elbow", "alt": "Kickbacks"}
        ],
        "Pull (Back/Biceps/Rear Delts)": [
            {"AR": "رفعة ميتة (Deadlift)", "EN": "Deadlifts", "i": "Back", "alt": "Rack Pulls"},
            {"AR": "عقلة واسع", "EN": "Wide Pullups", "i": "Shoulder", "alt": "Lat Pulldown"},
            {"AR": "سحب أرضي ضيق", "EN": "Seated Rows", "i": "Back", "alt": "One Arm Row"},
            {"AR": "مرجحة باي بار مستقيم", "EN": "Barbell Curls", "i": "Elbow", "alt": "Hammer Curls"},
            {"AR": "باي شاكوش", "EN": "Hammer Curls", "i": "Elbow", "alt": "Cable Curls"},
            {"AR": "رفرفة خلفي دمبل", "EN": "Rear Delt Flys", "i": "Shoulder", "alt": "Face Pulls"}
        ],
        "Legs (Quads/Hams/Calves)": [
            {"AR": "سكوات بار خلفي", "EN": "Back Squats", "i": "Knee", "alt": "Box Squat"},
            {"AR": "ليج برس", "EN": "Leg Press", "i": "Knee", "alt": "Goblet Squat"},
            {"AR": "خلفيات ماكينة", "EN": "Hamstring Curls", "i": "Knee", "alt": "RDL"},
            {"AR": "سمانة واقف", "EN": "Standing Calf Raise", "i": "Ankle", "alt": "Seated Calf"}
        ]
    }
}

# --- المرحلة الأولى: Awakening ---
if st.session_state.step == 'awakening':
    st.markdown(f'<div class="system-notification"><h1>{U["notify"]}</h1><p>{U["warn"]}</p></div>', unsafe_allow_html=True)
    
    u_id = st.text_input(U['id'], placeholder="ADAM...")
    col1, col2 = st.columns(2)
    u_gen = col1.selectbox(U['gen'], ["MALE (Hunter)", "FEMALE (Huntress)"])
    u_path = col2.selectbox(U['path'], list(DB.keys()))
    
    u_inj = st.multiselect(U['inj'], ["Shoulder", "Back", "Knee", "Elbow", "Ankle"])
    
    cw, ch = st.columns(2)
    u_w = cw.number_input("WEIGHT (KG)", min_value=10, max_value=200, value=80)
    u_h = ch.number_input("HEIGHT (CM)", min_value=100, max_value=250, value=175)

    if st.button(U['arise']):
        if u_id:
            st.session_state.player = {"id": u_id, "path": u_path, "inj": u_inj, "rank": "S-RANK"}
            st.session_state.step = 'status'
            st.rerun()

# --- المرحلة الثانية: Main HUD ---
elif st.session_state.step == 'status':
    p = st.session_state.player
    st.markdown(f"**PLAYER:** {p['id'].upper()} | **RANK:** {p['rank']}")
    
    st.markdown(f"### ⚔️ {U['quest']}")
    target = st.selectbox("MISSION ZONE", list(DB[p['path']].keys()))
    
    exs = DB[p['path']][target]
    for i, ex in enumerate(exs):
        name = ex[st.session_state.lang]
        with st.container():
            if ex['i'] in p['inj']:
                st.markdown(f"<div class='quest-item' style='border-color:#ff0055;'>❌ {name} <br> <small style='color:#00ffaa;'>ALT: {ex['alt']}</small></div>", unsafe_allow_html=True)
            else:
                st.checkbox(f"⚔️ {name}", key=f"ex_{i}")
    
    if st.button(U['comp']):
        st.success("REWARD COLLECTED!")
        st.session_state.history.append(target)

    if st.sidebar.button("TERMINATE"):
        st.session_state.step = 'awakening'
        st.rerun()
