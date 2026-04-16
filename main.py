import streamlit as st
import json
import os

# 1. إعدادات تجعل الصفحة تبدو كالموبايل
st.set_page_config(
    page_title="ARISE App",
    page_icon="🔥",
    layout="centered", # تجعل المحتوى في المنتصف كشاشة الموبايل
    initial_sidebar_state="collapsed" # إخفاء القائمة الجانبية لتوفير مساحة
)

# 2. وظائف البيانات
def load_data():
    if os.path.exists("progress.json"):
        try:
            with open("progress.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {"rank": "E-Rank", "level": 1, "xp": 0}
    return {"rank": "E-Rank", "level": 1, "xp": 0}

if 'user_data' not in st.session_state:
    st.session_state.user_data = load_data()
data = st.session_state.user_data

# 3. واجهة الموبايل (التنسيق)
# نستخدم CSS لجعل الواجهة تشبه التطبيق
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 3em;
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #3d3d3d;
    }
    .status-card {
        background: linear-gradient(135deg, #1e90ff, #00bfff);
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# كارت الحالة (Status Card)
st.markdown(f"""
    <div class="status-card">
        <h2 style='margin:0;'>عبد الله</h2>
        <p style='margin:0;'>رتبة: {data['rank']} | مستوي: {data['level']}</p>
    </div>
    """, unsafe_allow_html=True)

# شريط الخبرة
st.write("XP Progress")
st.progress(min(data['xp'] / 100, 1.0))

st.write("### ⚡ Daily Quests (المهام)")

# تقسيم المهام لأزرار تشبه الـ App Widgets
c1, c2 = st.columns(2)
with c1:
    if st.button("🏋️ الصدر"):
        data['xp'] += 20
        st.toast("XP +20")
    if st.button("🍗 الأرجل"):
        data['xp'] += 25
        st.toast("XP +25")

with c2:
    if st.button("💪 الظهر"):
        data['xp'] += 20
        st.toast("XP +20")
    if st.button("🍎 تغذية"):
        st.toast("سجل وجبتك")

# منطق الارتقاء
if data['xp'] >= 100:
    data['xp'] = 0
    data['level'] += 1
    st.balloons()
    st.session_state.user_data = data

# الحفظ
with open("progress.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
