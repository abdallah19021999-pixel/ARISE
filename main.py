import streamlit as st

# 1. الهوية البصرية (Absolute Monarch Dark Mode)
st.set_page_config(page_title="SYSTEM", layout="centered")

# CSS لمنع الأبيض تماماً وإخفاء أزرار الزائد/الناقص
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    
    /* منع الخلفيات البيضاء في كل العناصر */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="base-input"], div[data-testid="stMultiSelect"] {
        background-color: rgba(0, 20, 40, 0.4) !important;
        border: 1px solid rgba(0, 212, 255, 0.1) !important;
        color: #00d4ff !important;
    }
    input { color: #00d4ff !important; background: transparent !important; }
    
    /* إخفاء أزرار الزائد والناقص نهائياً */
    button[step="1"], button[step="-1"], [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] {
        display: none !important;
    }

    .system-card {
        background: rgba(0, 30, 60, 0.15);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 212, 255, 0.15);
        padding: 25px;
        text-align: center;
        border-radius: 2px;
        margin-bottom: 30px;
    }

    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron', 'Cairo';
        padding: 15px !important; margin-top: 20px; text-transform: uppercase;
    }
    .stButton > button:hover { background: rgba(0, 212, 255, 0.1) !important; box-shadow: 0 0 30px #00d4ff; }

    header, footer {visibility: hidden !important;}
    label { color: #444 !important; font-family: 'Orbitron'; font-size: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة اللغة والحالة
if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'step' not in st.session_state: st.session_state.step = 'awakening'

# مفتاح تبديل اللغة في الأعلى
col_l, col_r = st.columns([8, 2])
if col_r.button("العربية / EN"):
    st.session_state.lang = 'AR' if st.session_state.lang == 'EN' else 'EN'
    st.rerun()

# قاموس المصطلحات (Translation Dictionary)
T = {
    'EN': {
        'title': 'SYSTEM NOTIFICATION', 'warn': '[WARNING: YOU ARE ENTERING THE AWAKENING SYSTEM]',
        'sub': 'ENTER DATA TO DETERMINE YOUR RANK', 'name': 'PLAYER IDENTIFICATION',
        'age': 'AGE', 'weight': 'WEIGHT (KG)', 'height': 'HEIGHT (CM)', 'gender': 'GENDER',
        'male': 'MALE', 'female': 'FEMALE', 'injury': 'INJURY SCAN', 'split': 'TRAINING PROTOCOL',
        'goal': 'OBJECTIVE', 'arise': 'ARISE', 'status': 'STATUS WINDOW', 'rank': 'RANK',
        'quest': 'SELECT DAILY QUEST ZONE', 'active': 'ACTIVE QUESTS', 'complete': 'COMPLETE QUEST',
        'logout': 'LOGOUT', 'msg': 'Quest Completed! Take your rest, Hunter.',
        'parts': ["BRO SPLIT", "PPL", "UPPER LOWER", "FULL BODY"]
    },
    'AR': {
        'title': 'إشعار النظام', 'warn': '[تحذير: أنت على وشك الدخول إلى نظام الصحوة]',
        'sub': 'أدخل بياناتك لتحديد رتبتك كلاعب', 'name': 'تعريف اللاعب',
        'age': 'العمر', 'weight': 'الوزن (كجم)', 'height': 'الطول (سم)', 'gender': 'الجنس',
        'male': 'ذكر', 'female': 'أنثى', 'injury': 'مسح الإصابات', 'split': 'نظام التدريب',
        'goal': 'هدف اللاعب', 'arise': 'الاستيقاظ', 'status': 'نافذة الحالة', 'rank': 'الرتبة',
        'quest': 'اختر منطقة المهمة اليومية', 'active': 'المهمات النشطة', 'complete': 'إكمال المهمة',
        'logout': 'تسجيل الخروج', 'msg': 'تمت المهمة! خذ قسطاً من الراحة أيها الصياد.',
        'parts': ["عضلة واحدة", "دفع سحب أرجل", "علوي سفلي", "جسم كامل"]
    }
}
L = T[st.session_state.lang]

# --- المرحلة الأولى: Awakening ---
if st.session_state.step == 'awakening':
    st.markdown(f"""
        <div class="system-card">
            <h2 style="font-family:Orbitron; letter-spacing:5px; margin:0;">{L['title']}</h2>
            <div style="width: 50px; height: 1px; background: #00d4ff; margin: 15px auto; opacity: 0.5;"></div>
            <p style="color:#666; font-size:12px;">{L['warn']}</p>
            <p style="color:#00d4ff; font-size:16px;">{L['sub']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    u_name = st.text_input(L['name'], placeholder="...")
    c1, c2, c3 = st.columns(3)
    u_age = c1.number_input(L['age'], step=1, value=25)
    u_weight = c2.number_input(L['weight'], step=1, value=80)
    u_height = c3.number_input(L['height'], step=1, value=175)
    
    u_gender = st.selectbox(L['gender'], [L['male'], L['female']])
    u_injury = st.multiselect(L['injury'], ["NONE", "SHOULDER", "BACK", "KNEE", "WRIST"], default=["NONE"])
    u_split = st.selectbox(L['split'], L['parts'])
    u_goal = st.selectbox(L['goal'], ["BULK", "CUT"])
    
    if st.button(L['arise']):
        if u_name:
            bmi = round(u_weight / ((u_height/100)**2), 1)
            st.session_state.player = {"name": u_name, "bmi": bmi, "goal": u_goal, "injury": u_injury, "gender": u_gender, "split": u_split}
            st.session_state.step = 'dashboard'
            st.rerun()

# --- المرحلة الثانية: Status Window ---
elif st.session_state.step == 'dashboard':
    p = st.session_state.player
    st.markdown(f"""
        <div style='text-align:center; margin-bottom:30px;'>
            <p style='font-family:Orbitron; color:#00d4ff; font-size:10px; letter-spacing:10px;'>{L['status']}</p>
            <h1 style='font-family:Orbitron; font-size:40px; margin:0;'>{p['name'].upper()}</h1>
            <p style='color:#333; font-size:12px;'>BMI: {p['bmi']} | {p['gender']} | {p['split']}</p>
        </div>
    """, unsafe_allow_html=True)

    # نظام خريطة الجسم والتمارين (مختصر للعرض)
    target = st.selectbox(L['quest'], ["CHEST", "BACK", "LEGS", "ARMS"])
    
    # رسمة الجسم التفاعلية
    st.markdown(f"""
        <div style="text-align:center; margin-bottom:20px;">
            <svg width="60" height="100" viewBox="0 0 100 150">
                <rect x="30" y="20" width="40" height="40" fill="{'#00d4ff' if target in ['CHEST','BACK'] else '#111'}" />
                <rect x="30" y="65" width="40" height="60" fill="{'#00d4ff' if target == 'LEGS' else '#111'}" />
                <rect x="15" y="25" width="10" height="45" fill="{'#00d4ff' if target == 'ARMS' else '#111'}" />
                <rect x="75" y="25" width="10" height="45" fill="{'#00d4ff' if target == 'ARMS' else '#111'}" />
            </svg>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<p style='font-size:12px; letter-spacing:3px;'>{L['active']}</p>", unsafe_allow_html=True)
    st.checkbox(f"{target} Exercise 01")
    st.checkbox(f"{target} Exercise 02")

    if st.button(L['complete']):
        st.balloons()
        st.success(L['msg'])
    
    if st.button(L['logout']):
        st.session_state.step = 'awakening'
        st.rerun()
