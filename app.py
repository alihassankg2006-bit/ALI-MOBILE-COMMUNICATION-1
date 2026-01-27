import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی بگ ٹائل ڈیزائن (CSS) - اب بٹنز خود ٹائلز بنیں گے
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 0.5rem !important; }
    .stApp { background-color: #ffffff; }
    
    /* ٹائل جیسا نظر آنے والا ڈبہ (حساب کے لیے) */
    .metric-card {
        height: 140px; border-radius: 20px;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        text-align: center; color: white !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.15);
        margin-bottom: 15px;
    }
    .m-label { font-size: 14px; font-weight: bold; text-transform: uppercase; }
    .m-val { font-size: 32px; font-weight: 900; }

    /* اصلی اسٹریم لٹ بٹنوں کو رنگین ڈبے بنانا */
    div.stButton > button {
        height: 140px !important;
        width: 100% !important;
        border-radius: 20px !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        color: white !important;
        border: none !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.15) !important;
        margin-bottom: 15px !important;
        display: flex; flex-direction: column; justify-content: center;
    }
    
    /* ہر بٹن اور ڈبے کا اپنا پکا رنگ */
    .bg-profit { background: linear-gradient(135deg, #1b5e20, #2e7d32); }
    .bg-repair { background: linear-gradient(135deg, #0d47a1, #1e88e5); }
    .bg-expense { background: linear-gradient(135deg, #b71c1c, #d32f2f); }
    .bg-banking { background: linear-gradient(135deg, #e65100, #ff9800); }

    /* بٹنوں کے رنگ */
    button[key="n"] { background: linear-gradient(135deg, #4a148c, #6a1b9a) !important; } /* Entry */
    button[key="c"] { background: linear-gradient(135deg, #006064, #00838f) !important; } /* Credit */
    button[key="h"] { background: linear-gradient(135deg, #c2185b, #ad1457) !important; } /* History */
    button[key="hm"] { background: linear-gradient(135deg, #263238, #37474f) !important; } /* Home */
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو سیکشن (واپسی)
cl1, cl2, cl3 = st.columns([1, 0.4, 1])
with cl2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<h2 style='text-align:center; color:#1b5e20;'>ALI MOBILES</h2>", unsafe_allow_html=True)

# 4. ڈیٹا ہینڈلنگ
DATA_FILE = "ali_shop_v22_final.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()
if 'page' not in st.session_state: st.session_state.page = "home"
def nav(p):
    st.session_state.page = p
    st.rerun()

# 5. حساب کتاب
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else df
cp = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
rep = t_df[t_df['کیٹیگری']=="Repairing"]['منافع'].sum()
he = t_df[t_df['کیٹیگری']=="Home Expense"]['فروخت'].sum()
bank = t_df[t_df['کیٹیگری']=="Banking"]['فروخت'].sum()

# --- 8 بڑے ڈبے (Metrics & Buttons) ---

# Row 1: انٹری اور پرافٹ
c1, c2 = st.columns(2)
with c1:
    if st.button("➕\nنئی انٹری\n(ENTRY)", key="n"): nav("new")
with c2:
    st.markdown(f"<div class='metric-card bg-green'><div class='m-label'>کل نقد پرافٹ</div><div class='m-val'>Rs. {cp}</div></div>", unsafe_allow_html=True)

# Row 2: ریپیرنگ اور کریڈٹ
c3, c4 = st.columns(2)
with c3:
    st.markdown(f"<div class='metric-card bg-blue'><div class='m-label'>ریپیرنگ پرافٹ</div><div class='m-val'>Rs. {rep}</div></div>", unsafe_allow_html=True)
with c4:
    if st.button("📓\nادھار لسٹ\n(CREDIT)", key="c"): nav("credit")

# Row 3: ایزی پیسہ اور ہسٹری
c5, c6 = st.columns(2)
with c5:
    st.markdown(f"<div class='metric-card bg-orange'><div class='m-label'>ایزی پیسہ سیل</div><div class='m-val'>Rs. {bank}</div></div>", unsafe_allow_html=True)
with c6:
    if st.button("📅\nہسٹری\n(HISTORY)", key="h"): nav("history")

# Row 4: خرچہ اور ہوم
c7, c8 = st.columns(2)
with c7:
    st.markdown(f"<div class='metric-card bg-expense'><div class='m-label'>گھر کا خرچ</div><div class='m-val'>Rs. {he}</div></div>", unsafe_allow_html=True)
with c8:
    if st.button("🏠\nہوم پیج\n(HOME)", key="hm"): nav("home")

st.divider()

# 6. پیجز (بٹن دبانے پر یہ نیچے کھلیں گے)
if st.session_state.page == "new":
    st.markdown("### 📝 نئی انٹری شامل کریں")
    with st.form("ali_form", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل درج کریں")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        v1, v2 = st.columns(2)
        cost = v1.number_input("خریداری (Cost)", min_value=0)
        sale = v2.number_input("فروخت (Sale)", min_value=0)
        if st.form_submit_button("💾 محفوظ کریں"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            nr = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": p, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([nr])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ ریکارڈ محفوظ ہو گیا!"); st.balloons(); nav("home")

elif st.session_state.page == "home":
    st.subheader("📋 آج کی سیل کا ریکارڈ")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    if not cl.empty:
        st.dataframe(cl, use_container_width=True)
        st.error(f"کل ادھار: Rs. {cl['فروخت'].sum()}")
    else: st.info("کوئی ادھار نہیں ہے۔")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ہسٹری")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
    
