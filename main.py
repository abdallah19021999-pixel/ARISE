import streamlit as st
from datetime import datetime

# 1. تدمير شامل للخلفيات البيضاء (Deep CSS Injection)
st.set_page_config(page_title="SYSTEM HUD", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Cairo:wght@400;600;700&display=swap');
    
    /* السواد المطلق */
    .stApp { background: #000000 !important; color: #00d4ff !important; font-family: 'Cairo', sans-serif; }
    header, footer { display: none !important; }

    /* إجبار كل أنواع الخانات بلا استثناء على السواد */
    input, div[data-baseweb="input"], div[data-baseweb="select"] > div, 
    div[role="listbox"], li[role="option"], .stMultiSelect div {
        background-color: #000000 !important; 
        color: #00d4ff !important; 
        border: 1px solid #00d4ff66 !important;
        box-shadow: none !important;
    }
    
    /* معالجة خاصة لخانة الوزن والطول لمنع الرمادي */
    .stTextInput input { background-color: #000000 !important; }

    /* إشعار النظام الأيقوني */
    .system-notification {
        background: transparent; border: 2px solid #00d4ff;
        padding: 30px; text-align: center; margin-bottom: 30px;
        box-shadow: inset 0 0 15px rgba(0, 212, 255, 0.2);
    }
    .system-notification h1 { font-family: 'Orbitron'; font-size: 26px; color: #00d4ff; margin: 0; }
    .warning-text { color: #ff00ff; font-family: 'Orbitron'; font-size: 14px; margin-top: 8px; font-weight: bold; }

    /* الأزرار النيون */
    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 3px;
        padding: 12px !important; transition: 0.3s;
    }
    .stButton > button:hover { background: rgba(0, 212, 255, 0.1) !important; box-shadow: 0 0 20px #00d4ff; }
    
    label { color: #444 !important; font-size: 11px !important; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة واللغة
if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'step' not in st.session_state: st.session_state.step = 'awakening'

# زر تبديل اللغة الأنيق
col_sp, col_btn = st.columns([5, 1])
if col_btn.button("🌐 AR/EN"):
    st.session_state.lang = 'AR' if st.session_state.lang == 'EN' else 'EN'
    st.rerun()

U = {
    'EN': {
        'notify': 'SYSTEM NOTIFICATION', 'warn': '[WARNING: YOU HAVE BECOME A PLAYER]',
        'id': 'PLAYER NAME', 'gen': 'GENDER', 'path': 'TRAINING PATH', 'inj': 'INJURY SCAN',
        'arise': 'ARISE', 'quest': 'DAILY QUEST', 'comp': 'COLLECT REWARD'
    },
    'AR': {
        'notify': 'إشعار النظام', 'warn': '[تحذير: لقد أصبحت لاعباً الآن]',
        'id': 'اسم اللاعب', 'gen': 'الجنس', 'path': 'مسار التدريب', 'inj': 'مسح الإصابات',
        'arise': 'نهوض', 'quest': 'المهمة اليومية', 'comp': 'تحصيل المكافأة'
    }
}[st.session_state.lang]

# 3. قاعدة تمارين "المدرب الشامل" (Pro Multi-Path)
DB = {
    "PPL (Push/Pull/Legs)": {
        "Push": [{"AR": "بنش برس بار", "EN": "BB Bench Press", "i": "Shoulder"}, {"AR": "تجميع دمبل مائل", "EN": "Incline DB Press", "i": "Shoulder"}, {"AR": "عسكري بار", "EN": "Military Press", "i": "Shoulder"}, {"AR": "رفرفة كابل", "EN": "Lateral Raise", "i": "Shoulder"}, {"AR": "تراي كابل", "EN": "Pushdowns", "i": "Elbow"}, {"AR": "تراي خلفي", "EN": "Overhead Ext", "i": "Elbow"}],
        "Pull": [{"AR": "رفعة ميتة", "EN": "Deadlift", "i": "Back"}, {"AR": "عقلة", "EN": "Pullups", "i": "Back"}, {"AR": "سحب بار", "EN": "BB Row", "i": "Back"}, {"AR": "باي بار", "EN": "BB Curls", "i": "Elbow"}, {"AR": "باي شاكوش", "EN": "Hammer Curls", "i": "Elbow"}],
        "Legs": [{"AR": "سكوات", "EN": "Squat", "i": "Knee"}, {"AR": "ليج برس", "EN": "Leg Press", "i": "Knee"}, {"AR": "خلفيات", "EN": "Leg Curls", "i": "Knee"}, {"AR": "سمانة", "EN": "Calf Raise", "i": "Ankle"}]
    },
    "Bro Split (PRO)": {
        "Chest": [{"AR": "بنش مستوي", "EN": "Flat Bench", "i": "Shoulder"}, {"AR": "بنش مائل", "EN": "Incline Bench", "i": "Shoulder"}, {"AR": "كابل كروس", "EN": "Cable Flys", "i": "Shoulder"}, {"AR": "تجميع دمبل", "EN": "DB Press", "i": "Shoulder"}],
        "Back": [{"AR": "سحب عالي", "EN": "Lat Pulldown", "i": "Back"}, {"AR": "سحب أرضي", "EN": "Seated Row", "i": "Back"}, {"AR": "منشار", "EN": "One Arm Row", "i": "Back"}, {"AR": "قطنية", "EN": "Hyperextension", "i": "Back"}]
    },
    "Upper/Lower Body": {
        "Upper": [{"AR": "بنش برس", "EN": "Bench Press", "i": "Shoulder"}, {"AR": "سحب عالي", "EN": "Lat Pulldown", "i": "Back"}, {"AR": "ضغط كتف", "EN": "Shoulder Press", "i": "Shoulder"}],
        "Lower": [{"AR": "سكوات", "EN": "Squat", "i": "Knee"}, {"AR": "رفعة ميتة", "EN": "Deadlift", "i": "Back"}, {"AR": "طعن", "EN": "Lunges", "i": "Knee"}]
    }
}

# --- Phase 1: Awakening ---
if st.session_state.step == 'awakening':
    st.markdown(f'<div class="system-notification"><h1>{U["notify"]}</h1><p class="warning-text">{U["warn"]}</p></div>', unsafe_allow_html=True)
    
    u_id = st.text_input(U['id'], placeholder="ADAM...")
    col1, col2 = st.columns(2)
    u_gen = col1.selectbox(U['gen'], ["MALE (Hunter)", "FEMALE (Huntress)"])
    u_path = col2.selectbox(U['path'], list(DB.keys()))
    
    u_inj = st.multiselect(U['inj'], ["Shoulder", "Back", "Knee", "Elbow", "Ankle"])
    
    # تحويل الوزن والطول لنص لمنع اللون الرمادي
    cw, ch = st.columns(2)
    u_w = cw.text_input("WEIGHT (KG)", value="80")
    u_h = ch.text_input("HEIGHT (CM)", value="175")

    if st.button(U['arise']):
        if u_id:
            st.session_state.player = {"id": u_id, "path": u_path, "inj": u_inj}
            st.session_state.step = 'status'
            st.rerun()

# --- Phase 2: Combat HUD ---
elif st.session_state.step == 'status':
    p = st.session_state.player
    st.markdown(f"**PLAYER:** {p['id'].upper()} | **PATH:** {p['path']}")
    
    zone = st.selectbox("MISSION ZONE", list(DB[p['path']].keys()))
    st.markdown(f"### ⚔️ {U['quest']}")
    
    for i, ex in enumerate(DB[p['path']][zone]):
        name = ex[st.session_state.lang]
        if ex['i'] in p['inj']:
            st.markdown(f"<small style='color:#ff0055;'>❌ [SKIPPED] {name}</small>", unsafe_allow_html=True)
        else:
            st.checkbox(f"⚔️ {name}", key=f"ex_{i}")
    
    if st.button(U['comp']):
        st.success("MISSION SUCCESS.")

    if st.sidebar.button("TERMINATE"):
        st.session_state.step = 'awakening'
        st.rerun()
