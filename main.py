import streamlit as st
import json
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="ARISE System", page_icon="🔥", layout="centered")

# 2. تصميم الـ CSS المتقدم (Dark App Theme)
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #ffffff; }
    .player-card {
        background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #30363d;
        border-left: 5px solid #58a6ff;
        margin-bottom: 20px;
    }
    .stButton > button {
        width: 100%; border-radius: 10px; background-color: #21262d;
        color: #58a6ff; border: 1px solid #30363d; height: 50px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات مع معالجة الأخطاء (التعديل هنا لرفع الـ KeyError)
def load_data():
    default_data = {"level": 1, "xp": 0, "rank": "E-Rank", "weight": 85.0, "height": 175.0}
    if os.path.exists("progress.json"):
        try:
            with open("progress.json", "r", encoding="utf-8") as f:
                saved_data = json.load(f)
                # دمج البيانات القديمة مع الافتراضية لضمان عدم نقص أي مفتاح (Key)
                for key in default_data:
                    if key not in saved_data:
                        saved_data[key] = default_data[key]
                return saved_data
        except: return default_data
    return default_data

if 'user_data' not in st.session_state:
    st.session_state.user_data = load_data()
data = st.session_state.user_data

# 4. واجهة المستخدم العلوي
st.markdown(f"""
    <div class="player-card">
        <div style='display: flex; justify-content: space-between;'>
            <div><p style='color: #8b949e; margin:0;'>RANK</p><h2 style='margin:0; color: #58a6ff;'>{data['rank']}</h2></div>
            <div style='text-align: right;'><p style='color: #8b949e; margin:0;'>LEVEL</p><h2 style='margin:0;'>{data['level']}</h2></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.progress(min(data['xp']/100, 1.0))

# 5. حاسبة الـ BMI والبيانات الجسمانية
st.write("### 📊 PHYSICAL STATUS")
with st.expander("تعديل بيانات الجسم"):
    # استخدام .get لضمان عدم حدوث الخطأ مرة أخرى
    w = st.number_input("الوزن (kg)", value=float(data.get('weight', 85.0)))
    h = st.number_input("الطول (cm)", value=float(data.get('height', 175.0)))
    if st.button("حفظ البيانات"):
        data['weight'], data['height'] = w, h
        st.success("تم التحديث!")

# حساب الـ BMI
bmi = round(data['weight'] / ((data['height']/100)**2), 1)
c1, c2 = st.columns(2)
c1.metric("BMI", bmi)
status = "Normal" if 18.5 <= bmi < 25 else "Overweight" if bmi >= 25 else "Underweight"
c2.metric("Status", status)

st.divider()

# 6. نظام المهام
st.write("### ⚔️ ACTIVE QUESTS")
col_a, col_b = st.columns(2)
with col_a:
    if st.button("🏋️ Chest Day"):
        data['xp'] += 20
        st.toast("XP +20")
with col_b:
    if st.button("💪 Back Day"):
        data['xp'] += 20
        st.toast("XP +20")

# منطق الـ Level Up وحفظ البيانات
if data['xp'] >= 100:
    data['xp'], data['level'] = 0, data['level'] + 1
    if data['level'] >= 5: data['rank'] = "D-Rank"
    st.balloons()

with open("progress.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
