import streamlit as st
from datetime import datetime

# 1. تدمير اللون الأبيض (Void Black HUD)
st.set_page_config(page_title="SYSTEM HUD", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    header, footer, [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }

    /* تعديل الـ Tabs والـ SelectBoxes للسواد التام */
    .stTabs [data-baseweb="tab-list"], .stTabs [data-baseweb="tab"], div[data-baseweb="select"] > div, div[data-baseweb="input"] {
        background-color: #000 !important; color: #00d4ff !important; border-color: #00d4ff33 !important;
    }
    .stTabs [aria-selected="true"] { border-bottom: 2px solid #ff00ff !important; }

    .system-window {
        background: rgba(0, 15, 30, 0.9); border: 2px solid #00d4ff;
        padding: 20px; border-radius: 2px; margin-bottom: 20px;
    }
    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 2px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة واللغة
if 'lang' not in st.session_state: st.session_state.lang = 'AR'
if 'step' not in st.session_state: st.session_state.step = 'awakening'
if 'history' not in st.session_state: st.session_state.history = []

# أرشيف التمارين الكامل (6-7 تمارين لكل حصة)
FULL_TRAINER_DB = {
    "PPL (Push/Pull/Legs)": {
        "Push": [
            {"AR": "بنش برس بار مستوي", "EN": "Barbell Bench Press", "i": "Shoulder", "alt": "Floor Press"},
            {"AR": "تجميع دمبل مائل علوي", "EN": "Incline DB Press", "i": "Shoulder", "alt": "Low Incline Hex"},
            {"AR": "عسكري بار واقف (أكتاف)", "EN": "Military Press", "i": "Shoulder", "alt": "Landmine Press"},
            {"AR": "غطس متوازي (صدر)", "EN": "Chest Dips", "i": "Shoulder", "alt": "Pushups"},
            {"AR": "رفرفة جانبي دمبل", "EN": "Lateral Raises", "i": "Shoulder", "alt": "Cable Lateral"},
            {"AR": "تراي كابل مسطرة", "EN": "Tricep Pushdowns", "i": "Elbow", "alt": "Diamond Pushups"},
            {"AR": "تراي دمبل خلف الرأس", "EN": "Overhead Extension", "i": "Elbow", "alt": "Kickbacks"}
        ],
        "Pull": [
            {"AR": "رفعة ميتة (Deadlift)", "EN": "Deadlifts", "i": "Back", "alt": "Rack Pulls"},
            {"AR": "عقلة واسع", "EN": "Wide Pullups", "i": "Shoulder", "alt": "Lat Pulldown"},
            {"AR": "سحب بار ظهر (T-Bar)", "EN": "T-Bar Rows", "i": "Back", "alt": "Chest Supported Row"},
            {"AR": "سحب أرضي ضيق", "EN": "Seated Rows", "i": "Back", "alt": "Single Arm Row"},
            {"AR": "رفرفة خلفي دمبل", "EN": "Rear Delt Flys", "i": "Shoulder", "alt": "Face Pulls"},
            {"AR": "باي بار مستقيم", "EN": "Barbell Curls", "i": "Elbow", "alt": "Preacher Curls"},
            {"AR": "باي شاكوش (Hammer)", "EN": "Hammer Curls", "i": "Elbow", "alt": "Cable Curls"}
        ],
        "Legs": [
            {"AR": "سكوات بار خلفي", "EN": "Back Squats", "i": "Knee", "alt": "Box Squat"},
            {"AR": "ليج برس", "EN": "Leg Press", "i": "Knee", "alt": "Goblet Squat"},
            {"AR": "طعن دمبل (Lunges)", "EN": "Walking Lunges", "i": "Knee", "alt": "Split Squat"},
            {"AR": "رفرفة رجلي أمامي", "EN": "Leg Extension", "i": "Knee", "alt": "Sissy Squat"},
            {"AR": "خلفيات ماكينة نائم", "EN": "Hamstring Curls", "i": "Knee", "alt": "RDL"},
            {"AR": "سمانة واقف", "EN": "Standing Calf Raise", "i": "Ankle", "alt": "Seated Calf"}
        ]
    },
    "Bro Split (Single Muscle)": {
        "Chest": [{"AR": "بنش مستوي", "EN": "Flat Bench", "i": "Shoulder", "alt": "Pushups"}, {"AR": "بنش مائل", "EN": "Incline Bench", "i": "Shoulder", "alt": "Incline DB"}, {"AR": "كابل كروس", "EN": "Cable Cross", "i": "Shoulder", "alt": "Flys"}],
        "Back": [{"AR": "عقلة", "EN": "Pullups", "i": "Back", "alt": "Pulldown"}, {"AR": "منشار", "EN": "DB Row", "i": "Back", "alt": "T-Bar"}, {"AR": "سحب عالي", "EN": "Lat Pulldown", "i": "Back", "alt": "Rows"}]
        # ... يمكن إضافة الباقي بنفس النمط
    }
}

# القاموس
T = {
    'AR': {'init': 'إعداد النظام', 'arise': 'نهوض', 'quest': 'المهمة', 'log': 'السجل', 'skip': '⚠️ تخطي: ', 'alt': 'البديل: '},
    'EN': {'init': 'SYSTEM INIT', 'arise': 'ARISE', 'quest': 'QUEST', 'log': 'LOG', 'skip': '⚠️ SKIP: ', 'alt': 'ALT: '}
}[st.session_state.lang]

if st.sidebar.button("🌐 AR/EN"):
    st.session_state.lang = 'EN' if st.session_state.lang == 'AR' else 'AR'
    st.rerun()

# --- المرحلة الأولى: Awakening ---
if st.session_state.step == 'awakening':
    st.markdown(f'<div class="system-window"><h2>{T["init"]}</h2></div>', unsafe_allow_html=True)
    u_id = st.text_input("PLAYER ID")
    u_path = st.selectbox("PATH", list(FULL_TRAINER_DB.keys()))
    u_inj = st.multiselect("INJURIES", ["Shoulder", "Back", "Knee", "Elbow", "Ankle"])
    if st.button(T['arise']):
        if u_id:
            st.session_state.player = {"id": u_id, "path": u_path, "inj": u_inj}
            st.session_state.step = 'status'
            st.rerun()

# --- المرحلة الثانية: Status ---
elif st.session_state.step == 'status':
    p = st.session_state.player
    st.markdown(f"**PLAYER:** {p['id'].upper()} | **PATH:** {p['path']}")
    
    tab1, tab2 = st.tabs([T['quest'], T['log']])
    
    with tab1:
        zones = list(FULL_TRAINER_DB[p['path']].keys())
        target = st.selectbox("ZONE", zones)
        
        exs = FULL_TRAINER_DB[p['path']][target]
        for i, ex in enumerate(exs):
            ex_name = ex[st.session_state.lang]
            if ex['i'] in p['inj']:
                st.markdown(f"<small style='color:#ff4b4b;'>{T['skip']} {ex_name} ({T['alt']} {ex['alt']})</small>", unsafe_allow_html=True)
            else:
                st.checkbox(f"⚔️ {ex_name}", key=f"q_{i}")
        
        if st.button("DONE"):
            st.session_state.history.append({"time": datetime.now().strftime("%H:%M"), "task": target})
            st.rerun()

    if st.sidebar.button("TERMINATE"):
        st.session_state.step = 'awakening'
        st.rerun()
