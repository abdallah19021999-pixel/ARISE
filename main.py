import streamlit as st
import json
import os

# 1. إعدادات الصفحة (أولوية للموبايل وشكل الأنمي)
st.set_page_config(page_title="ARISE System v2.0", page_icon="🔥", layout="centered", initial_sidebar_state="collapsed")

# 2. تصميم الـ CSS المتقدم (شكل الأنمي الاحترافي - Solo Leveling Dark Mode)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* كارت الصياد الرئيسي */
    .player-header {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
        padding: 25px; border-radius: 12px; border: 2px solid #58a6ff;
        text-align: center; margin-bottom: 25px; box-shadow: 0px 0px 15px rgba(88, 166, 255, 0.4);
    }
    
    /* تصميم الـ Progress Bar */
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #1e90ff, #58a6ff); }
    
    /* تصميم الأزرار - سوداء بتنور أزرق */
    .stButton > button {
        width: 100%; height: 55px; border-radius: 5px; background-color: #000000;
        color: #58a6ff; border: 2px solid #161b22; font-weight: bold; transition: 0.3s;
    }
    .stButton > button:hover { border-color: #58a6ff; color: white; box-shadow: 0px 0px 10px #58a6ff; }
    
    /* صندوق التمارين (Quest Box) */
    .quest-box {
        background: #161b22; padding: 15px; border-radius: 8px;
        border: 1px solid #30363d; margin-top: 10px; border-right: 4px solid #58a6ff;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة اللغة (عربي / انجليزي)
translations = {
    'ar': {
        'awaken': 'تسجيل الصياد (Awakening)', 'player_data': 'بيانات الصياد',
        'quest_menu': 'نظام المهمات (Quest Menu)', 'select_muscle': 'حدد العضلة المستهدفة (Target)',
        'start_awakening': 'إتمام الصحوة (Awaken)', 'rank': 'الرتبة', 'level': 'المستوى',
        'chest': 'الصدر', 'back': 'الظهر', 'legs': 'الأرجل', 'shoulders': 'الكتف', 'arms': 'الذراع',
        'complete_quest': 'تم إتمام المهمة!', 'xp_gained': 'نقطة خبرة'
    },
    'en': {
        'awaken': 'Hunter Registration (Awakening)', 'player_data': 'Player Data',
        'quest_menu': 'Quest Menu', 'select_muscle': 'Select Target Muscle',
        'start_awakening': 'Start Awakening', 'rank': 'Rank', 'level': 'Level',
        'chest': 'Chest', 'back': 'Back', 'legs': 'Legs', 'shoulders': 'Shoulders', 'arms': 'Arms',
        'complete_quest': 'Quest Completed!', 'xp_gained': 'XP Gained'
    }
}

# 4. دالة إدارة البيانات (مع الفحص الشامل لمنع KeyError)
def load_data():
    default_data = {
        "name": "", "height": 175.0, "weight": 80.0, "level": 1,
        "xp": 0, "rank": "E-Rank", "initialized": False, "lang": "en"
    }
    if os.path.exists("progress.json"):
        try:
            with open("progress.json", "r", encoding="utf-8") as f:
                saved_data = json.load(f)
                # دمج ذكي: أي خانة ناقصة في الملف القديم تتضاف فوراً
                for key, value in default_data.items():
                    if key not in saved_data:
                        saved_data[key] = value
                return saved_data
        except: return default_data
    return default_data

def save_data(data):
    with open("progress.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'user_data' not in st.session_state:
    st.session_state.user_data = load_data()

data = st.session_state.user_data
# تأمين خانة اللغة قبل استخدامها
current_lang = data.get('lang', 'en')
T = translations[current_lang]

# 5. القائمة الجانبية (Settings)
with st.sidebar:
    st.header("⚙️ SYSTEM SETTINGS")
    new_lang = st.radio("Language / اللغة", ["en", "ar"], index=0 if current_lang == "en" else 1)
    if new_lang != current_lang:
        data['lang'] = new_lang
        save_data(data)
        st.rerun()
    
    if st.button("FORMAT SYSTEM (Reset)"):
        if os.path.exists("progress.json"): os.remove("progress.json")
        st.session_state.user_data = None
        st.rerun()

# --- المرحلة الأولى: تسجيل المستخدم (Awakening) ---
if not data.get('initialized', False):
    st.markdown(f"<h1 style='text-align: center; color:#58a6ff;'>🔥 ARISE SYSTEM <br>{T['awaken']}</h1>", unsafe_allow_html=True)
    with st.form("awakening_form"):
        name = st.text_input("Player Code Name")
        h = st.number_input("Height (cm)", value=175.0)
        w = st.number_input("Weight (kg)", value=80.0)
        if st.form_submit_button(T['start_awakening']):
            if name:
                data.update({"name": name, "height": h, "weight": w, "initialized": True})
                save_data(data)
                st.rerun()
    st.stop()

# --- المرحلة الثانية: الواجهة الرئيسية ---
st.markdown(f"""
    <div class="player-header">
        <p style='color: #8b949e; margin:0; font-size:12px;'>PLAYER IDENTITY</p>
        <h1 style='color: white; margin:0;'>{data['name'].upper()}</h1>
        <div style='display:flex; justify-content:space-around; color:#58a6ff; font-weight:bold; margin-top:10px;'>
            <span>{T['rank']}: {data['rank']}</span>
            <span>{T['level']}: {data['level']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# الـ BMI والتقدم
bmi = round(data['weight'] / ((data['height']/100)**2), 1)
st.progress(min(data['xp']/100, 1.0))
st.write(f"**XP Status:** {data['xp']}/100 | **BMI:** {bmi}")

st.divider()

# --- خريطة الجسم والتمارين ---
st.write(f"### 🧭 {T['select_muscle']}")

# عرض الأزرار كأنها خريطة اختيار عضلات
col1, col2 = st.columns(2)
with col1:
    btn_chest = st.button(f"🛡️ {T['chest']}")
    btn_back = st.button(f"⚔️ {T['back']}")
    btn_arms = st.button(f"🐍 {T['arms']}")
with col2:
    btn_shoulders = st.button(f"🦾 {T['shoulders']}")
    btn_legs = st.button(f"🍗 {T['legs']}")
    btn_reset_xp = st.button("🔄 Clear Quest")

# قاعدة بيانات التمارين
quests = {
    "chest": [("Bench Press", 20, "4x10"), ("Incline DB", 15, "3x12")],
    "back": [("Lat Pulldown", 20, "4x12"), ("Seated Row", 15, "3x12")],
    "shoulders": [("OHP", 15, "4x8"), ("Lateral Raise", 10, "3x15")],
    "arms": [("Pushdowns", 10, "3x12"), ("Bicep Curls", 10, "3x12")],
    "legs": [("Squats", 25, "4x8"), ("Leg Press", 20, "3x10")]
}

selected = None
if btn_chest: selected = "chest"
if btn_back: selected = "back"
if btn_shoulders: selected = "shoulders"
if btn_arms: selected = "arms"
if btn_legs: selected = "legs"

if selected:
    st.write(f"#### 📜 {T['quest_menu']}: {T[selected]}")
    for ex, xp, reps in quests[selected]:
        st.markdown(f"""
            <div class="quest-box">
                <div style='display:flex; justify-content:space-between;'>
                    <span><b>{ex}</b></span>
                    <span style='color:#58a6ff;'>+{xp} XP | {reps}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    if st.button(T['complete_quest']):
        total_xp = sum(x[1] for x in quests[selected])
        data['xp'] += total_xp
        st.toast(f"{T['complete_quest']} +{total_xp} XP")
        save_data(data)
        st.rerun()

# منطق الارتقاء
if data['xp'] >= 100:
    data['xp'] = 0
    data['level'] += 1
    if data['level'] >= 5: data['rank'] = "D-Rank"
    st.balloons()
    st.success(f"LEVEL UP! Welcome to Level {data['level']}")
    save_data(data)

st.markdown("<br><p style='text-align:center; color:#30363d;'>SYSTEM v2.0 - RANK S ACTIVE</p>", unsafe_allow_html=True)
