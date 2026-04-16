import streamlit as st
import json
import os
import time

# 1. إعدادات الصفحة (أولوية للموبايل وشكل الأنمي)
st.set_page_config(page_title="ARISE System v2.0", page_icon="🔥", layout="centered", initial_sidebar_state="collapsed")

# 2. تصميم الـ CSS المتقدم (للحصول على شكل الأنمي الاحترافي فشخ)
st.markdown("""
    <style>
    /* تغيير الخلفية للأسود القاتم */
    .stApp {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Courier New', Courier, monospace; /* خط يشبه شاشات الأوامر */
    }
    /* تصميم كارت الصياد (Header) */
    .player-header {
        background: linear-gradient(180deg, rgba(0,0,0,1) 0%, rgba(22,27,34,1) 100%);
        padding: 30px;
        border-radius: 10px;
        border: 2px solid #58a6ff;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 0px 20px rgba(88, 166, 255, 0.5);
    }
    /* تصميم الـ Progress Bar لتكون باللون الأزرق */
    .stProgress > div > div > div > div { background-color: #58a6ff; }
    
    /* تصميم أزرار العضلات (Body Map) لتكون سوداء بالكامل */
    .stButton > button {
        width: 100%;
        height: 60px;
        border-radius: 0px; /* زوايا قائمة لشكل النظام */
        background-color: #000000;
        color: #8b949e;
        border: 2px solid #161b22;
        font-weight: bold;
        transition: 0.3s;
        text-transform: uppercase;
    }
    /* الأزرار تنور أزرق عند اللمس والاختيار */
    .stButton > button:hover, .stButton > button:focus {
        border-color: #58a6ff;
        color: white;
        background-color: #0d1117;
        box-shadow: 0px 0px 15px rgba(88, 166, 255, 0.7);
    }
    /* تصميم صندوق التمارين */
    .quest-box {
        background: rgba(22,27,34,0.7);
        padding: 20px;
        border-radius: 5px;
        border: 1px solid #30363d;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة اللغة (عربي / انجليزي)
translations = {
    'ar': {
        'awaken': 'تسجيل الصياد (Awakening)',
        'player_data': 'بيانات الصياد',
        'quest_menu': 'نظام المهمات (Quest Menu)',
        'select_muscle': 'حدد العضلة المستهدفة (Target)',
        'start_awakening': 'إتمام الصحوة (Start Awakening)',
        'chest': 'الصدر', 'back': 'الظهر', 'legs': 'الأرجل', 'shoulders': 'الكتف', 'arms': 'الذراع',
        'complete_quest': 'تم إتمام المهمة!', 'xp_gained': 'XP مكتسب'
    },
    'en': {
        'awaken': 'Hunter Registration (Awakening)',
        'player_data': 'Player Data',
        'quest_menu': 'Quest Menu',
        'select_muscle': 'Select Target Muscle',
        'start_awakening': 'Start Awakening',
        'chest': 'Chest', 'back': 'Back', 'legs': 'Legs', 'shoulders': 'Shoulders', 'arms': 'Arms',
        'complete_quest': 'Quest Completed!', 'xp_gained': 'XP Gained'
    }
}

# 4. دالة إدارة البيانات مع نظام "الفحص الذكي" لرفع الـ KeyError
def load_data():
    default_data = {
        "name": "", "height": 175.0, "weight": 80.0, "level": 1,
        "xp": 0, "rank": "E-Rank", "initialized": False, "lang": "en"
    }
    if os.path.exists("progress.json"):
        try:
            with open("progress.json", "r", encoding="utf-8") as f:
                saved_data = json.load(f)
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
T = translations[data['lang']]

# 5. القائمة الجانبية لإعدادات اللغة وReset
with st.sidebar:
    st.header("SYSTEM SETTINGS")
    lang = st.radio("System Language", ["en", "ar"], index=0 if data['lang'] == "en" else 1)
    if lang != data['lang']:
        data['lang'] = lang
        save_data(data)
        st.rerun()
    
    if st.button("FORMAT SYSTEM (Reset)"):
        if os.path.exists("progress.json"):
            os.remove("progress.json")
        st.session_state.user_data = None
        st.rerun()

# --- المرحلة الأولى: تسجيل المستخدم الجديد (The Awakening) ---
if not data.get('initialized', False):
    st.markdown(f"<h1 style='text-align: center; color:#58a6ff;'>🔥 ARISE SYSTEM: <br>{T['awaken']}</h1>", unsafe_allow_html=True)
    
    with st.form("awakening_form"):
        name = st.text_input("Player Name", placeholder="Input your code name...")
        h = st.number_input("Height (cm)", value=175.0)
        w = st.number_input("Weight (kg)", value=80.0)
        submit = st.form_submit_button(T['start_awakening'])
        
        if submit and name:
            data.update({"name": name, "height": h, "weight": w, "initialized": True})
            save_data(data)
            st.rerun()
    st.stop()

# --- المرحلة الثانية: واجهة التطبيق الرئيسية (NEXUS) ---
# كارت الصياد (Header)
st.markdown(f"""
    <div class="player-header">
        <p style='color: #8b949e; margin:0;'>PLAYER</p>
        <h1 style='color: white; margin:0;'>{data['name'].upper()}</h1>
        <div style='display:flex; justify-content:space-around; color:#58a6ff; font-weight:bold; margin-top:10px;'>
            <span>RANK: {data['rank']}</span>
            <span>LEVEL: {data['level']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# شريط الخبرة (XP)
st.progress(min(data['xp']/100, 1.0))
st.write(f"XP Status: {data['xp']}/100 [ {min(data['xp']/100, 1.0)*100}% ]")

st.divider()

# --- خريطة الجسم التفاعلية (The 3D Nexus) ---طلبك الأساسي
st.write(f"### 🧭 {T['select_muscle']}")

# حيلة لاستخدام صور عالية الجودة كخريطة جسم بديلة للـ 3D الحقيقي
col_img, col_menu = st.columns([2, 1])

with col_img:
    # هنا هنحط صورة المجسم الـ 3D الأساسية (استبدل الرابط بصورتك لو عايز)
    st.image("https://via.placeholder.com/400x600/000000/58a6ff?text=3D+BODY+MAP+(Nexus)")

with col_menu:
    chest_btn = st.button(f"🛡️ {T['chest']}")
    back_btn = st.button(f"⚔️ {T['back']}")
    legs_btn = st.button(f"🍗 {T['legs']}")
    sh_btn = st.button(f"🦾 {T['shoulders']}")
    arms_btn = st.button(f"🐍 {T['arms']}")

# نظام المهمات الذكي (Smart Quest System)
if chest_btn:
    data['xp'] += 20
    st.markdown(f"<div class='quest-box'><b>Current Quest:</b><br>- Bench Press (4x10)<br>- Incline Dumbbell (3x12)<br><span style='color:#58a6ff;'>+20 XP Gained!</span></div>", unsafe_allow_html=True)
    st.toast("Quest Log Updated: +20 XP")

if back_btn:
    data['xp'] += 20
    st.markdown(f"<div class='quest-box'><b>Current Quest:</b><br>- Lat Pulldown (4x12)<br>- Seated Row (3x12)<br><span style='color:#58a6ff;'>+20 XP Gained!</span></div>", unsafe_allow_html=True)

if legs_btn:
    data['xp'] += 25
    st.markdown(f"<div class='quest-box'><b>Current Quest:</b><br>- Squats (4x8)<br>- Leg Press (3x10)<br><span style='color:#58a6ff;'>+25 XP Gained!</span></div>", unsafe_allow_html=True)

if sh_btn:
    data['xp'] += 15
    st.markdown(f"<div class='quest-box'><b>Current Quest:</b><br>- Overhead Press (4x8)<br>- Lateral Raises (3x15)<br><span style='color:#58a6ff;'>+15 XP Gained!</span></div>", unsafe_allow_html=True)

if arms_btn:
    data['xp'] += 15
    st.markdown(f"<div class='quest-box'><b>Current Quest:</b><br>- Pushdowns (Triceps) (3x12)<br>- Hammer Curls (Biceps) (3x12)<br><span style='color:#58a6ff;'>+15 XP Gained!</span></div>", unsafe_allow_html=True)

# منطق الارتقاء (Level Up)
if data['xp'] >= 100:
    data['xp'] = 0
    data['level'] += 1
    # تغيير الرتبة تلقائياً
    if data['level'] >= 5 and data['rank'] == "E-Rank": data['rank'] = "D-Rank"
    elif data['level'] >= 10 and data['rank'] == "D-Rank": data['rank'] = "C-Rank"
    st.balloons()
    st.success(f"مبروك! لقد ارتقيت للمستوى {data['level']}!")

# حفظ التغييرات
save_data(data)
