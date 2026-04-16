import streamlit as st
from datetime import datetime

# 1. إعدادات الواجهة القتالية (HUD - No White)
st.set_page_config(page_title="SYSTEM HUD", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    
    /* إخفاء الهيدر وأزرار الزائد والناقص */
    header, footer, button[step="1"], button[step="-1"], [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }

    .system-card {
        background: rgba(0, 15, 30, 0.6); border: 1px solid rgba(0, 212, 255, 0.2);
        padding: 20px; border-radius: 2px; margin-bottom: 20px;
    }

    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {
        background-color: #050505 !important; border: 1px solid #00d4ff44 !important; color: #00d4ff !important;
    }
    input { color: #00d4ff !important; background: transparent !important; }

    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 5px; padding: 15px !important;
    }
    .stButton > button:hover { background: rgba(0, 212, 255, 0.1) !important; box-shadow: 0 0 20px #00d4ff; }
    
    label { color: #444 !important; font-size: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الذاكرة واللغة
if 'history' not in st.session_state: st.session_state.history = []
if 'level' not in st.session_state: st.session_state.level = 1
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'step' not in st.session_state: st.session_state.step = 'awakening'
if 'lang' not in st.session_state: st.session_state.lang = 'AR'

# أيقونة التبديل السريع
if st.sidebar.button("🌐"):
    st.session_state.lang = 'EN' if st.session_state.lang == 'AR' else 'AR'
    st.rerun()

# القاموس الشامل
DB = {
    'AR': {
        'title': 'إشعار النظام', 'name': 'اسم اللاعب', 'gender': 'تحديد الجنس', 'm': 'ذكر (Hunter)', 'f': 'أنثى (Huntress)',
        'path': 'المسار التدريبي', 'arise': 'نهوض (ARISE)', 'status': 'نافذة الحالة', 'log': 'سجل اللاعب',
        'info': {"PPL": "دفع/سحب/أرجل - نظام متوازن", "Bro": "عضلة واحدة - تركيز عالي"},
        'quest': 'المهمة النشطة', 'comp': 'تأكيد الإنجاز', 'lvl': 'المستوى', 'rank': 'الرتبة'
    },
    'EN': {
        'title': 'SYSTEM NOTIFICATION', 'name': 'PLAYER ID', 'gender': 'GENDER', 'm': 'MALE (Hunter)', 'f': 'FEMALE (Huntress)',
        'path': 'TRAINING PATH', 'arise': 'ARISE', 'status': 'STATUS WINDOW', 'log': 'PLAYER LOG',
        'info': {"PPL": "Push/Pull/Legs - Balanced Path", "Bro": "One Muscle - High Focus"},
        'quest': 'ACTIVE QUEST', 'comp': 'CONFIRM COMPLETION', 'lvl': 'LEVEL', 'rank': 'RANK'
    }
}
L = DB[st.session_state.lang]

# --- المرحلة الأولى: Awakening (التسجيل وتحديد الجنس) ---
if st.session_state.step == 'awakening':
    st.markdown(f'<div class="system-card" style="text-align:center;"><h1>{L["title"]}</h1></div>', unsafe_allow_html=True)
    
    u_name = st.text_input(L['name'])
    
    col_g, col_s = st.columns(2)
    u_gender = col_g.selectbox(L['gender'], [L['m'], L['f']])
    u_split = col_s.selectbox(L['path'], ["PPL", "Bro Split"])
    st.caption(L['info'].get(u_split, ""))

    col_w, col_h = st.columns(2)
    u_w = col_w.number_input("WEIGHT", value=80)
    u_h = col_h.number_input("HEIGHT", value=175)

    if st.button(L['arise']):
        if u_name:
            bmi = round(u_w / ((u_h/100)**2), 1)
            rank = "S" if 22 <= bmi <= 25 else "A"
            st.session_state.player = {"name": u_name, "gender": u_gender, "split": u_split, "bmi": bmi, "rank": rank}
            st.session_state.step = 'dashboard'
            st.rerun()

# --- المرحلة الثانية: THE HUD (المهام والسجل) ---
elif st.session_state.step == 'dashboard':
    p = st.session_state.player
    
    # واجهة الحالة (Status Window)
    st.markdown(f"""
        <div style="display:flex; justify-content:space-between; border-bottom:1px solid #111; padding-bottom:10px;">
            <div>{L['lvl']}: <span style="color:#ff00ff;">{st.session_state.level}</span></div>
            <div style="font-family:Orbitron;">{p['name'].upper()} [{p['gender']}]</div>
            <div>{L['rank']}: <span style="color:#00d4ff;">{p['rank']}</span></div>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs([L['quest'], L['log']])

    with tab1:
        # نظام الفلترة الذكي بناءً على المسار
        zones = ["Push", "Pull", "Legs"] if p['split'] == "PPL" else ["Chest", "Back", "Arms"]
        target = st.selectbox("MISSION ZONE", zones)
        
        st.markdown(f'<div class="system-card"><b>CURRENT QUEST: {target}</b></div>', unsafe_allow_html=True)
        q1 = st.checkbox("Phase 1: Heavy Sets")
        q2 = st.checkbox("Phase 2: Volume Sets")
        
        if st.button(L['comp']):
            if q1 and q2:
                log_data = {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "task": target, "xp": 25}
                st.session_state.history.append(log_data)
                st.session_state.xp += 25
                if st.session_state.xp >= 100:
                    st.session_state.level += 1
                    st.session_state.xp = 0
                st.rerun()

    with tab2:
        for entry in reversed(st.session_state.history):
            st.markdown(f"""
                <div style="background:rgba(0,212,255,0.02); padding:10px; margin-bottom:5px; border-left:2px solid #00d4ff;">
                    <small>{entry['date']}</small> | <b>{entry['task']}</b> | XP +{entry['xp']}
                </div>
            """, unsafe_allow_html=True)

    if st.sidebar.button("LOGOUT"):
        st.session_state.step = 'awakening'
        st.rerun()
