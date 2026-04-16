import streamlit as st

# 1. نظام النيون المتقدم وتنسيق الواجهة
st.set_page_config(page_title="SYSTEM HUD", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600&family=Cairo:wght@400;600&display=swap');
    
    /* الخلفية والسواد المطلق */
    .stApp { background: #000000 !important; color: #00d4ff !important; font-family: 'Orbitron', 'Cairo', sans-serif; }
    header, footer { display: none !important; }

    /* صندوق التنبيه الاحترافي مع توهج نيون (Glow) */
    .system-notification {
        background: rgba(0, 20, 40, 0.2);
        border: 1px solid #00d4ff;
        border-radius: 2px;
        padding: 20px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.4), inset 0 0 10px rgba(0, 212, 255, 0.2);
        position: relative;
    }
    
    .system-notification h1 {
        font-size: 22px; 
        letter-spacing: 6px; 
        margin: 0; 
        color: #00d4ff; 
        text-shadow: 0 0 10px #00d4ff;
    }
    
    .warning-message {
        color: #ff00ff; 
        font-size: 12px; 
        font-weight: 500; 
        margin-top: 10px; 
        letter-spacing: 2px;
        text-shadow: 0 0 5px #ff00ff;
    }

    /* تنسيق المدخلات لتكون سوداء نيون وبدون رمادي */
    input, div[data-baseweb="input"], div[data-baseweb="select"] > div, 
    div[role="listbox"], li[role="option"], .stMultiSelect div {
        background-color: #000000 !important; 
        color: #00d4ff !important; 
        border: 1px solid #00d4ff33 !important;
        font-size: 13px !important;
    }
    
    /* إخفاء أزرار الزائد والناقص نهائياً */
    button[step="1"], [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }

    /* زر الأكشن (Arise) بتصميم زجاجي */
    .stButton > button {
        width: 100px; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron'; font-size: 12px;
        letter-spacing: 2px; margin-top: 20px; transition: 0.4s;
    }
    .stButton > button:hover { 
        background: rgba(0, 212, 255, 0.1) !important; 
        box-shadow: 0 0 15px #00d4ff;
        border-color: #ffffff !important;
    }

    /* زر تبديل اللغة (Top Right) */
    .lang-btn { position: absolute; top: -50px; right: 0; }
    
    label { color: #555 !important; font-size: 10px !important; letter-spacing: 1px; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. اللغات والأنظمة التدريبية المكثفة
if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'step' not in st.session_state: st.session_state.step = 'awakening'

U = {
    'EN': {
        'notify': 'SYSTEM NOTIFICATION', 'warn': '[WARNING: YOU HAVE BECOME A PLAYER]',
        'id': 'PLAYER NAME', 'gen': 'GENDER', 'path': 'TRAINING PATH', 'inj': 'INJURY SCAN',
        'arise': 'ARISE', 'weight': 'WEIGHT (KG)', 'height': 'HEIGHT (CM)'
    },
    'AR': {
        'notify': 'إشعار النظام', 'warn': '[تحذير: لقد أصبحت لاعباً الآن]',
        'id': 'اسم اللاعب', 'gen': 'الجنس', 'path': 'مسار التدريب', 'inj': 'مسح الإصابات',
        'arise': 'نهوض', 'weight': 'الوزن (كجم)', 'height': 'الطول (سم)'
    }
}[st.session_state.lang]

# 3. واجهة الصحوة (Awakening Phase)
if st.session_state.step == 'awakening':
    # زر اللغة في مكان احترافي
    c1, c2 = st.columns([5, 1])
    if c2.button("🌐 AR/EN"):
        st.session_state.lang = 'AR' if st.session_state.lang == 'EN' else 'EN'
        st.rerun()

    st.markdown(f"""
        <div class="system-notification">
            <h1>{U['notify']}</h1>
            <div class="warning-message">{U['warn']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # تنظيم المدخلات بشكل احترافي
    u_id = st.text_input(U['id'], placeholder="Enter Name...")
    
    col_a, col_b = st.columns(2)
    u_gen = col_a.selectbox(U['gen'], ["MALE", "FEMALE"])
    u_path = col_b.selectbox(U['path'], ["PPL (Push/Pull/Legs)", "Bro Split", "Upper/Lower"])
    
    u_inj = st.multiselect(U['inj'], ["Shoulder", "Back", "Knee", "Elbow", "Ankle"])
    
    col_c, col_d = st.columns(2)
    u_w = col_c.text_input(U['weight'], value="80")
    u_h = col_d.text_input(U['height'], value="175")

    if st.button(U['arise']):
        if u_id:
            st.session_state.player = {"id": u_id, "path": u_path, "inj": u_inj}
            st.session_state.step = 'status'
            st.rerun()

# 4. واجهة المهمات (Status Phase)
elif st.session_state.step == 'status':
    p = st.session_state.player
    st.markdown(f"<h3 style='font-size:16px;'>PLAYER: {p['id'].upper()}</h3>", unsafe_allow_html=True)
    
    # قاعدة التمارين (مدرب محترف)
    exercises = {
        "PPL (Push/Pull/Legs)": ["Bench Press", "Incline DB Press", "Military Press", "Lateral Raise", "Tricep Pushdown", "Deadlift", "Pullups", "Barbell Row", "Bicep Curls", "Back Squat", "Leg Press", "Leg Curls"],
        "Bro Split": ["Flat Bench", "Incline Bench", "Cable Flys", "Lat Pulldown", "Seated Row", "Deadlift", "Shoulder Press", "Lateral Raise", "Bicep Curls", "Tricep Ext"],
        "Upper/Lower": ["Bench Press", "Lat Pulldown", "Shoulder Press", "Barbell Row", "Squat", "RDL", "Leg Press", "Calf Raise"]
    }
    
    st.markdown("---")
    for ex in exercises[p['path']]:
        st.checkbox(f"⚔️ {ex}")

    if st.sidebar.button("TERMINATE"):
        st.session_state.step = 'awakening'
        st.rerun()
