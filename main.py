import streamlit as st
import json
import os

# 1. إعدادات الصفحة (تصحيح كل أخطاء السنتكس السابقة)
st.set_page_config(
    page_title="ARISE: Solo Leveling System",
    page_icon="🔥",
    layout="centered"
)

# 2. وظائف إدارة البيانات (حفظ التقدم)
def load_data():
    if os.path.exists("progress.json"):
        try:
            with open("progress.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"rank": "E-Rank", "level": 1, "xp": 0, "injuries": []}
    return {"rank": "E-Rank", "level": 1, "xp": 0, "injuries": []}

def save_data(data):
    with open("progress.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# تهيئة بيانات الجلسة
if 'user_data' not in st.session_state:
    st.session_state.user_data = load_data()

data = st.session_state.user_data

# 3. واجهة المستخدم (Header)
st.markdown("<h1 style='text-align: center; color: #1E90FF;'>🔥 ARISE: نظام الارتقاء الذاتي</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center;'>الصياد: عبد الله | الرتبة: {data['rank']} | المستوى: {data['level']}</h3>", unsafe_allow_html=True)

# شريط الخبرة التفاعلي
xp_progress = min(data['xp'] / 100, 1.0)
st.progress(xp_progress)
st.write(f"💪 نقاط الخبرة الحالية: {data['xp']} / 100")

st.divider()

# 4. الخريطة التفاعلية للتمارين
st.write("### 🧭 الخريطة التفاعلية - اختر عضلتك اليوم:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("الصدر (Chest)"):
        st.info("💡 التمارين: Chest Press + Pushups (3x12)")
        data['xp'] += 20
        st.toast("تم إضافة 20 XP لتدريب الصدر!")

with col2:
    if st.button("الظهر (Back)"):
        st.info("💡 التمارين: Lat Pulldown + Seated Row (4x10)")
        data['xp'] += 20
        st.toast("تم إضافة 20 XP لتدريب الظهر!")

with col3:
    if st.button("الأرجل (Legs)"):
        st.info("💡 التمارين: Leg Press + Squats (3x15)")
        data['xp'] += 25
        st.toast("تم إضافة 25 XP لتدريب الأرجل!")

# 5. منطق الارتقاء (Level Up Logic)
if data['xp'] >= 100:
    data['xp'] = 0
    data['level'] += 1
    # تغيير الرتبة تلقائياً عند الوصول لمستوى معين
    if data['level'] >= 5 and data['rank'] == "E-Rank":
        data['rank'] = "D-Rank"
    elif data['level'] >= 10 and data['rank'] == "D-Rank":
        data['rank'] = "C-Rank"
        
    st.balloons()
    st.success(f"✨ مبروك! ارتقيت للمستوى {data['level']}!")

# حفظ الحالة بعد كل ضغطة
st.session_state.user_data = data
save_data(data)

# 6. مركز الاستشفاء والإصابات (Sidebar)
with st.sidebar:
    st.header("🛡️ مركز الاستشفاء")
    st.write("أبلغ عن ألم لتعديل خطتك فوراً:")
    injury = st.selectbox("مكان الألم:", ["لا يوجد", "الظهر", "الركبة", "الكتف"])
    
    if injury != "لا يوجد":
        st.warning(f"⚠️ بروتوكول حماية: تجنب الأوزان الثقيلة لعضلة {injury} واتبع تمارين التأهيل.")
    
    st.divider()
    if st.button("🔄 إعادة ضبط النظام (Reset)"):
        st.session_state.user_data = {"rank": "E-Rank", "level": 1, "xp": 0, "injuries": []}
        save_data(st.session_state.user_data)
        st.rerun()

    st.write("---")
    st.caption("نظام ARISE - النسخة التجريبية 1.0")
