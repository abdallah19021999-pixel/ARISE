import streamlit as st
from datetime import datetime

# 1. واجهة الظلام المطلق (The Clean Void HUD)
st.set_page_config(page_title="SYSTEM HUD", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Cairo:wght@400;600;700&display=swap');
    
    .stApp { background: #000000 !important; color: #00d4ff !important; font-family: 'Cairo', sans-serif; }
    header, footer { display: none !important; }

    /* إخفاء أزرار الزائد والناقص تماماً */
    [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }
    input[type=number] { -moz-appearance: textfield; }
    input[type=number]::-webkit-inner-spin-button, input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }

    /* تصميم إشعار النظام (SYSTEM NOTIFICATION) - متناسق */
    .system-notification {
        background: transparent; border: 2px solid #00d4ff;
        padding: 25px; text-align: center; margin-bottom: 25px;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
    }
    .system-notification h1 { font-family: 'Orbitron'; font-size: 24px; color: #00d4ff; margin: 0; }
    .warning-text { color: #ff00ff; font-family: 'Orbitron'; font-size: 14px; margin-top: 5px; letter-spacing: 1px; }

    /* صناديق الإدخال - سواد نيون احترافي */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[role="listbox"], li[role="option"] {
        background-color: #000 !important; color: #00d4ff !important; 
        border: 1px solid #00d4ff55 !important; border-radius: 4px !important;
    }
    
    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 3px;
        padding: 12px !important; text-transform: uppercase; border-radius: 2px;
    }
    .stButton > button:hover { background: rgba(0, 212, 255, 0.1) !important; box-shadow: 0 0 20px #00d4ff; }
    
    label { color: #555 !important; font-size: 11px !important; text-transform: uppercase; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic & Language
if 'lang' not in st.session_state: st.session_state.lang = 'AR'
if 'step' not in st.session_state: st.session_state.step = 'awakening'

col_l1, col_l2 = st.columns([5, 1])
if col_l2.button("🌐 AR/EN"):
    st.session_state.lang = 'EN' if st.session_state.lang == 'AR' else 'AR'
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

# 3. قاعدة تمارين "مدرب محترف" (Pro Routines)
DB = {
    "PPL (Push/Pull/Legs)": {
        "Push (Chest/Shoulders/Triceps)": [
            {"AR": "بنش برس بار مستوي", "EN": "Barbell Bench Press", "i": "Shoulder"},
            {"AR": "تجميع دمبل مائل علوي", "EN": "Incline DB Press", "i": "Shoulder"},
            {"AR": "غطس متوازي (صدر)", "EN": "Chest Dips", "i": "Shoulder"},
            {"AR": "عسكري بار واقف", "EN": "Military Press", "i": "Shoulder"},
            {"AR": "رفرفة جانبي كابل", "EN": "Cable Lateral Raise", "i": "Shoulder"},
            {"AR": "تراي كابل مسطرة", "EN": "Tricep Pushdowns", "i": "Elbow"},
            {"AR": "تراي دمبل خلف الرأس", "EN": "Overhead Extension", "i": "Elbow"}
        ],
        "Pull (Back/Biceps/Rear Delts)": [
            {"AR": "رفعة ميتة (Deadlift)", "EN": "Deadlifts", "i": "Back"},
            {"AR": "عقلة واسع (Pullups)", "EN": "Wide Pullups", "i": "Shoulder"},
            {"AR": "سحب بار ظهر (Rows)", "EN": "Barbell Rows", "i": "Back"},
            {"AR": "سحب أرضي ضيق", "EN": "Seated Rows", "i": "Back"},
            {"AR": "رفرفة خلفي دمبل", "EN": "Rear Delt Flys", "i": "Shoulder"},
            {"AR": "مرجحة باي بار مستقيم", "EN": "Barbell Curls", "i": "Elbow"},
            {"AR": "باي شاكوش", "EN": "Hammer Curls", "i": "Elbow"}
        ],
        "Legs (Quads/Hams/Calves)": [
            {"AR": "سكوات بار خلفي", "EN": "Back Squats", "i": "Knee"},
            {"AR": "ليج برس", "EN": "Leg Press", "i": "Knee"},
            {"AR": "طعن دمبل (Lunges)", "EN": "Walking Lunges", "i": "Knee"},
            {"AR": "رفرفة رجلي أمامي", "EN": "Leg Extension", "i": "Knee"},
            {"AR": "خلفيات ماكينة نائم", "EN": "Hamstring Curls", "i": "Knee"},
            {"AR": "سمانة واقف", "EN": "Standing Calf Raise", "i": "Ankle"}
        ]
    },
    "Bro Split (Single Muscle)": {
        "Chest": [{"AR": "بنش بار مستوي", "EN": "Flat Bench", "i": "Shoulder"}, {"AR": "بنش مائل", "EN": "Incline Bench", "i": "Shoulder"}, {"AR": "تجميع دمبل", "EN": "DB Press", "i": "Shoulder"}, {"AR": "كابل كروس", "EN": "Cable Flys", "i": "Shoulder"}, {"AR": "تفتيح دمبل", "EN": "DB Flys", "i": "Shoulder"}],
        "Back": [{"AR": "عقلة", "EN": "Pullups", "i": "Back"}, {"AR": "سحب عالي", "EN": "Lat Pulldown", "i": "Back"}, {"AR": "منشار دمبل", "EN": "DB Row", "i": "Back"}, {"AR": "سحب أرضي", "EN": "Seated Row", "i": "Back"}, {"AR": "قطنية", "EN": "Back Extension", "i": "Back"}]
        # يمكن إضافة الباقي بنفس الكثافة
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
    
    cw, ch = st.columns(2)
    u_w = cw.number_input("WEIGHT (KG)", value=80)
    u_h = ch.number_input("HEIGHT (CM)", value=175)

    if st.button(U['arise']):
        if u_id:
            st.session_state.player = {"id": u_id, "path": u_path, "inj": u_inj, "rank": "S-RANK"}
            st.session_state.step = 'status'
            st.rerun()

# --- Phase 2: Combat HUD ---
elif st.session_state.step == 'status':
    p = st.session_state.player
    st.markdown(f"**PLAYER:** {p['id'].upper()} | **RANK:** {p['rank']}")
    
    zone = st.selectbox("MISSION ZONE", list(DB[p['path']].keys()))
    st.markdown(f"### ⚔️ {U['quest']}")
    
    for i, ex in enumerate(DB[p['path']][zone]):
        name = ex[st.session_state.lang]
        if ex['i'] in p['inj']:
            st.markdown(f"<small style='color:#ff0055;'>❌ [INJURY LIMIT] {name}</small>", unsafe_allow_html=True)
        else:
            st.checkbox(f"⚔️ {name}", key=f"ex_{i}")
    
    if st.button(U['comp']):
        st.success("MISSION COMPLETE. STATUS UPDATED.")

    if st.sidebar.button("TERMINATE"):
        st.session_state.step = 'awakening'
        st.rerun()
