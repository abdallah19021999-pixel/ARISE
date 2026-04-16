import streamlit as st
import json
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="SYSTEM: ARISE", page_icon="⚡", layout="wide")

# 2. الـ CSS الاحترافي (The Monarch Aesthetic)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');

    /* تحويل الخلفية لعمق فضائي */
    .stApp {
        background: linear-gradient(135deg, #00050a 0%, #001220 100%);
        color: #e0f2ff;
    }

    /* تصميم النافذة الزجاجية (The Notification Box) */
    .glass-container {
        background: rgba(0, 20, 40, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.15);
        max-width: 600px;
        margin: auto;
    }

    /* تجميل الـ Inputs ومنعها من "التمدد" البايخ */
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: rgba(0, 0, 0, 0.5) !important;
        border: 1px solid #00d4ff !important;
        border-radius: 8px !important;
        width: 100% !important;
        margin-bottom: 15px;
    }
    
    /* جعل الخطوط متوهجة */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 15px #00d4ff;
        text-align: center;
        letter-spacing: 3px;
    }

    /* زرار الـ ARISE الاحترافي */
    .stButton > button {
        background: linear-gradient(90deg, #00d4ff, #0055ff);
        color: white;
        border: none;
        padding: 10px 40px;
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        border-radius: 50px;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        transition: 0.3s;
        display: block;
        margin: auto;
    }
    .stButton > button:hover {
        transform: scale(1.1);
        box-shadow: 0 0 40px #00d4ff;
    }

    /* إخفاء شريط التنقل الافتراضي لزيادة الاحترافية */
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات (نفس النظام المستقر)
def load_data():
    if os.path.exists("monarch_pro.json"):
        with open("monarch_pro.json", "r", encoding="utf-8") as f: return json.load(f)
    return {"initialized": False, "lang": "en", "lv": 1, "xp": 0}

if 'user' not in st.session_state:
    st.session_state.user = load_data()
user = st.session_state.user

# 4. واجهة "الصحوة" الاحترافية
if not user['initialized']:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="glass-container">
            <h1 style='font-size: 24px; color: #00d4ff;'>SYSTEM NOTIFICATION</h1>
            <p style='text-align:center; color: #888; font-family: "Cairo";'>أنت الآن مؤهل لتكون لاعباً في النظام</p>
            <hr style='border: 0.5px solid rgba(0, 212, 255, 0.2);'>
        </div>
    """, unsafe_allow_html=True)

    # وضع المدخلات داخل حاوية ضيقة (Centered)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("awakening"):
            u_name = st.text_input("CODE NAME", placeholder="Enter your name...")
            u_goal = st.selectbox("OBJECTIVE", ["HYPERTROPHY (Bulk)", "DEFINITION (Cut)"])
            
            c_inner1, c_inner2 = st.columns(2)
            u_weight = c_inner1.number_input("Weight", 40, 150, 80)
            u_height = c_inner2.number_input("Height", 120, 220, 175)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("ARISE"):
                if u_name:
                    user.update({
                        "name": u_name.upper(), "goal": u_goal, 
                        "w": u_weight, "h": u_height, "initialized": True
                    })
                    with open("monarch_pro.json", "w", encoding="utf-8") as f: json.dump(user, f)
                    st.rerun()

# 5. عرض الـ Status بعد الدخول (بشكل يشبه الصورة 3)
else:
    st.markdown(f"""
        <div class="glass-container">
            <h2 style='color:#ffcc00;'>STATUS: ACTIVE</h2>
            <h1 style='font-size: 40px;'>LEVEL {user['lv']}</h1>
            <p style='color:#00d4ff;'>PLAYER: {user['name']}</p>
            <div style='background:rgba(255,255,255,0.1); height:8px; width:100%; border-radius:10px;'>
                <div style='background:#00d4ff; height:100%; width:{user['xp']}%; box-shadow:0 0 10px #00d4ff; border-radius:10px;'></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("RESET SYSTEM"):
        os.remove("monarch_pro.json")
        st.session_state.clear()
        st.rerun()
