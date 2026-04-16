import streamlit as st

# 1. الهوية البصرية (The Absolute Monarch - Zero White)
st.set_page_config(page_title="SYSTEM", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    
    /* إخفاء التحكمات الرقمية والألوان البيضاء */
    button[step="1"], button[step="-1"], [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {
        background-color: rgba(0, 15, 30, 0.7) !important; border: 1px solid #00d4ff33 !important; color: #00d4ff !important;
    }
    input { color: #00d4ff !important; background: transparent !important; }

    .system-msg { border-left: 2px solid #00d4ff; padding: 10px 15px; background: rgba(0, 212, 255, 0.05); margin-bottom: 20px; }
    
    /* أيقونة اللغة */
    .lang-btn { position: fixed; top: 10px; right: 10px; z-index: 1000; }
    
    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron', 'Cairo'; letter-spacing: 2px;
    }
    header, footer {visibility: hidden !important;}
    label { color: #333 !important; font-size: 11px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة المحرك واللغة
if 'lang' not in st.session_state: st.session_state.lang = 'AR'
if 'step' not in st.session_state: st.session_state.step = 'awakening'

# أيقونة تبديل اللغة الصغيرة
if st.button("🌐"):
    st.session_state.lang = 'EN' if st.session_state.lang == 'AR' else 'AR'
    st.rerun()

# القاموس الذكي مع شرح الأنظمة
DB = {
    'AR': {
        'warn': '[نظام التوجيه النشط: أدخل بياناتك]',
        'name': 'هوية اللاعب', 'age': 'العمر', 'weight': 'الوزن', 'height': 'الطول',
        'split': 'اختر بروتوكول التدريب',
        'split_info': {
            "Bro Split": "تمرين عضلة واحدة يومياً (مناسب للمبتدئين للتركيز).",
            "PPL": "تقسيم الجسم لتمارين الدفع، السحب، والأرجل (نظام احترافي).",
            "Upper/Lower": "يوم للجزء العلوي ويوم للجزء السفلي (توازن عالي).",
            "Full Body": "تمرين الجسم بالكامل في حصة واحدة (لأقصى حرق)."
        },
        'status': 'نافذة الحالة', 'quest': 'حدد منطقة المهمة', 'arise': 'نهوض (ARISE)',
        'target_map': {
            "Bro Split": ["صدر", "ظهر", "أرجل", "أكتاف", "ذراع"],
            "PPL": ["دفع (Push)", "سحب (Pull)", "أرجل (Legs)"],
            "Upper/Lower": ["جزء علوي", "جزء سفلي"],
            "Full Body": ["كامل الجسم"]
        }
    },
    'EN': {
        'warn': '[GUIDANCE SYSTEM ACTIVE: INPUT DATA]',
        'name': 'PLAYER ID', 'age': 'AGE', 'weight': 'WEIGHT', 'height': 'HEIGHT',
        'split': 'SELECT TRAINING PROTOCOL',
        'split_info': {
            "Bro Split": "One muscle group per day (Great for focus).",
            "PPL": "Push, Pull, and Legs rotation (Elite balance).",
            "Upper/Lower": "Dedicated days for Upper and Lower body.",
            "Full Body": "Hit every muscle in one session (High frequency)."
        },
        'status': 'STATUS WINDOW', 'quest': 'TARGET ZONE', 'arise': 'ARISE',
        'target_map': {
            "Bro Split": ["CHEST", "BACK", "LEGS", "SHOULDERS", "ARMS"],
            "PPL": ["PUSH Day", "PULL Day", "LEGS Day"],
            "Upper/Lower": ["UPPER", "LOWER"],
            "Full Body": ["FULL BODY"]
        }
    }
}
L = DB[st.session_state.lang]

# --- المرحلة الأولى: Awakening ---
if st.session_state.step == 'awakening':
    st.markdown(f'<div class="system-msg"><p style="font-size:14px;">{L["warn"]}</p></div>', unsafe_allow_html=True)
    
    u_name = st.text_input(L['name'])
    c1, c2, c3 = st.columns(3)
    u_age = c1.number_input(L['age'], step=1, value=25)
    u_weight = c2.number_input(L['weight'], step=1, value=80)
    u_height = c3.number_input(L['height'], step=1, value=175)
    
    # اختيار النظام مع الشرح
    u_split = st.selectbox(L['split'], list(L['split_info'].keys()))
    st.info(f"💡 {L['split_info'][u_split]}") # شرح يظهر للمبتدئ فوراً
    
    u_injury = st.multiselect("إصابات / Injuries", ["SHOULDER", "BACK", "KNEE"])
    
    if st.button(L['arise']):
        if u_name:
            bmi = round(u_weight / ((u_height/100)**2), 1)
            st.session_state.player = {"name": u_name, "bmi": bmi, "split": u_split, "injury": u_injury}
            st.session_state.step = 'dashboard'
            st.rerun()

# --- المرحلة الثانية: Dashboard ---
elif st.session_state.step == 'dashboard':
    p = st.session_state.player
    st.markdown(f"<div style='text-align:center;'><p>{L['status']}</p><h1>{p['name'].upper()}</h1></div>", unsafe_allow_html=True)

    # الفلترة الذكية: يظهر فقط ما يخص النظام المختار
    available_zones = L['target_map'][p['split']]
    target = st.selectbox(L['quest'], available_zones)

    # رسمة الجسم (تتحرك مع الفلتر الجديد)
    is_lower = "أرجل" in target or "LEGS" in target or "سفلي" in target or "LOWER" in target
    st.markdown(f"""
        <div style="text-align:center; margin: 20px 0;">
            <svg width="60" height="100" viewBox="0 0 100 150">
                <circle cx="50" cy="15" r="10" fill="#111" />
                <rect x="30" y="30" width="40" height="50" fill="{'#111' if is_lower else '#00d4ff'}" rx="2" />
                <rect x="32" y="85" width="15" height="60" fill="{'#00d4ff' if is_lower else '#111'}" rx="2" />
                <rect x="53" y="85" width="15" height="60" fill="{'#00d4ff' if is_lower else '#111'}" rx="2" />
            </svg>
        </div>
    """, unsafe_allow_html=True)

    # عرض التمارين بناءً على الاختيار المفلتر
    st.write(f"⚔️ {target} Protocol Active")
    st.checkbox("Exercise Alpha")
    st.checkbox("Exercise Beta")

    if st.button("TERMINATE"):
        st.session_state.step = 'awakening'
        st.rerun()
