import streamlit as st

# 1. تدمير اللون الأبيض وتثبيت واجهة الـ HUD (Neon & Glass)
st.set_page_config(page_title="THE SYSTEM", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    /* الخلفية الكونية */
    .stApp { 
        background: radial-gradient(circle at center, #000814 0%, #000000 100%) !important; 
        color: #00d4ff !important; 
    }
    
    /* إخفاء الهيدر وأزرار الـ + والـ - المزعجة */
    header, footer, button[step="1"], button[step="-1"], [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { 
        display: none !important; 
    }

    /* كروت النظام الزجاجية (Glassmorphism) */
    .system-card {
        background: rgba(0, 212, 255, 0.03);
        border: 1px solid rgba(0, 212, 255, 0.1);
        backdrop-filter: blur(15px);
        padding: 30px; border-radius: 4px;
        box-shadow: 0 0 50px rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
    }

    /* مدخلات البيانات - اختفاء الأبيض تماماً */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {
        background-color: rgba(0, 20, 40, 0.5) !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        color: #00d4ff !important; border-radius: 2px !important;
    }
    input { color: #00d4ff !important; background: transparent !important; font-family: 'Orbitron'; }

    /* أزرار ARISE القتالية */
    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron';
        letter-spacing: 10px; padding: 20px !important; transition: 0.4s;
    }
    .stButton > button:hover { 
        background: rgba(0, 212, 255, 0.1) !important; 
        box-shadow: 0 0 30px #00d4ff, inset 0 0 20px #00d4ff; 
    }

    /* نصوص الرتب */
    .rank-text { font-family: 'Orbitron'; font-size: 50px; text-shadow: 0 0 20px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# إدارة الحالة واللغة
if 'lang' not in st.session_state: st.session_state.lang = 'AR'
if 'step' not in st.session_state: st.session_state.step = 'awakening'

# أيقونة اللغة
if st.sidebar.button("🌐"):
    st.session_state.lang = 'EN' if st.session_state.lang == 'AR' else 'AR'
    st.rerun()

D = {
    'AR': {
        'title': 'إشعار النظام', 'warn': '[تحذير: لقد أصبحت لاعباً]',
        'name': 'هوية اللاعب', 'gender': 'الجنس', 'male': 'ذكر (Hunter)', 'female': 'أنثى (Huntress)',
        'path': 'اختر المسار', 'arise': 'نهوض (ARISE)', 'status': 'نافذة الحالة',
        'bmi_msg': 'تحليل كتلة الجسم جارٍ...', 'rank': 'الرتبة المستحقة'
    },
    'EN': {
        'title': 'SYSTEM NOTIFICATION', 'warn': '[WARNING: YOU HAVE BECOME A PLAYER]',
        'name': 'PLAYER ID', 'gender': 'GENDER', 'male': 'MALE (Hunter)', 'female': 'FEMALE (Huntress)',
        'path': 'CHOOSE PATH', 'arise': 'ARISE', 'status': 'STATUS WINDOW',
        'bmi_msg': 'ANALYZING BIOMETRICS...', 'rank': 'CALCULATED RANK'
    }
}
L = D[st.session_state.lang]

# --- المرحلة الأولى: THE INITIALIZATION ---
if st.session_state.step == 'awakening':
    st.markdown(f"""
        <div class="system-card" style="text-align:center;">
            <h1 style="font-family:Orbitron; letter-spacing:5px;">{L['title']}</h1>
            <p style="color:#555; font-size:12px;">{L['warn']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        u_name = st.text_input(L['name'], placeholder="ENTER CODE NAME...")
        
        col_g, col_p = st.columns(2)
        u_gender = col_g.selectbox(L['gender'], [L['male'], L['female']])
        u_split = col_p.selectbox(L['path'], ["PPL", "BRO SPLIT", "FULL BODY"])
        
        c1, c2 = st.columns(2)
        u_weight = c1.number_input("WEIGHT", value=80)
        u_height = c2.number_input("HEIGHT", value=175)
        
        if st.button(L['arise']):
            if u_name:
                bmi = round(u_weight / ((u_height/100)**2), 1)
                # نظام حساب الرتبة الحقيقي بناءً على القوة (BMI)
                if bmi < 18.5: rank = "E-RANK"
                elif 18.5 <= bmi < 25: rank = "S-RANK"
                elif 25 <= bmi < 30: rank = "A-RANK"
                else: rank = "B-RANK"
                
                st.session_state.player = {
                    "name": u_name, "gender": u_gender, "bmi": bmi, 
                    "rank": rank, "split": u_split
                }
                st.session_state.step = 'dashboard'
                st.rerun()

# --- المرحلة الثانية: THE STATUS HUD ---
elif st.session_state.step == 'dashboard':
    p = st.session_state.player
    
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <p style="font-family:Orbitron; font-size:12px;">{L['status']}</p>
            <p style="font-family:Orbitron; font-size:12px;">LVL. 01</p>
        </div>
        <div style="text-align:center; margin-top:20px;">
            <h1 style="font-family:Orbitron; font-size:50px; margin:0;">{p['name'].upper()}</h1>
            <p style="color:#00d4ff; letter-spacing:10px;">{p['gender'].upper()}</p>
        </div>
    """, unsafe_allow_html=True)

    col_rank, col_stat = st.columns(2)
    
    with col_rank:
        st.markdown(f"""
            <div class="system-card" style="text-align:center;">
                <p style="font-size:10px;">{L['rank']}</p>
                <h2 class="rank-text">{p['rank']}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col_stat:
        st.markdown(f"""
            <div class="system-card" style="text-align:center;">
                <p style="font-size:10px;">BIOMETRICS</p>
                <h2 style="font-family:Orbitron;">{p['bmi']}</h2>
                <p style="font-size:10px;">BMI INDEX</p>
            </div>
        """, unsafe_allow_html=True)

    # نظام المهام (Daily Quest)
    st.markdown(f"<p style='font-family:Orbitron; letter-spacing:3px;'>DAILY QUEST: {p['split']}</p>", unsafe_allow_html=True)
    with st.container():
        st.checkbox("Push Ups [0/100]")
        st.checkbox("Sit Ups [0/100]")
        st.checkbox("Running [0/10KM]")

    if st.button("TERMINATE"):
        st.session_state.step = 'awakening'
        st.rerun()
