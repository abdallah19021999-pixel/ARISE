import streamlit as st
import json
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="ARISE System", page_icon="🔥", layout="centered")

# 2. تصميم الـ CSS (الديزاين اللي اتفقنا عليه)
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .player-card {
        background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
        padding: 20px; border-radius: 15px; border: 1px solid #30363d;
        border-left: 5px solid #58a6ff; margin-bottom: 20px; text-align: center;
    }
    .stButton > button {
        width: 100%; border-radius: 10px; background-color: #21262d;
        color: #58a6ff; border: 1px solid #30363d; height: 50px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. دالة إدارة البيانات
def load_data():
    if os.path.exists("progress.json"):
        with open("progress.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return None # تعني مستخدم جديد

def save_data(data):
    with open("progress.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# تهيئة بيانات المستخدم
if 'user_data' not in st.session_state:
    st.session_state.user_data = load_data()

# --- المرحلة الأولى: تسجيل المستخدم الجديد ---
if st.session_state.user_data is None:
    st.markdown("<h1 style='text-align: center;'>🔥 ARISE: Awakening</h1>", unsafe_allow_html=True)
    st.write("### أهلاً بك أيها الصياد.. سجل بياناتك لتبدأ الارتقاء:")
    
    with st.form("setup_form"):
        name = st.text_input("اسم الصياد (Player Name)")
        height = st.number_input("الطول (cm)", value=170)
        weight = st.number_input("الوزن (kg)", value=70)
        submit = st.form_submit_button("ابدأ الارتقاء (Start Awakening)")
        
        if submit and name:
            new_data = {
                "name": name,
                "height": height,
                "weight": weight,
                "level": 1,
                "xp": 0,
                "rank": "E-Rank",
                "initialized": True
            }
            st.session_state.user_data = new_data
            save_data(new_data)
            st.rerun()
    st.stop() # إيقاف الكود هنا لحين التسجيل

# --- المرحلة الثانية: واجهة التطبيق الرئيسية (بعد التسجيل) ---
data = st.session_state.user_data

# كارت الحالة
st.markdown(f"""
    <div class="player-card">
        <h2 style='color: #58a6ff; margin:0;'>{data['name']}</h2>
        <p style='margin:0; color: #8b949e;'>رتبة: {data['rank']} | مستوي: {data['level']}</p>
    </div>
    """, unsafe_allow_html=True)

# شريط الخبرة
st.write(f"XP: {data['xp']} / 100")
st.progress(min(data['xp']/100, 1.0))

# حساب الـ BMI تلقائياً
bmi = round(data['weight'] / ((data['height']/100)**2), 1)
status = "Normal" if 18.5 <= bmi < 25 else "Overweight" if bmi >= 25 else "Underweight"

col1, col2 = st.columns(2)
col1.metric("BMI", bmi)
col2.metric("Status", status)

st.divider()

# نظام الكويستات (Quests)
st.write("### ⚔️ DAILY QUESTS")
c1, c2 = st.columns(2)
with c1:
    if st.button("🏋️ تمرين الصدر"):
        data['xp'] += 20
        st.toast("XP +20 - لقد اقتربت من الارتقاء!")
with c2:
    if st.button("💪 تمرين الظهر"):
        data['xp'] += 20
        st.toast("XP +20 - وحش!")

# منطق الارتقاء (Level Up)
if data['xp'] >= 100:
    data['xp'] = 0
    data['level'] += 1
    if data['level'] >= 5: data['rank'] = "D-Rank"
    st.balloons()
    st.success(f"مبروك يا {data['name']}! ارتقيت للمستوى {data['level']}")

# حفظ التغييرات
save_data(data)

# القائمة الجانبية للتعديلات
with st.sidebar:
    st.header("⚙️ الإعدادات")
    if st.button("🔄 إعادة ضبط النظام"):
        if os.path.exists("progress.json"):
            os.remove("progress.json")
        st.session_state.user_data = None
        st.rerun()
