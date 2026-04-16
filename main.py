import streamlit as st
import json
import os

# 1. إعدادات تجعل الصفحة "موبايل" وتثبيت الألوان
st.set_page_config(page_title="ARISE System", page_icon="🔥", layout="centered")

# 2. الديزاين والألوان (CSS) - ده اللي بيخلي الشكل "أب" مش "ويب"
st.markdown("""
    <style>
    /* تغيير لون الخلفية للأسود العميق */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    /* تصميم كارت الحالة العلوي */
    .user-card {
        background: linear-gradient(135deg, #1e90ff 0%, #00008b 100%);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #4da6ff;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 4px 15px rgba(30, 144, 255, 0.3);
    }
    /* تصميم الأزرار لتشبه الموبايل */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 60px;
        background-color: #1a1a1a;
        color: #1e90ff;
        border: 2px solid #1e90ff;
        font-weight: bold;
        font-size: 18px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1e90ff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات
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

# 4. عرض الواجهة (الديزاين اللي اخترناه)
st.markdown(f"""
    <div class="user-card">
        <h1 style='margin:0; color:white;'>ARISE SYSTEM</h1>
        <p style='margin:5px; font-size:20px;'>الصياد: عبد الله</p>
        <div style='display:flex; justify-content:space-around; margin-top:10px;'>
            <span><b>الرتبة:</b> {data['rank']}</span>
            <span><b>المستوى:</b> {data['level']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# شريط الخبرة بالألوان
st.write("### الخبرة (XP)")
st.progress(min(data['xp'] / 100, 1.0))
st.write(f"🌟 {data['xp']} / 100")

st.divider()

# 5. الأزرار (الخريطة التفاعلية)
st.write("### 🧭 مهام التدريب اليومية")
col1, col2 = st.columns(2)

with col1:
    if st.button("🔥 الصدر"):
        data['xp'] += 20
        st.toast("تم تسجيل تمرين الصدر! +20 XP")
    if st.button("🦵 الأرجل"):
        data['xp'] += 25
        st.toast("تم تسجيل تمرين الأرجل! +25 XP")

with col2:
    if st.button("⚔️ الظهر"):
        data['xp'] += 20
        st.toast("تم تسجيل تمرين الظهر! +20 XP")
    if st.button("🛡️ استشفاء"):
        st.info("تم تفعيل وضع الراحة")

# منطق التطور
if data['xp'] >= 100:
    data['xp'] = 0
    data['level'] += 1
    st.balloons()
    st.success("ارتقيت لمستوى جديد!")

# حفظ البيانات
with open("progress.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
