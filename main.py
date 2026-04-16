import streamlit as st
import json
import os

# 1. إعدادات الصفحة (Mobile-First)
st.set_page_config(page_title="ARISE System", page_icon="🔥", layout="centered")

# 2. تصميم الـ CSS (نفس الروح والديزاين اللي اخترناه)
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
    .stMetric { background-color: #161b22; padding: 10px; border-radius: 10px; border: 1px solid #30363d; }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        background-color: #21262d;
        color: #58a6ff;
        border: 1px solid #30363d;
        height: 50px;
        font-weight: bold;
    }
    .stButton > button:hover { border-color: #58a6ff; background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات (حفظ التقدم)
def load_data():
    if os.path.exists("progress.json"):
        try:
            with open("progress.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {"level": 1, "xp": 0, "rank": "E-Rank", "weight": 85.0, "height": 175.0}
    return {"level": 1, "xp": 0, "rank": "E-Rank", "weight": 85.0, "height": 175.0}

if 'user_data' not in st.session_state:
    st.session_state.user_data = load_data()
data = st.session_state.user_data

# 4. واجهة المستخدم (Header)
st.markdown(f"""
    <div class="player-card">
        <div style='display: flex; justify-content: space-between;'>
            <div>
                <p style='color: #8b949e; margin:0;'>PLAYER RANK</p>
                <h2 style='margin:0; color: #58a6ff;'>{data['rank']}</h2>
            </div>
            <div style='text-align: right;'>
                <p style='color: #8b949e; margin:0;'>LEVEL</p>
                <h2 style='margin:0;'>{data['level']}</h2>
            </div>
        </div>
        <p style='margin-bottom:5px; margin-top:15px; font-size:12px;'>XP: {data['xp']}/100</p>
    </div>
    """, unsafe_allow_html=True)

st.progress(min(data['xp']/100, 1.0))

# 5. حاسبة كتلة الجسم (BMI Calculator) - طلبك الجديد
st.write("### 📊 PHYSICAL STATUS")
with st.expander("تحديث بيانات الجسم (Weight & Height)"):
    new_weight = st.number_input("الوزن (kg)", value=float(data['weight']))
    new_height = st.number_input("الطول (cm)", value=float(data['height']))
    if st.button("تحديث وحساب BMI"):
        data['weight'] = new_weight
        data['height'] = new_height
        st.success("تم التحديث!")

# حساب الـ BMI
height_m = data['height'] / 100
bmi = round(data['weight'] / (height_m ** 2), 1)

col1, col2 = st.columns(2)
with col1:
    st.metric("BMI", bmi)
with col2:
    if bmi < 18.5: status = "Underweight"
    elif 18.5 <= bmi < 25: status = "Normal"
    elif 25 <= bmi < 30: status = "Overweight"
    else: status = "Obese"
    st.metric("Status", status)

st.divider()

# 6. نظام المهام (Active Quests)
st.write("### ⚔️ ACTIVE QUESTS")
col_a, col_b = st.columns(2)
with col_a:
    if st.button("🏋️ Chest Day"):
        data['xp'] += 20
        st.toast("XP +20 - استمر!")
    if st.button("🦵 Legs Day"):
        data['xp'] += 25
        st.toast("XP +25 - وحش!")
with col_b:
    if st.button("💪 Back Day"):
        data['xp'] += 20
        st.toast("XP +20 - ارتقِ!")
    if st.button("🧘 Recovery"):
        st.info("بروتوكول الاستشفاء مفعل")

# منطق الـ Level Up
if data['xp'] >= 100:
    data['xp'] = 0
    data['level'] += 1
    if data['level'] >= 5: data['rank'] = "D-Rank"
    st.balloons()
    st.success(f"لقد ارتقيت للمستوى {data['level']}!")

# حفظ البيانات
with open("progress.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

st.markdown("<p style='text-align:center; color:#8b949e; margin-top:30px;'>ARISE SYSTEM v1.2</p>", unsafe_allow_html=True)
