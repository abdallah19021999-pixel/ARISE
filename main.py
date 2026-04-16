import streamlit as st
import json
import os
import datetime

# 1. إعدادات الصفحة (Mobile-First)
st.set_page_config(page_title="ARISE System", page_icon="🔥", layout="centered")

# 2. تصميم الـ CSS (الديزاين الغامق والاحترافي للأزرق والأسود)
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
        color: #58a6ff; border: 1px solid #30363d; height: 50px; font-weight: bold; margin-bottom: 10px;
    }
    .exercise-box { background: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #58a6ff; margin-top: 10px; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات مع معالجة الأخطاء
def load_data():
    default = {"name": "", "height": 175, "weight": 80, "level": 1, "xp": 0, "rank": "E-Rank", "initialized": False}
    if os.path.exists("progress.json"):
        with open("progress.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # التأكد من وجود كل المفاتيح
            for k, v in default.items():
                if k not in data: data[k] = v
            return data
    return default

if 'user_data' not in st.session_state:
    st.session_state.user_data = load_data()
data = st.session_state.user_data

# --- المرحلة الأولى: تسجيل المستخدم الجديد ---
if not data['initialized']:
    st.markdown("<h1 style='text-align: center;'>🔥 ARISE SYSTEM: Awakening</h1>", unsafe_allow_html=True)
    st.write("### أهلاً بك أيها الصياد.. سجل بياناتك لتبدأ الارتقاء:")
    
    with st.form("setup_form"):
        name = st.text_input("اسم الصياد (Player Name)")
        h = st.number_input("الطول (cm)", value=175)
        w = st.number_input("الوزن (kg)", value=80)
        if st.form_submit_button("إتمام الصحوة (Awaken)"):
            if name:
                data.update({"name": name, "height": h, "weight": w, "initialized": True})
                with open("progress.json", "w", encoding="utf-8") as f: json.dump(data, f)
                st.rerun()
            else:
                st.error("يرجى إدخال اسمك.")
    st.stop() # إيقاف الكود هنا لحين التسجيل

# --- المرحلة الثانية: واجهة التطبيق الرئيسية (بعد التسجيل) ---
st.markdown(f"""
    <div class="player-card">
        <h2 style='color: #58a6ff; margin:0;'>{data['name']}</h2>
        <p style='margin:0; color: #8b949e;'>رتبة: {data['rank']} | مستوي: {data['level']}</p>
    </div>
    """, unsafe_allow_html=True)

# شريط الخبرة
st.write(f"XP: {data['xp']} / 100")
st.progress(min(data['xp']/100, 1.0))

# حساب الـ BMI تلقائياً وعرضه
bmi = round(data['weight'] / ((data['height']/100)**2), 1)
status = "Normal" if 18.5 <= bmi < 25 else "Overweight" if bmi >= 25 else "Underweight"

col1, col2 = st.columns(2)
with col1:
    st.metric("BMI", bmi)
with col2:
    st.metric("الحالة", status)

st.divider()

# --- خريطة الجسم التفاعلية للتمارين (طلبك الأساسي) ---
st.write("### 🧭 اختر العضلة المستهدفة (Daily Quest)")
muscle_group = st.selectbox("العضلة:", ["اختر...", "الصدر (Chest)", "الظهر (Back)", "الكتف (Shoulders)", "الباي (Biceps)", "التراي (Triceps)", "الأرجل (Legs)", "الاستشفاء (Recovery)"])

# قاعدة بيانات التمارين والـ XP (بناءً على نظام PPL)
exercises_db = {
    "الصدر (Chest)": [("Bench Press", 20, "4x10"), ("Incline Dumbbell", 15, "3x12"), ("Chest Flys", 10, "3x15")],
    "الظهر (Back)": [("Lat Pulldown", 20, "4x12"), ("Seated Row", 15, "3x12"), ("Deadlift", 25, "1x5")],
    "الكتف (Shoulders)": [("Overhead Press", 15, "4x8"), ("Lateral Raises", 10, "3x15")],
    "الباي (Biceps)": [("Barbell Curls", 10, "3x12"), ("Hammer Curls", 10, "3x12")],
    "التراي (Triceps)": [("Pushdowns", 10, "3x12"), ("Overhead Ext", 10, "3x12")],
    "الأرجل (Legs)": [("Squats", 25, "4x8"), ("Leg Press", 20, "3x10"), ("Calves", 10, "3x15")],
}

if muscle_group != "اختر...":
    if muscle_group == "الاستشفاء (Recovery)":
        st.info("🧘 تم تفعيل بروتوكول الاستشفاء. قلل الأوزان بنسبة 50%.")
    else:
        st.write(f"#### التمارين المقترحة لعضلة {muscle_group}:")
        exercises = exercises_db[muscle_group]
        for name, xp, sets in exercises:
            st.markdown(f"""
                <div class="exercise-box">
                    <div style='display: flex; justify-content: space-between;'>
                        <span><b>{name}</b> ({sets})</span>
                        <span style='color: #58a6ff;'>+{xp} XP</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # زر لتسجيل إتمام التمرين
        if st.button(f"تم إتمام تدريب {muscle_group}!"):
            total_xp = sum(xp for _, xp, _ in exercises)
            data['xp'] += total_xp
            st.toast(f"تهانينا! حصلت على {total_xp} XP!")
            st.rerun()

# منطق الارتقاء (Level Up)
if data['xp'] >= 100:
    data['xp'] = 0
    data['level'] += 1
    # تغيير الرتبة تلقائياً
    if data['level'] >= 5 and data['rank'] == "E-Rank": data['rank'] = "D-Rank"
    elif data['level'] >= 10 and data['rank'] == "D-Rank": data['rank'] = "C-Rank"
    st.balloons()
    st.success(f"مبروك يا {data['name']}! ارتقيت للمستوى {data['level']}!")

# حفظ التغييرات
with open("progress.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# القائمة الجانبية للتعديلات
with st.sidebar:
    st.header("⚙️ الإعدادات")
    if st.button("🔄 إعادة ضبط النظام"):
        if os.path.exists("progress.json"):
            os.remove("progress.json")
        st.session_state.user_data = None
        st.rerun()
