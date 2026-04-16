import streamlit as st

# 1. إعدادات النظام وتثبيت الـ CSS الاحترافي
st.set_page_config(page_title="SYSTEM", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    .stApp { background: radial-gradient(circle at center, #001220 0%, #000000 100%) !important; color: #fff; }
    
    /* الـ Notification Box الزجاجي (كما في صورتك) */
    .glass-card {
        background: rgba(0, 30, 60, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 255, 0.15);
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        margin-bottom: 30px;
    }

    /* القضاء على الأبيض في الخانات والقوائم */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        color: #00d4ff !important;
    }
    
    /* تعديل شكل الـ Expander عشان ميبقاش أبيض */
    .st-emotion-cache-p4mowd { background-color: rgba(0, 0, 0, 0.4) !important; border: 1px solid rgba(0, 212, 255, 0.2) !important; }

    /* زرار ARISE النيون */
    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 5px;
        padding: 15px !important; box-shadow: 0 0 10px rgba(0, 212, 255, 0.2);
    }
    .stButton > button:hover { background: rgba(0, 212, 255, 0.1) !important; box-shadow: 0 0 30px #00d4ff; }

    header, footer {visibility: hidden !important;}
    label { color: rgba(255, 255, 255, 0.6) !important; font-family: 'Orbitron'; font-size: 11px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة خطوات التطبيق
if 'step' not in st.session_state:
    st.session_state.step = 'login'

# --- المرحلة الأولى: تسجيل اللاعب (Player Awakening) ---
if st.session_state.step == 'login':
    st.markdown('<div class="glass-card"><h2 style="color:#00d4ff; font-family:Orbitron;">SYSTEM NOTIFICATION</h2><p style="font-family:Cairo; color:#888;">أنت الآن مؤهل لتكون لاعباً في النظام</p></div>', unsafe_allow_html=True)
    
    with st.container():
        u_name = st.text_input("CODE NAME", placeholder="Enter Identity...")
        col1, col2 = st.columns(2)
        u_gender = col1.selectbox("GENDER", ["MALE", "FEMALE"])
        u_body = col2.selectbox("BODY TYPE", ["ECTOMORPH", "MESOMORPH", "ENDOMORPH"])
        u_goal = st.selectbox("PRIMARY OBJECTIVE", ["HYPERTROPHY (BULK)", "DEFINITION (CUT)"])
        
        if st.button("ARISE"):
            if u_name:
                st.session_state.user = {"name": u_name, "goal": u_goal, "gender": u_gender}
                st.session_state.step = 'dashboard'
                st.rerun()

# --- المرحلة الثانية: لوحة التحكم (Status & Muscle Selection) ---
elif st.session_state.step == 'dashboard':
    st.markdown(f"""
        <div style='text-align:center; margin-bottom:30px;'>
            <p style='font-family:Orbitron; color:#00d4ff; font-size:12px; letter-spacing:3px;'>STATUS: ACTIVE</p>
            <h1 style='font-family:Orbitron; font-size:40px; margin:0;'>PLAYER: {st.session_state.user['name'].upper()}</h1>
            <p style='color:#555;'>OBJECTIVE: {st.session_state.user['goal']}</p>
        </div>
    """, unsafe_allow_html=True)

    # اختيار العضلة
    target_muscle = st.selectbox("SELECT TARGET MUSCLE GROUP", ["CHEST & TRICEPS", "BACK & BICEPS", "LEGS & ABS", "SHOULDERS"])
    
    st.markdown("<br><p style='font-family:Orbitron; color:#00d4ff;'>DAILY QUESTS</p>", unsafe_allow_html=True)
    
    with st.expander(f"⚔️ {target_muscle} WORKOUT PLAN", expanded=True):
        st.write(f"Preparing protocol for {st.session_state.user['name']}...")
        q1 = st.checkbox("Main Compound Lift (4 Sets)")
        q2 = st.checkbox("Isolation Movement (3 Sets)")
        q3 = st.checkbox("Finisher Set (to Failure)")
        
        if q1 and q2 and q3:
            st.success("QUEST COMPLETED! +100 XP REWARDED")

    if st.button("TERMINATE SESSION (LOGOUT)"):
        st.session_state.step = 'login'
        st.rerun()
