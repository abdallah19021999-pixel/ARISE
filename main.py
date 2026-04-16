import streamlit as st

# 1. إعدادات الهوية البصرية (Void UI - No White - High Contrast)
st.set_page_config(page_title="SYSTEM", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    
    /* منع الخلفيات البيضاء نهائياً وإخفاء أزرار التحكم الرقمي */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="base-input"], div[data-testid="stMultiSelect"] {
        background-color: rgba(0, 10, 20, 0.6) !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        color: #00d4ff !important;
    }
    input { color: #00d4ff !important; background: transparent !important; }
    button[step="1"], button[step="-1"], [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] {
        display: none !important;
    }

    .system-log {
        background: rgba(0, 20, 40, 0.2);
        border-right: 3px solid #00d4ff;
        padding: 15px;
        margin-bottom: 25px;
        font-family: 'Orbitron', 'Cairo';
    }

    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron', 'Cairo';
        letter-spacing: 5px; padding: 12px !important; margin-top: 10px;
    }
    .stButton > button:hover { background: rgba(0, 212, 255, 0.1) !important; box-shadow: 0 0 25px #00d4ff; }

    header, footer {visibility: hidden !important;}
    label { color: #222 !important; font-size: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة واللغة
if 'lang' not in st.session_state: st.session_state.lang = 'AR'
if 'step' not in st.session_state: st.session_state.step = 'awakening'

# زر تبديل اللغة (Invisible UI)
if st.button("SWITCH LANGUAGE / تبديل اللغة"):
    st.session_state.lang = 'EN' if st.session_state.lang == 'AR' else 'AR'
    st.rerun()

# مصفوفة البيانات الضخمة (The Global Dictionary)
DB = {
    'AR': {
        'title': 'إشعار النظام', 'warn': '[تحذير: دخول بروتوكول الصحوة]',
        'sub': 'أدخل البيانات الحيوية لتحديد الرتبة', 'name': 'تعريف الهوية',
        'age': 'العمر', 'weight': 'الوزن', 'height': 'الطول', 'gender': 'الجنس',
        'm': 'ذكر', 'f': 'أنثى', 'inj': 'مسح الإصابات', 'split': 'نظام التدريب',
        'goal': 'الهدف', 'arise': 'نهوض (ARISE)', 'status': 'نافذة الحالة',
        'rank': 'الرتبة', 'quest': 'اختر المهمة اليومية', 'active': 'البروتوكول النشط',
        'comp': 'تأكيد إكمال المهمة', 'logout': 'إغلاق النظام',
        'splits': ["عضلة واحدة", "دفع سحب أرجل", "علوي سفلي", "جسم كامل"],
        'muscles': ["صدر", "ظهر", "أرجل", "أكتاف", "ذراع"]
    },
    'EN': {
        'title': 'SYSTEM NOTIFICATION', 'warn': '[WARNING: AWAKENING PROTOCOL ACTIVE]',
        'sub': 'INPUT BIOMETRICS TO CALCULATE RANK', 'name': 'IDENTIFICATION',
        'age': 'AGE', 'weight': 'WEIGHT', 'height': 'HEIGHT', 'gender': 'GENDER',
        'm': 'MALE', 'f': 'FEMALE', 'inj': 'INJURY SCAN', 'split': 'TRAINING SPLIT',
        'goal': 'GOAL', 'arise': 'ARISE', 'status': 'STATUS WINDOW',
        'rank': 'RANK', 'quest': 'SELECT DAILY QUEST', 'active': 'ACTIVE PROTOCOL',
        'comp': 'CONFIRM COMPLETION', 'logout': 'TERMINATE SYSTEM',
        'splits': ["BRO SPLIT", "PPL", "UPPER LOWER", "FULL BODY"],
        'muscles': ["CHEST", "BACK", "LEGS", "SHOULDERS", "ARMS"]
    }
}
L = DB[st.session_state.lang]

# --- المرحلة الأولى: Awakening ---
if st.session_state.step == 'awakening':
    st.markdown(f'<div class="system-log"><h3>{L["title"]}</h3><p>{L["warn"]}</p></div>', unsafe_allow_html=True)
    
    u_name = st.text_input(L['name'])
    c1, c2, c3 = st.columns(3)
    u_age = c1.number_input(L['age'], step=1, value=25)
    u_weight = c2.number_input(L['weight'], step=1, value=80)
    u_height = c3.number_input(L['height'], step=1, value=175)
    
    u_gender = st.selectbox(L['gender'], [L['m'], L['f']])
    u_injury = st.multiselect(L['inj'], ["SHOULDER", "BACK", "KNEE", "WRIST"], default=[])
    u_split = st.selectbox(L['split'], L['splits'])
    u_goal = st.selectbox(L['goal'], ["BULK", "CUT"])
    
    if st.button(L['arise']):
        if u_name:
            bmi = round(u_weight / ((u_height/100)**2), 1)
            rank = "S-RANK" if 22 <= bmi <= 25 else "A-RANK"
            st.session_state.player = {"name": u_name, "bmi": bmi, "goal": u_goal, "injury": u_injury, "gender": u_gender, "split": u_split, "rank": rank}
            st.session_state.step = 'dashboard'
            st.rerun()

# --- المرحلة الثانية: Status & Anatomy Map ---
elif st.session_state.step == 'dashboard':
    p = st.session_state.player
    st.markdown(f"""
        <div style='text-align:center;'>
            <p style='font-family:Orbitron; color:#00d4ff; font-size:10px; letter-spacing:8px;'>{L['status']}</p>
            <h1 style='margin:0;'>{p['name'].upper()}</h1>
            <p style='color:#444;'>{p['rank']} | {p['gender']} | BMI: {p['bmi']}</p>
        </div>
    """, unsafe_allow_html=True)

    target = st.selectbox(L['quest'], L['muscles'])

    # خريطة الجسم الاحترافية (Anatomy Logic)
    is_upper = target in ["صدر", "CHEST", "ظهر", "BACK", "أكتاف", "SHOULDERS"]
    is_lower = target in ["أرجل", "LEGS"]
    is_arms = target in ["ذراع", "ARMS"]

    st.markdown(f"""
        <div style="text-align:center; margin: 20px 0;">
            <svg width="80" height="120" viewBox="0 0 100 150">
                <circle cx="50" cy="15" r="10" fill="#111" />
                <rect x="30" y="30" width="40" height="50" fill="{'#00d4ff' if is_upper else '#111'}" rx="2" />
                <rect x="15" y="30" width="10" height="50" fill="{'#00d4ff' if is_arms or is_upper else '#111'}" rx="2" />
                <rect x="75" y="30" width="10" height="50" fill="{'#00d4ff' if is_arms or is_upper else '#111'}" rx="2" />
                <rect x="32" y="85" width="15" height="60" fill="{'#00d4ff' if is_lower else '#111'}" rx="2" />
                <rect x="53" y="85" width="15" height="60" fill="{'#00d4ff' if is_lower else '#111'}" rx="2" />
            </svg>
        </div>
    """, unsafe_allow_html=True)

    # محرك التمارين المزدوج (Dual Exercise Engine)
    exercises = {
        "CHEST": ["Bench Press", "Incline DB Press", "Cable Flys"],
        "صدر": ["بنش برس بار", "تجميع دمبل مائل", "تفتيح كابل"],
        "BACK": ["Deadlifts", "Lat Pulldowns", "Seated Rows"],
        "ظهر": ["رفعة ميتة", "سحب عالي", "سحب أرضي"],
        "LEGS": ["Squats", "Leg Press", "Leg Curls"],
        "أرجل": ["سكوات", "ليج برس", "خلفيات"]
    }
    
    current_list = exercises.get(target.upper(), ["Custom Exercise 01", "Custom Exercise 02"])
    
    st.markdown(f"<p style='font-size:12px; border-bottom: 1px solid #111;'>{L['active']}</p>", unsafe_allow_html=True)
    for ex in current_list:
        st.checkbox(ex + (" (6-8)" if p['goal'] in ["BULK", "تضخيم"] else " (12-15)"))

    if st.button(L['comp']):
        st.info("DATA RECORDED. PROTOCOL CONTINUES.")
    
    if st.button(L['logout']):
        st.session_state.step = 'awakening'
        st.rerun()
