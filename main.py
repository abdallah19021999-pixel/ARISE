import streamlit as st

# 1. بروتوكول الهوية البصرية (Void & Neon HUD)
st.set_page_config(page_title="SYSTEM", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    .stApp { background: #000000 !important; color: #00d4ff !important; }
    
    /* إخفاء كل العناصر البيضاء والتحكمات التقليدية */
    header, footer, button[step="1"], button[step="-1"], [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] { 
        display: none !important; 
    }

    /* كروت المهمة (HUD Glass) */
    .quest-card {
        background: rgba(0, 212, 255, 0.02);
        border: 1px solid rgba(0, 212, 255, 0.1);
        padding: 20px; border-radius: 2px; margin-bottom: 20px;
    }

    /* مدخلات البيانات - Neon Dark Style */
    div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {
        background-color: #050505 !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        color: #00d4ff !important;
    }
    input { color: #00d4ff !important; background: transparent !important; font-family: 'Orbitron', 'Cairo'; }

    .stButton > button {
        width: 100%; background: transparent !important; color: #00d4ff !important;
        border: 1px solid #00d4ff !important; font-family: 'Orbitron';
        letter-spacing: 5px; padding: 15px !important; text-transform: uppercase;
    }
    .stButton > button:hover { background: rgba(0, 212, 255, 0.1) !important; box-shadow: 0 0 20px #00d4ff; }
    
    label { color: #222 !important; font-size: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# إدارة الحالة واللغة
if 'lang' not in st.session_state: st.session_state.lang = 'AR'
if 'step' not in st.session_state: st.session_state.step = 'awakening'

# أيقونة اللغة الصغيرة (Globe)
if st.sidebar.button("🌐"):
    st.session_state.lang = 'EN' if st.session_state.lang == 'AR' else 'AR'
    st.rerun()

# قاعدة بيانات التمارين المبرمجة
WORKOUTS = {
    "PPL": {
        "AR": {"دفع (Push)": ["بنش بار", "تجميع مائل", "كتف جانبي", "تراي كابل"], "سحب (Pull)": ["سحب واسع", "سحب أرضي", "باي بار", "رفرفة خلفي"], "أرجل (Legs)": ["سكوات", "ليج برس", "خلفيات", "سمانة"]},
        "EN": {"Push": ["Bench Press", "Incline DB", "Lateral Raises", "Triceps"], "Pull": ["Lat Pulldown", "Rows", "Bicep Curls", "Rear Delts"], "Legs": ["Squats", "Leg Press", "Leg Curls", "Calves"]}
    },
    "BRO SPLIT": {
        "AR": {"صدر": ["بنش بار", "تجميع مائل", "تفتيح"], "ظهر": ["عقلة", "منشار", "سحب عالي"], "أكتاف": ["ضغط بار", "جانبي", "خلفي"]},
        "EN": {"Chest": ["Flat Bench", "Incline DB", "Flys"], "Back": ["Pullups", "Rows", "Lat Pulldown"], "Shoulders": ["Military Press", "Lateral", "Rear"]}
    }
}

# --- المرحلة الأولى: THE REGISTRATION ---
if st.session_state.step == 'awakening':
    st.markdown('<div class="quest-card" style="text-align:center;"><h3>SYSTEM NOTIFICATION</h3><p>أنت الآن مؤهل لتكون لاعباً في النظام</p></div>', unsafe_allow_html=True)
    
    u_name = st.text_input("PLAYER ID")
    u_split = st.selectbox("CHOOSE PATH", ["PPL", "BRO SPLIT"])
    u_goal = st.selectbox("GOAL", ["BULK", "CUT"])
    
    c1, c2 = st.columns(2)
    u_w = c1.number_input("WEIGHT", value=80)
    u_h = c2.number_input("HEIGHT", value=175)
    
    if st.button("ARISE"):
        if u_name:
            bmi = round(u_w / ((u_h/100)**2), 1)
            rank = "S-RANK" if 22 <= bmi <= 25 else "A-RANK"
            st.session_state.player = {"name": u_name, "split": u_split, "goal": u_goal, "bmi": bmi, "rank": rank}
            st.session_state.step = 'dashboard'
            st.rerun()

# --- المرحلة الثانية: THE TRAINING HUD ---
elif st.session_state.step == 'dashboard':
    p = st.session_state.player
    st.markdown(f"<p style='font-family:Orbitron; font-size:12px;'>PLAYER: {p['name'].upper()} | {p['rank']}</p>", unsafe_allow_html=True)
    
    # فلترة الأيام بناءً على النظام المختار
    day_options = list(WORKOUTS[p['split']][st.session_state.lang].keys())
    selected_day = st.selectbox("SELECT MISSION ZONE", day_options)
    
    st.markdown(f'<div class="quest-card"><h4>DAILY QUEST: {selected_day}</h4></div>', unsafe_allow_html=True)
    
    # محرك التمارين الذكي
    ex_list = WORKOUTS[p['split']][st.session_state.lang][selected_day]
    rep_scheme = " (4 Sets x 8-10 Reps)" if p['goal'] == "BULK" else " (3 Sets x 15 Reps)"
    
    for ex in ex_list:
        st.checkbox(f"⚔️ {ex} {rep_scheme}")
    
    if st.button("CONFIRM COMPLETION"):
        st.info("QUEST DATA RECORDED IN SYSTEM LOG.")

    if st.button("TERMINATE"):
        st.session_state.step = 'awakening'
        st.rerun()
