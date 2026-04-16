import streamlit as st
import json
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="ARISE System", page_icon="🔥", layout="centered")

# 2. تصميم الـ CSS (الديزاين الاحترافي Dark Mode)
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
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# 3. دالة إدارة البيانات مع نظام "الفحص الذكي"
def load_data():
    default_data = {
        "name": "الصياد الجديد",
        "height": 175.0,
        "weight": 80.0,
        "level": 1,
        "xp": 0,
        "rank": "E-Rank",
        "initialized": False
    }
    if os.path.exists("progress.json"):
        try:
            with open("progress.json", "r", encoding="utf-8") as f:
                saved_data = json.load(f)
                # التأكد من وجود كل المفاتيح (عشان نتجنب KeyError)
                for key, value in default_data.items():
                    if key not in saved_data:
                        saved_data[key] = value
                return saved_data
        except:
            return default_data
    return default_data

def save_data(data):
    with open("progress.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# تهيئة البيانات
if 'user_data' not in st.session_state:
    st.session_state.user_data = load_data()

data = st.session_state.user_data

# --- المرحلة الأولى: التسجيل الأول (لو initialized = False) ---
if not data.get('initialized', False):
    st.markdown("<h1 style='text-align: center;'>🔥 ARISE: Awakening</h1>", unsafe_allow_html=True)
    st.write("### أهلاً بك في نظام الارتقاء.. سجل بياناتك لتبدأ:")
    
    with st.form("awakening_form"):
        name = st.text_input("اسمك (Player Name)", placeholder="ادخل اسمك هنا...")
        h = st.number_input("طولك (cm)", min_value=100, max_value=250, value=175)
        w = st.number_input("وزنك (kg)", min_value=30, max_value=250, value=80)
        submit = st.form_submit_button("إتمام الصحوة (Awaken)")
        
        if submit and name:
            data.update({
                "name": name,
                "height": h,
                "weight": w,
                "initialized": True
            })
            save_data(data)
            st.rerun()
    st.stop()

# --- المرحلة الثانية: واجهة التطبيق الرئيسية ---
st.markdown(f"""
    <div class="player-card">
        <h2 style='color: #58a6ff; margin:0;'>{data['name']}</h2>
        <p style='margin:0; color: #8b949e;'>رتبة: {data['rank']} | مستوى: {data['level']}</p>
    </div>
    """, unsafe_allow_html=True)

# شريط الخبرة
st.write(f"XP: {data['xp']} / 100")
st.progress(min(data['xp']/100, 1.0))

# حساب الـ BMI تلقائياً
bmi = round(data['weight'] / ((data['height']/100)**2), 1)
status = "Normal" if 18.5 <= bmi < 25 else "Overweight" if bmi >= 25 else "Underweight"

col1, col2 = st.columns(2)
with col1:
    st.metric("BMI", bmi)
with col2:
    st.metric("الحالة", status)

st.divider()

# نظام المهام (Daily Quests)
st.write("### ⚔️ ACTIVE QUESTS")
c1, c2 = st.columns(2)
with c1:
    if st.button("🏋️ تمرين الصدر"):
        data['xp'] += 20
        st.toast("XP +20 - استمر يا بطل!")
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

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ الإعدادات")
    if st.button("🔄 إعادة ضبط النظام"):
        if os.path.exists("progress.json"):
            os.remove("progress.json")
        st.session_state.user_data = None
        st.rerun()
