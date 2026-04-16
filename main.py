import streamlit as st
import json
import os

# 1. إعدادات النظام (Solo Leveling UI)
st.set_page_config(page_title="ARISE SYSTEM", page_icon="🔥", layout="centered")

# 2. التصميم البصري (The Monarch Design)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* كارت الحالة الاحترافي */
    .status-card {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
        padding: 20px; border-radius: 10px; border: 2px solid #58a6ff;
        text-align: center; margin-bottom: 20px; box-shadow: 0px 0px 15px #58a6ff66;
    }
    
    /* أزرار العضلات (Body Map Simulation) */
    .stButton > button {
        width: 100%; height: 50px; background-color: #000000;
        color: #58a6ff; border: 1px solid #30363d; font-weight: bold;
        transition: 0.3s; text-transform: uppercase; letter-spacing: 1px;
    }
    .stButton > button:hover {
        border-color: #58a6ff; color: white; box-shadow: 0px 0px 10px #58a6ff;
        background-color: #0d1117;
    }
    
    /* كويست بوكس */
    .quest-item {
        background: #161b22; padding: 12px; border-radius: 5px;
        border-left: 4px solid #58a6ff; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. محرك البيانات (Data Engine) - معالجة الـ AttributeError
def init_system():
    default = {
        "name": "Unknown", "height": 175.0, "weight": 80.0, 
        "level": 1, "xp": 0, "rank": "E-Rank", 
        "initialized": False, "lang": "en"
    }
    if os.path.exists("progress.json"):
        try:
            with open("progress.json", "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    # دمج المفاتيح الناقصة
                    for k, v in default.items():
                        if k not in loaded: loaded[k] = v
                    return loaded
        except: pass
    return default

if 'user_data' not in st.session_state:
    st.session_state.user_data = init_system()

data = st.session_state.user_data

# 4. نظام الترجمة (Dual Language)
strings = {
    'en': {
        'title': 'SYSTEM INTERFACE', 'player': 'PLAYER', 'rank': 'RANK', 'lv': 'LEVEL',
        'map': 'BODY SCANNER: SELECT TARGET', 'chest': 'CHEST', 'back': 'BACK', 
        'legs': 'LEGS', 'shoulders': 'SHOULDERS', 'arms': 'ARMS', 'complete': 'QUEST COMPLETE',
        'awakening': 'AWAKENING FORM', 'start': 'START ASCENSION'
    },
    'ar': {
        'title': 'واجهة النظام', 'player': 'الصياد', 'rank': 'الرتبة', 'lv': 'المستوى',
        'map': 'ماسح الجسم: اختر العضلة', 'chest': 'الصدر', 'back': 'الظهر', 
        'legs': 'الأرجل', 'shoulders': 'الكتف', 'arms': 'الذراع', 'complete': 'إتمام المهمة',
        'awakening': 'نموذج الصحوة', 'start': 'بدء الارتقاء'
    }
}

L = strings[data['lang']]

# 5. القائمة الجانبية (Control Panel)
with st.sidebar:
    st.title("⚙️ SETTINGS")
    new_l = st.radio("Language", ["en", "ar"], index=0 if data['lang'] == 'en' else 1)
    if new_l != data['lang']:
        data['lang'] = new_l
        st.rerun()
    if st.button("RESET SYSTEM"):
        if os.path.exists("progress.json"): os.remove("progress.json")
        st.session_state.user_data = init_system()
        st.rerun()

# --- المرحلة 1: الصحوة (Initial Setup) ---
if not data['initialized']:
    st.markdown(f"<h1 style='text-align:center; color:#58a6ff;'>🔥 {L['awakening']}</h1>", unsafe_allow_html=True)
    with st.form("awakening"):
        name = st.text_input("CODE NAME")
        h = st.number_input("HEIGHT (cm)", value=175)
        w = st.number_input("WEIGHT (kg)", value=80)
        if st.form_submit_button(L['start']):
            data.update({"name": name, "height": h, "weight": w, "initialized": True})
            with open("progress.json", "w") as f: json.dump(data, f)
            st.rerun()
    st.stop()

# --- المرحلة 2: NEXUS (Main UI) ---
st.markdown(f"""
    <div class="status-card">
        <p style='color:#8b949e; margin:0; font-size:12px;'>{L['player']}</p>
        <h1 style='margin:0;'>{data['name'].upper()}</h1>
        <div style='display:flex; justify-content:space-around; margin-top:10px; color:#58a6ff;'>
            <b>{L['rank']}: {data['rank']}</b>
            <b>{L['lv']}: {data['level']}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# الـ XP Progress
st.progress(data['xp']/100)
st.write(f"XP: {data['xp']}/100")

st.divider()

# --- نظام الـ Body Map الذكي ---
st.write(f"### 🧭 {L['map']}")

# تصميم يشبه توزيع العضلات في الجسم
col1, col2, col3 = st.columns([1, 2, 1])

with col2: # أزرار في المنتصف تحاكي شكل الجسم
    if st.button(f"🦾 {L['shoulders']}"): target = "shoulders"
    elif st.button(f"🛡️ {L['chest']}"): target = "chest"
    elif st.button(f"⚔️ {L['back']}"): target = "back"
    elif st.button(f"🐍 {L['arms']}"): target = "arms"
    elif st.button(f"🦵 {L['legs']}"): target = "legs"
    else: target = None

# قاعدة بيانات التمارين
exercises = {
    "chest": [("Bench Press", 20), ("Incline DB", 15)],
    "back": [("Pull Ups", 20), ("Seated Rows", 15)],
    "shoulders": [("OHP", 15), ("Lateral Raises", 10)],
    "arms": [("Curls", 10), ("Extensions", 10)],
    "legs": [("Squats", 25), ("Leg Press", 20)]
}

if target:
    st.write(f"#### 📜 QUEST LOG: {L[target]}")
    for ex, xp in exercises[target]:
        st.markdown(f"<div class='quest-item'><b>{ex}</b> <span style='float:right; color:#58a6ff;'>+{xp} XP</span></div>", unsafe_allow_html=True)
    
    if st.button(f"🔥 {L['complete']}"):
        data['xp'] += sum(x[1] for x in exercises[target])
        if data['xp'] >= 100:
            data['xp'] = 0
            data['level'] += 1
            st.balloons()
        with open("progress.json", "w") as f: json.dump(data, f)
        st.success("SUCCESS: Progress Saved.")
        st.rerun()
