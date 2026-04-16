import streamlit as st
import time

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="SYSTEM HUD", layout="centered")

# إدارة الحالة (State Management)
if 'lang' not in st.session_state: st.session_state.lang = 'EN'
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'level' not in st.session_state: st.session_state.level = 1
if 'inventory' not in st.session_state: st.session_state.inventory = {}
if 'step' not in st.session_state: st.session_state.step = 'awakening'

# قاموس الترجمة الكامل
STR = {
    'EN': {
        'title': 'SYSTEM NOTIFICATION', 'warning': '[WARNING: YOU HAVE BECOME A PLAYER]',
        'name': 'PLAYER NAME', 'gen': 'GENDER', 'path': 'TRAINING PATH', 'inj': 'INJURY SCAN',
        'weight': 'WEIGHT (KG)', 'height': 'HEIGHT (CM)', 'btn_arise': 'ARISE',
        'lvl': 'LVL', 'mission': 'SELECT MISSION SESSION', 'prev': 'Prev', 'rest': 'Rest',
        'clear': 'Cleared (+15 XP)', 'reset': 'RESET SYSTEM', 'male': 'MALE (Hunter)',
        'female': 'FEMALE (Huntress)', 'go': '🔥 GO!', 'bmi': 'BMI STATUS'
    },
    'AR': {
        'title': 'تنبيه النظام', 'warning': '[تحذير: لقد أصبحت لاعباً في النظام]',
        'name': 'اسم اللاعب', 'gen': 'الجنس', 'path': 'مسار التدريب', 'inj': 'فحص الإصابات',
        'weight': 'الوزن (كجم)', 'height': 'الطول (سم)', 'btn_arise': 'نهوض',
        'lvl': 'المستوى', 'mission': 'اختر المهمة التدريبية', 'prev': 'السابق', 'rest': 'راحة',
        'clear': 'تم التنفيذ (+15 XP)', 'reset': 'إعادة ضبط النظام', 'male': 'ذكر (صياد)',
        'female': 'أنثى (صيادة)', 'go': '🔥 انطلق!', 'bmi': 'حالة كتلة الجسم'
    }
}

L = STR[st.session_state.lang]

# تصميم الـ CSS (المتوهج والنظيف)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    .stApp {{
        background: radial-gradient(circle at center, #001525 0%, #000000 100%) !important;
        background-attachment: fixed; color: #00d4ff !important; 
        font-family: '{"Orbitron" if st.session_state.lang == "EN" else "Cairo"}', sans-serif;
        direction: {"ltr" if st.session_state.lang == "EN" else "rtl"};
    }}
    .system-title {{
        font-family: 'Orbitron'; color: #00d4ff; text-align: center;
        text-shadow: 0 0 20px #00d4ff; background: rgba(0, 212, 255, 0.05); 
        padding: 20px; border: 1px solid rgba(0, 212, 255, 0.1); border-radius: 10px;
        animation: glowPulse 3s infinite ease-in-out;
    }}
    @keyframes glowPulse {{
        0% {{ text-shadow: 0 0 5px #00d4ff; opacity: 0.8; }}
        50% {{ text-shadow: 0 0 20px #00d4ff, 0 0 30px #00fbff; opacity: 1; }}
        100% {{ text-shadow: 0 0 5px #00d4ff; opacity: 0.8; }}
    }}
    .xp-bar-container {{
        width: 100%; background: rgba(0, 212, 255, 0.05); border: 1px solid #00d4ff44; 
        height: 12px; border-radius: 6px; margin: 10px 0;
    }}
    .xp-bar-fill {{
        height: 100%; background: linear-gradient(90deg, #00d4ff, #00fbff); 
        box-shadow: 0 0 15px #00d4ff; border-radius: 6px; transition: width 0.8s ease;
    }}
    .exercise-card {{
        background: rgba(0, 212, 255, 0.07); border-left: 5px solid #00d4ff;
        padding: 20px; margin: 15px 0; border-radius: 4px; text-align: {"left" if st.session_state.lang == "EN" else "right"};
    }}
    .alt-card {{
        background: rgba(255, 0, 255, 0.07); border-left: 5px solid #ff00ff;
        padding: 20px; margin: 15px 0; border-radius: 4px; text-align: {"left" if st.session_state.lang == "EN" else "right"};
    }}
    input, .stSelectbox div, .stMultiSelect div, .stNumberInput div {{
        background-color: rgba(0, 0, 0, 0.8) !important; color: #00d4ff !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# زر تبديل اللغة في الأعلى
if st.button(f"🌐 {st.session_state.lang}"):
    st.session_state.lang = 'AR' if st.session_state.lang == 'EN' else 'EN'
    st.rerun()

def add_xp(amount):
    st.session_state.xp += amount
    if st.session_state.xp >= 100:
        st.session_state.level += 1
        st.session_state.xp = 0
        st.toast("⚡ LEVEL UP! ⚡" if st.session_state.lang == 'EN' else "⚡ ارتقاء بالمستوى! ⚡")

# 2. قاعدة البيانات الشاملة (7 تمارين لكل حصة)
DB = {
    "PPL (Push/Pull/Legs)": {
        "PULL (Back/Biceps)": [
            {"en": "Deadlift", "ar": "رفعة ميتة", "sets": 3, "reps": "5", "inj": "Lower Back", "alt_en": "Lat Pulldown", "alt_ar": "سحب عالي"},
            {"en": "Barbell Rows", "ar": "سحب بار", "sets": 4, "reps": "8", "inj": "Lower Back", "alt_en": "Seated Rows", "alt_ar": "سحب أرضي"},
            {"en": "Lat Pulldown", "ar": "سحب عالي واسع", "sets": 4, "reps": "12", "inj": "Shoulder Blade", "alt_en": "Seated Rows", "alt_ar": "سحب أرضي"},
            {"en": "One Arm DB Row", "ar": "سحب دمبل فردي", "sets": 3, "reps": "12", "inj": "Lower Back", "alt_en": "Face Pulls", "alt_ar": "سحب وجه"},
            {"en": "Face Pulls", "ar": "سحب وجه كيبل", "sets": 3, "reps": "15", "inj": "Rear Shoulder", "alt_en": "Reverse Flys", "alt_ar": "رفرفة خلفي"},
            {"en": "Barbell Curls", "ar": "تبادل بار باي", "sets": 3, "reps": "12", "inj": "Wrist/Forearm", "alt_en": "Hammer Curls", "alt_ar": "هامر دمبل"},
            {"en": "Hammer Curls", "ar": "هامر دمبل", "sets": 3, "reps": "12", "inj": "Wrist/Forearm", "alt_en": "Concentration Curls", "alt_ar": "تركيز باي"}
        ],
        "PUSH (Chest/Shoulders/Triceps)": [
            {"en": "Bench Press", "ar": "بنش برس مستوي", "sets": 4, "reps": "8", "inj": "Front Shoulder", "alt_en": "Floor Press", "alt_ar": "ضغط أرضي"},
            {"en": "Military Press", "ar": "ضغط كتف بار", "sets": 3, "reps": "10", "inj": "Side Shoulder", "alt_en": "Landmine Press", "alt_ar": "لاندمين برس"},
            {"en": "Incline DB Press", "ar": "تجميع عالي دمبل", "sets": 3, "reps": "12", "inj": "Front Shoulder", "alt_en": "Chest Press Machine", "alt_ar": "جهاز ضغط صدر"},
            {"en": "Lateral Raises", "ar": "رفرفة جانبي", "sets": 4, "reps": "15", "inj": "Side Shoulder", "alt_en": "Cable Lateral Raise", "alt_ar": "رفرفة كيبل"},
            {"en": "Tricep Pushdown", "ar": "تراي كيبل", "sets": 3, "reps": "15", "inj": "Elbow Joint", "alt_en": "Diamond Pushups", "alt_ar": "ضغط ضيق"},
            {"en": "Skullcrushers", "ar": "تراي بار نايم", "sets": 3, "reps": "12", "inj": "Elbow Joint", "alt_en": "Kickbacks", "alt_ar": "ركلة خلفية"},
            {"en": "Dips", "ar": "متوازي", "sets": 3, "reps": "Max", "inj": "Front Shoulder", "alt_en": "Tricep Extension", "alt_ar": "تراي فردي"}
        ],
        "LEGS (Lower Body)": [
            {"en": "Back Squat", "ar": "سكوات بار خلفي", "sets": 4, "reps": "8", "inj": "Knee Joint", "alt_en": "Leg Press", "alt_ar": "رجل هريس"},
            {"en": "RDL", "ar": "رفعة رومانية", "sets": 4, "reps": "10", "inj": "Lower Back", "alt_en": "Leg Curls", "alt_ar": "رجل خلفي"},
            {"en": "Leg Extension", "ar": "رجل أمامي جهاز", "sets": 3, "reps": "15", "inj": "Knee Joint", "alt_en": "Step Ups", "alt_ar": "صعود دكة"},
            {"en": "Leg Curls", "ar": "رجل خلفي جهاز", "sets": 3, "reps": "15", "inj": "Knee Joint", "alt_en": "Glute Bridges", "alt_ar": "جسر جلوتس"},
            {"en": "Bulgarian Split Squat", "ar": "سكوات بلغاري", "sets": 3, "reps": "10", "inj": "Knee Joint", "alt_en": "Goblet Squats", "alt_ar": "سكوات دمبل"},
            {"en": "Calf Raises", "ar": "سمانة واقف", "sets": 4, "reps": "20", "inj": "Ankle", "alt_en": "Seated Calf Raise", "alt_ar": "سمانة جالس"},
            {"en": "Plank", "ar": "بلانك", "sets": 3, "reps": "60s", "inj": "Lower Back", "alt_en": "Bird Dog", "alt_ar": "تمرين الكلب والطائر"}
        ]
    },
    "Bro Split (Classic)": {
         "CHEST DAY": [
            {"en": "Flat Bench Press", "ar": "بنش برس مستوي", "sets": 4, "reps": "10", "inj": "Front Shoulder", "alt_en": "Floor Press", "alt_ar": "ضغط أرضي"},
            {"en": "Incline DB Press", "ar": "تجميع عالي دمبل", "sets": 4, "reps": "10", "inj": "Front Shoulder", "alt_en": "Incline Flys", "alt_ar": "تفتيح عالي"},
            {"en": "Cable Cross", "ar": "كيبل كروس", "sets": 3, "reps": "15", "inj": "Front Shoulder", "alt_en": "Pec Deck", "alt_ar": "فراشة جهاز"},
            {"en": "Chest Press Machine", "ar": "جهاز ضغط صدر", "sets": 3, "reps": "12", "inj": "Front Shoulder", "alt_en": "Pushups", "alt_ar": "ضغط"},
            {"en": "Dips (Chest Focus)", "ar": "متوازي صدر", "sets": 3, "reps": "Max", "inj": "Front Shoulder", "alt_en": "Machine Flys", "alt_ar": "تفتيح جهاز"},
            {"en": "DB Flys", "ar": "تفتيح دمبل", "sets": 3, "reps": "15", "inj": "Front Shoulder", "alt_en": "Cable Cross High", "alt_ar": "كيبل عالي"},
            {"en": "Pushups", "ar": "ضغط", "sets": 3, "reps": "Max", "inj": "Wrist/Forearm", "alt_en": "Machine Press", "alt_ar": "جهاز ضغط"}
        ],
        "BACK DAY": [
            {"en": "Deadlift", "ar": "رفعة ميتة", "sets": 3, "reps": "5", "inj": "Lower Back", "alt_en": "Lat Pulldown", "alt_ar": "سحب عالي"},
            {"en": "T-Bar Row", "ar": "تي بار رو", "sets": 4, "reps": "10", "inj": "Lower Back", "alt_en": "Seated Rows", "alt_ar": "سحب أرضي"},
            {"en": "Lat Pulldown", "ar": "سحب عالي", "sets": 4, "reps": "12", "inj": "Shoulder Blade", "alt_en": "Seated Rows", "alt_ar": "سحب أرضي"},
            {"en": "One Arm DB Row", "ar": "سحب دمبل فردي", "sets": 3, "reps": "12", "inj": "Lower Back", "alt_en": "Face Pulls", "alt_ar": "سحب وجه"},
            {"en": "Seated Row", "ar": "سحب أرضي جهاز", "sets": 3, "reps": "12", "inj": "Lower Back", "alt_en": "Lat Pulldown", "alt_ar": "سحب عالي"},
            {"en": "Straight Arm Pulldown", "ar": "سحب ذراع مستقيم", "sets": 3, "reps": "15", "inj": "Rear Shoulder", "alt_en": "Face Pulls", "alt_ar": "سحب وجه"},
            {"en": "Hyper Extensions", "ar": "قطنية", "sets": 3, "reps": "15", "inj": "Lower Back", "alt_en": "Bird Dog", "alt_ar": "تمرين العصفور"}
        ]
    },
    "Upper/Lower Body": {
        "UPPER": [
            {"en": "Bench Press", "ar": "بنش برس", "sets": 4, "reps": "8", "inj": "Front Shoulder", "alt_en": "Floor Press", "alt_ar": "ضغط أرضي"},
            {"en": "Barbell Rows", "ar": "سحب بار", "sets": 4, "reps": "8", "inj": "Lower Back", "alt_en": "Seated Rows", "alt_ar": "سحب أرضي"},
            {"en": "Military Press", "ar": "ضغط كتف بار", "sets": 3, "reps": "10", "inj": "Side Shoulder", "alt_en": "Lateral Raises", "alt_ar": "رفرفة جانبي"},
            {"en": "Lat Pulldowns", "ar": "سحب عالي", "sets": 3, "reps": "12", "inj": "Shoulder Blade", "alt_en": "Seated Rows", "alt_ar": "سحب أرضي"},
            {"en": "Lateral Raises", "ar": "رفرفة جانبي", "sets": 3, "reps": "15", "inj": "Side Shoulder", "alt_en": "Face Pulls", "alt_ar": "سحب وجه"},
            {"en": "Bicep Curls", "ar": "باي بار", "sets": 3, "reps": "12", "inj": "Wrist/Forearm", "alt_en": "Hammer Curls", "alt_ar": "هامر دمبل"},
            {"en": "Tricep Extensions", "ar": "تراي كيبل", "sets": 3, "reps": "12", "inj": "Elbow Joint", "alt_en": "Diamond Pushups", "alt_ar": "ضغط ضيق"}
        ],
        "LOWER": [
            {"en": "Squats", "ar": "سكوات بار", "sets": 4, "reps": "8", "inj": "Knee Joint", "alt_en": "Leg Press", "alt_ar": "رجل هريس"},
            {"en": "RDL", "ar": "رفعة رومانية", "sets": 4, "reps": "10", "inj": "Lower Back", "alt_en": "Leg Curls", "alt_ar": "رجل خلفي"},
            {"en": "Leg Press", "ar": "رجل هريس", "sets": 3, "reps": "12", "inj": "Knee Joint", "alt_en": "Step Ups", "alt_ar": "صعود دكة"},
            {"en": "Leg Extensions", "ar": "رجل أمامي جهاز", "sets": 3, "reps": "15", "inj": "Knee Joint", "alt_en": "Lunges", "alt_ar": "طعن"},
            {"en": "Leg Curls", "ar": "رجل خلفي جهاز", "sets": 3, "reps": "15", "inj": "Knee Joint", "alt_en": "Glute Bridges", "alt_ar": "جسر جلوتس"},
            {"en": "Calf Raises", "ar": "سمانة واقف", "sets": 4, "reps": "20", "inj": "Ankle", "alt_en": "Seated Calf Raise", "alt_ar": "سمانة جالس"},
            {"en": "Deadbug", "ar": "ديد باج", "sets": 3, "reps": "12", "inj": "Lower Back", "alt_en": "Plank", "alt_ar": "بلانك"}
        ]
    }
}

# --- المرحلة الأولى: التسجيل (Registration) ---
if st.session_state.step == 'awakening':
    st.markdown(f'<div class="system-title"><h1>{L["title"]}</h1></div>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; color:#ff00ff; font-weight:bold;">{L["warning"]}</p>', unsafe_allow_html=True)
    
    u_name = st.text_input(L['name'], placeholder="...")
    c1, c2 = st.columns(2)
    u_gen = c1.selectbox(L['gen'], [L['male'], L['female']])
    u_path = c2.selectbox(L['path'], list(DB.keys()))
    
    u_inj = st.multiselect(L['inj'], ["Front Shoulder", "Side Shoulder", "Rear Shoulder", "Lower Back", "Shoulder Blade", "Knee Joint", "Elbow Joint", "Wrist/Forearm", "Ankle"])
    
    cw, ch = st.columns(2)
    u_w = cw.number_input(L['weight'], 40.0, 200.0, 80.0)
    u_h = ch.number_input(L['height'], 100.0, 250.0, 175.0)

    if st.button(L['btn_arise']):
        if u_name:
            bmi = u_w / ((u_h/100)**2)
            st.session_state.player = {"name": u_name, "path": u_path, "inj": u_inj, "bmi": round(bmi, 1), "gen": u_gen}
            st.session_state.step = 'mission'
            st.rerun()

# --- المرحلة الثانية: واجهة المهمات (Mission HUD) ---
elif st.session_state.step == 'mission':
    p = st.session_state.player
    st.markdown(f"""
        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <h2 style='color:#ff00ff; font-family:Orbitron; margin:0;'>{L['lvl']}. {st.session_state.level} | {p['name'].upper()}</h2>
            <div style='background:rgba(0,212,255,0.1); padding:5px 15px; border-radius:20px; border: 1px solid #00d4ff;'>{L['bmi']}: {p['bmi']}</div>
        </div>
        <div class='xp-bar-container'><div class='xp-bar-fill' style='width:{st.session_state.xp}%;'></div></div>
    """, unsafe_allow_html=True)

    day = st.selectbox(L['mission'], list(DB[p['path']].keys()))
    st.write("---")

    for idx, ex in enumerate(DB[p['path']][day]):
        is_inj = ex['inj'] in p['inj']
        
        # اختيار اسم التمرين بناءً على اللغة والحالة الصحية
        if st.session_state.lang == 'AR':
            display_name = ex['alt_ar'] if is_inj else ex['ar']
        else:
            display_name = ex['alt_en'] if is_inj else ex['en']
        
        st.markdown(f"""
            <div class="{'alt-card' if is_inj else 'exercise-card'}">
                <span style="font-weight:bold; font-size:18px;">{'🔄 ' if is_inj else '⚔️ '}{display_name}</span><br>
                <span style="color:#ff00ff; font-family:'Orbitron';">{ex['sets']} SETS x {ex['reps']} REPS</span>
                {f"<br><small style='color:#ff00ff;'>ADAPTED FOR {ex['inj']}</small>" if is_inj else ""}
            </div>
        """, unsafe_allow_html=True)

        c_inv, c_tmr = st.columns([2, 1])
        w_key = f"w_{p['path']}_{day}_{idx}"
        prev_w = st.session_state.inventory.get(w_key, "0")
        
        new_w = c_inv.text_input(f"{L['prev']}: {prev_w}kg", key=f"inp_{idx}")
        if new_w != "0" and new_w != prev_w: st.session_state.inventory[w_key] = new_w

        if c_tmr.button(f"⏱️ {L['rest']}", key=f"t_{idx}"):
            with st.empty():
                for i in range(60, 0, -1):
                    st.write(f"⌛ {i}s")
                    time.sleep(1)
                st.write(L['go'])

        if st.checkbox(L['clear'], key=f"ch_{idx}"):
            add_xp(15)

    if st.sidebar.button(L['reset']):
        st.session_state.step = 'awakening'
        st.rerun()
