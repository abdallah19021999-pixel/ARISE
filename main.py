import streamlit as st

# 1. تثبيت الواجهة المظلمة (The Absolute Void)
st.set_page_config(page_title="SYSTEM", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    header, footer, [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { display: none !important; }
    
    .system-card {
        background: rgba(0, 20, 40, 0.4); border: 1px solid #00d4ff33;
        padding: 20px; border-radius: 4px; margin-bottom: 20px;
    }
    
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background: #050505 !important; border: 1px solid #00d4ff22 !important; color: #00d4ff !important;
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

if st.sidebar.button("🌐"):
    st.session_state.lang = 'EN' if st.session_state.lang == 'AR' else 'AR'
    st.rerun()

# 2. قاعدة بيانات التمارين (The Sacred Archive)
WORKOUT_DB = {
    "PPL": {
        "AR": {
            "PUSH": ["بنش برس بار", "تجميع دمبل مائل", "كتف بار أمامي", "تراي كابل", "رفرفة جانبي"],
            "PULL": ["سحب عالي (Lats)", "سحب أرضي", "رفرفة خلفي", "باي دمبل تبادل", "سحب بار ظهر"],
            "LEGS": ["سكوات", "ليج برس", "رفرفة أمامي", "خلفيات ماكينة", "سمانة"]
        },
        "EN": {
            "PUSH": ["Bench Press", "Incline DB Press", "Overhead Press", "Tricep Pushdowns", "Lateral Raises"],
            "PULL": ["Lat Pulldowns", "Seated Rows", "Rear Delt Flys", "Bicep Curls", "Barbell Rows"],
            "LEGS": ["Squats", "Leg Press", "Leg Extensions", "Hamstring Curls", "Calf Raises"]
        }
    },
    "BRO SPLIT": {
        "AR": {
            "CHEST": ["بنش مستوي", "تفتيح كابل", "غطس", "بنش مائل"],
            "BACK": ["عقلة", "سحب واسع", "منشار دمبل", "رفعة ميتة"],
            "ARMS": ["باي بار", "تراي مسطرة", "تبادل دمبل", "تراي بنش ضيق"]
        },
        "EN": {
            "CHEST": ["Flat Bench", "Cable Flys", "Dips", "Incline Bench"],
            "BACK": ["Pull-ups", "Wide Pulldown", "DB Rows", "Deadlifts"],
            "ARMS": ["Barbell Curls", "Tricep Bar", "DB Curls", "Close Grip Bench"]
        }
    }
}

# --- المرحلة الأولى: THE INITIALIZATION ---
if st.session_state.step == 'awakening':
    st.markdown('<div class="system-card" style="text-align:center;"><h2>SYSTEM NOTIFICATION</h2><p>[تحذير: دخول بروتوكول الصحوة]</p></div>', unsafe_allow_html=True)
    u_name = st.text_input("CODE NAME")
    u_split = st.selectbox("PATH", ["PPL", "BRO SPLIT"])
    u_goal = st.selectbox("OBJECTIVE", ["BULK", "CUT"])
    u_gender = st.selectbox("GENDER", ["MALE", "FEMALE"])
    
    col1, col2 = st.columns(2)
    u_w = col1.number_input("WEIGHT", value=80)
    u_h = col2.number_input("HEIGHT", value=175)

    if st.button("ARISE"):
        if u_name:
            bmi = round(u_w / ((u_h/100)**2), 1)
            st.session_state.player = {"name": u_name, "split": u_split, "goal": u_goal, "bmi": bmi, "gender": u_gender}
            st.session_state.step = 'dashboard'
            st.rerun()

# --- المرحلة الثانية: THE COMBAT ZONE (التمارين) ---
elif st.session_state.step == 'dashboard':
    p = st.session_state.player
    st.markdown(f"<p style='font-family:Orbitron; font-size:10px;'>STATUS: {p['name'].upper()}</p>", unsafe_allow_html=True)
    
    # اختيار اليوم التدريبي بناءً على النظام
    days = list(WORKOUT_DB[p['split']][st.session_state.lang].keys())
    active_day = st.selectbox("SELECT TARGET ZONE", days)

    # عرض المهمة اليومية (Daily Quest)
    st.markdown(f"""
        <div class="system-card">
            <h3 style="color:#00d4ff; margin:0;">DAILY QUEST: {active_day}</h3>
            <p style="font-size:12px; opacity:0.6;">[الهدف: {p['goal']} | المسار: {p['split']}]</p>
        </div>
    """, unsafe_allow_html=True)

    # استخراج التمارين وتعديل الـ Reps ذكياً
    exercises = WORKOUT_DB[p['split']][st.session_state.lang][active_day]
    reps = " (4 Sets x 8 Heavy)" if p['goal'] == "BULK" else " (3 Sets x 15 Speed)"

    for i, ex in enumerate(exercises):
        st.checkbox(f"{ex} {reps}", key=f"ex_{i}")

    if st.button("COMPLETE QUEST"):
        st.balloons()
        st.success("تم تسجيل البيانات. رتبتك في تزايد.")

    if st.button("LOGOUT"):
        st.session_state.step = 'awakening'
        st.rerun()
