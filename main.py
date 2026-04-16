import streamlit as st
import time

# 1. تثبيت واجهة "النظام" (Zero White - Neon Blue/Red)
st.set_page_config(page_title="THE SYSTEM", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    
    /* إخفاء العبث */
    button[step="1"], button[step="-1"], [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"], header, footer { display: none !important; }
    
    /* رسائل النظام المميزة */
    .system-header {
        border: 2px solid #00d4ff; background: rgba(0, 212, 255, 0.1);
        padding: 20px; text-align: center; font-family: 'Orbitron';
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2); margin-bottom: 30px;
    }
    
    .quest-box {
        border-left: 5px solid #00d4ff; background: rgba(0, 10, 20, 0.8);
        padding: 20px; margin-top: 20px; font-family: 'Cairo';
    }

    .penalty-warn {
        color: #ff4b4b !important; border: 2px solid #ff4b4b;
        background: rgba(255, 75, 75, 0.1); padding: 15px; text-align: center;
        font-family: 'Orbitron'; animation: blinker 1.5s linear infinite;
    }
    @keyframes blinker { 50% { opacity: 0.3; } }

    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background: #050505 !important; border: 1px solid #111 !important; color: #00d4ff !important;
    }
    
    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# إدارة الحالة واللغة
if 'lang' not in st.session_state: st.session_state.lang = 'AR'
if 'step' not in st.session_state: st.session_state.step = 'awakening'

# أيقونة التبديل (Stealth Mode)
if st.sidebar.button("🌐"):
    st.session_state.lang = 'EN' if st.session_state.lang == 'AR' else 'AR'
    st.rerun()

# القاموس الروحي للنظام
D = {
    'AR': {
        'title': 'إشعار النظام', 'warn': '[تحذير: لقد أصبحت لاعباً]',
        'sub': 'أكمل عملية التسجيل للوصول إلى نافذة الحالة',
        'quest_title': 'المهمة اليومية: تحضيرات القوة',
        'penalty': 'تحذير: الفشل في إنهاء المهمة سيؤدي إلى "منطقة العقاب"',
        'info': {"PPL": "دفع/سحب/أرجل - توازن القوى", "Bro": "عضلة واحدة - تركيز الصياد"},
        'arise': 'نهوض (ARISE)', 'complete': 'إكمال المهمة', 'status': 'نافذة الحالة'
    },
    'EN': {
        'title': 'SYSTEM NOTIFICATION', 'warn': '[WARNING: YOU HAVE BECOME A PLAYER]',
        'sub': 'COMPLETE REGISTRATION TO ACCESS STATUS WINDOW',
        'quest_title': 'DAILY QUEST: PREPARATIONS TO BECOME STRONG',
        'penalty': 'WARNING: FAILURE TO COMPLETE WILL TRIGGER PENALTY QUEST',
        'info': {"PPL": "Push/Pull/Legs - Balanced Power", "Bro": "One Muscle - Hunter Focus"},
        'arise': 'ARISE', 'complete': 'COMPLETE QUEST', 'status': 'STATUS WINDOW'
    }
}
L = D[st.session_state.lang]

# --- المرحلة الأولى: THE AWAKENING ---
if st.session_state.step == 'awakening':
    st.markdown(f'<div class="system-header"><h1>{L["title"]}</h1><p>{L["warn"]}</p></div>', unsafe_allow_html=True)
    
    name = st.text_input("PLAYER NAME", placeholder="...")
    u_split = st.selectbox("CHOOSE YOUR PATH", list(L['info'].keys()))
    st.caption(L['info'][u_split])
    
    c1, c2 = st.columns(2)
    weight = c1.number_input("WEIGHT", value=80)
    height = c2.number_input("HEIGHT", value=175)

    if st.button(L['arise']):
        if name:
            st.session_state.player = {"name": name, "split": u_split}
            st.session_state.step = 'dashboard'
            st.rerun()

# --- المرحلة الثانية: THE QUEST LOG ---
elif st.session_state.step == 'dashboard':
    p = st.session_state.player
    st.markdown(f"<div style='text-align:right;'>[ {L['status']} ]</div>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='font-family:Orbitron;'>{p['name'].upper()}</h1>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="quest-box">
            <h3 style="color:#00d4ff; margin:0;">{L['quest_title']}</h3>
            <p style="font-size:12px; opacity:0.7;">[المهمة الحالية: {p['split']}]</p>
        </div>
    """, unsafe_allow_html=True)

    # محتوى المهمة بناءً على النظام (PPL كمثال للتوضيح)
    st.write("---")
    q1 = st.checkbox("Push Ups [0/100]")
    q2 = st.checkbox("Squats [0/100]")
    q3 = st.checkbox("Running [0/10 KM]")

    # العقوبة (Penalty Zone) - تظهر إذا حاولت تخرج بدون إكمال
    st.markdown(f'<div class="penalty-warn">{L["penalty"]}</div>', unsafe_allow_html=True)

    if st.button(L['complete']):
        if q1 and q2 and q3:
            st.success("لقد حصلت على مكافأة: زيادة في رتبة اللاعب!")
        else:
            st.error("المهمة لم تكتمل بعد. لا يمكنك الهروب من النظام.")

    if st.sidebar.button("TERMINATE"):
        st.warning("هل أنت متأكد؟ النظام لن ينسى هذا التراجع.")
        if st.sidebar.button("YES"):
            st.session_state.step = 'awakening'
            st.rerun()
