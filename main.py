import streamlit as st

# 1. إعدادات النظام والستايل الزجاجي (Zero-White Policy)
st.set_page_config(page_title="MONARCH SYSTEM", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    .stApp { background: radial-gradient(circle at center, #001220 0%, #000000 100%) !important; color: #fff; }
    
    /* الـ System Notification */
    .glass-card {
        background: rgba(0, 30, 60, 0.2);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 212, 255, 0.15);
        border-radius: 10px;
        padding: 25px;
        text-align: center;
        margin-bottom: 25px;
    }

    /* الخانات الاحترافية */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-testid="stNumberInput"] {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(0, 212, 255, 0.1) !important;
        color: #00d4ff !important;
    }

    /* شاشة الـ Status (Deep UI) */
    .stat-box {
        border-left: 2px solid #00d4ff;
        background: rgba(0, 212, 255, 0.03);
        padding: 15px;
        margin: 10px 0;
    }

    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron'; letter-spacing: 5px;
        padding: 12px !important; box-shadow: 0 0 10px rgba(0, 212, 255, 0.1);
    }
    .stButton > button:hover { background: rgba(0, 212, 255, 0.1) !important; box-shadow: 0 0 20px #00d4ff; }

    header, footer {visibility: hidden !important;}
    label { color: #555 !important; font-family: 'Orbitron'; font-size: 11px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام إدارة البيانات
if 'step' not in st.session_state:
    st.session_state.step = 'awakening'

# --- المرحلة الأولى: Awakening & Bio-Data ---
if st.session_state.step == 'awakening':
    st.markdown('<div class="glass-card"><h2 style="color:#00d4ff; font-family:Orbitron; letter-spacing:3px;">SYSTEM NOTIFICATION</h2><p style="font-family:Cairo; color:#666;">بروتوكول تحليل المؤشرات الحيوية قيد التشغيل</p></div>', unsafe_allow_html=True)
    
    with st.container():
        u_name = st.text_input("PLAYER CODE NAME", placeholder="IDENTIFY YOURSELF...")
        
        col1, col2, col3 = st.columns(3)
        u_age = col1.number_input("AGE", min_value=15, max_value=60, value=25)
        u_weight = col2.number_input("WEIGHT (KG)", min_value=40, max_value=200, value=80)
        u_height = col3.number_input("HEIGHT (CM)", min_value=140, max_value=220, value=175)
        
        u_goal = st.selectbox("PRIMARY OBJECTIVE", ["HYPERTROPHY (BULK)", "DEFINITION (CUT)"])
        
        # حساب BMI تلقائياً
        bmi = round(u_weight / ((u_height/100)**2), 1)
        
        if st.button("ARISE"):
            if u_name:
                st.session_state.player = {
                    "name": u_name, "age": u_age, "weight": u_weight, 
                    "height": u_height, "bmi": bmi, "goal": u_goal
                }
                st.session_state.step = 'dashboard'
                st.rerun()

# --- المرحلة الثانية: Pro Dashboard & Elite Workout ---
elif st.session_state.step == 'dashboard':
    p = st.session_state.player
    
    # واجهة الـ Status الاحترافية (كما في الصور)
    st.markdown(f"""
        <div style='text-align:center; margin-bottom:30px;'>
            <p style='font-family:Orbitron; color:#00d4ff; font-size:12px; letter-spacing:5px;'>STATUS: ONLINE</p>
            <h1 style='font-family:Orbitron; font-size:35px; margin:0;'>{p['name'].upper()}</h1>
            <div style='display:flex; justify-content:center; gap:20px; color:#555; font-family:Orbitron; font-size:12px;'>
                <span>AGE: {p['age']}</span> | <span>BMI: {p['bmi']}</span> | <span>GOAL: {p['goal']}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # نظام اختيار التمارين الاحترافي
    muscle_group = st.selectbox("CHOOSE YOUR BATTLEFIELD (MUSCLE GROUP)", 
                               ["CHEST & TRICEPS", "BACK & BICEPS", "LEGS & GLUTES", "SHOULDERS & ABS"])

    # بنك التمارين الاحترافي (Professional Coach Data)
    workouts = {
        "CHEST & TRICEPS": [
            "Incline Bench Press (Barbell) - 4 Sets x 8-10",
            "Flat Dumbbell Press - 3 Sets x 12",
            "Cable Chest Flys (Middle to Low) - 3 Sets x 15",
            "Dips (Chest Version) - 3 Sets to Failure",
            "Skull Crushers (EZ Bar) - 4 Sets x 10",
            "Tricep Overhead Extension - 3 Sets x 12",
            "Rope Pushdowns (Extreme Squeeze) - 3 Sets x 15"
        ],
        "BACK & BICEPS": [
            "Deadlifts / Rack Pulls - 4 Sets x 6-8",
            "Lat Pulldowns (Wide Grip) - 4 Sets x 10",
            "Seated Cable Row - 3 Sets x 12",
            "Single Arm Dumbbell Row - 3 Sets x 10",
            "Barbell Curls - 4 Sets x 10",
            "Hammer Curls - 3 Sets x 12",
            "Concentration Curls - 3 Sets x 15"
        ]
    }

    st.markdown("<p style='font-family:Orbitron; color:#00d4ff; font-size:14px;'>DAILY QUESTS (ELITE PROTOCOL)</p>", unsafe_allow_html=True)
    
    with st.container():
        current_workout = workouts.get(muscle_group, ["Rest Day Protocol - Active Recovery"])
        completed_count = 0
        
        for exercise in current_workout:
            if st.checkbox(exercise):
                completed_count += 1
        
        # Progress Bar نيون
        progress = completed_count / len(current_workout)
        st.progress(progress)
        
        if completed_count == len(current_workout):
            st.success("LEVEL UP! QUEST CLEARED.")

    if st.button("TERMINATE SESSION"):
        st.session_state.step = 'awakening'
        st.rerun()
