import streamlit as st
import time

# 1. إعدادات النظام
st.set_page_config(page_title="MONARCH SYSTEM", layout="centered")

# 2. CSS الاحترافي (Glassmorphism & Minimalist)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');

    .stApp { background: radial-gradient(circle at center, #001220 0%, #000000 100%) !important; color: white; }
    
    /* الـ Notification Box الزجاجي */
    .glass-card {
        background: rgba(0, 30, 60, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 25px;
        text-align: center;
    }

    /* ستايل الخانات */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(0, 212, 255, 0.1) !important;
        color: #00d4ff !important;
    }

    /* زر ARISE */
    .stButton > button {
        width: 100%;
        background: transparent !important;
        color: #00d4ff !important;
        border: 1px solid #00d4ff !important;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 5px;
        padding: 15px !important;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.2);
    }
    .stButton > button:hover { background: rgba(0, 212, 255, 0.1) !important; box-shadow: 0 0 30px #00d4ff; }

    /* شاشة الـ Status (زي الصورة اللي بعتها) */
    .status-text { font-family: 'Orbitron', sans-serif; color: #00d4ff; font-size: 14px; letter-spacing: 2px; }
    .level-val { font-size: 50px; font-weight: bold; color: white; }
    
    header, footer {visibility: hidden !important;}
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة حالة المستخدم (Session State)
if 'page' not in st.session_state:
    st.session_state.page = 'awakening'

# --- المرحلة الأولى: واجهة الدخول (The Awakening) ---
if st.session_state.page == 'awakening':
    st.markdown("""
        <div class="glass-card">
            <h1 style='color:#00d4ff; font-family:Orbitron; font-size:22px; letter-spacing:5px;'>SYSTEM NOTIFICATION</h1>
            <p style='font-family:Cairo; color:#666; font-size:14px; margin-top:10px;'>أنت الآن مؤهل لتكون لاعباً في النظام</p>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            name = st.text_input("IDENTIFICATION", placeholder="NAME...")
            goal = st.selectbox("OBJECTIVE", ["BULK", "CUT"])
            if st.button("ARISE"):
                if name:
                    st.session_state.user_name = name
                    st.session_state.goal = goal
                    st.session_state.page = 'status'
                    st.rerun()

# --- المرحلة الثانية: لوحة التحكم والتمارين (Status & Quests) ---
elif st.session_state.page == 'status':
    # الهيدر الفخم
    st.markdown(f"""
        <div style='text-align:center; margin-bottom:40px;'>
            <p class="status-text">STATUS</p>
            <div class="level-val">1</div>
            <p style='color:#555; font-family:Orbitron;'>LEVEL</p>
            <h3 style='color:#00d4ff; font-family:Orbitron;'>PLAYER: {st.session_state.user_name.upper()}</h3>
        </div>
    """, unsafe_allow_html=True)

    # تقسيم المهام اليومية (Daily Quests)
    st.markdown("<p class='status-text'>DAILY QUESTS</p>", unsafe_allow_html=True)
    
    with st.expander("⚔️ WORKOUT PLAN (TODAY)", expanded=True):
        st.write("Target: Chest & Triceps")
        # هنا التمارين اللي قولتلي عليها قبل كدا
        quest1 = st.checkbox("Bench Press (4 Sets x 10)")
        quest2 = st.checkbox("Incline Dumbbell Press (3 Sets x 12)")
        quest3 = st.checkbox("Tricep Pushdowns (4 Sets x 15)")
        
        if quest1 and quest2 and quest3:
            st.success("QUEST COMPLETED! +100 XP")

    if st.button("LOGOUT"):
        st.session_state.page = 'awakening'
        st.rerun()
