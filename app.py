import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی "8 ٹائلز" ڈیزائن (CSS)
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 0.5rem !important; }
    .stApp { background-color: #ffffff; }
    
    /* اوپر والے 4 ڈبوں (حساب) کا ڈیزائن */
    .metric-tile {
        height: 140px; 
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: white !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.2);
        margin-bottom: 10px;
        border: 2px solid rgba(255,255,255,0.1);
    }
    .t-name { font-size: 14px; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
    .t-data { font-size: 36px; font-weight: 900; }

    /* نیچے والے 4 ڈبوں (بٹنز) کا ڈیزائن - بالکل اوپر جیسا */
    div.stButton > button {
        height: 140px !important;
        width: 100% !important;
        border-radius: 20px !important;
        font-size: 22px !important;
        font-weight: 800 !important;
        color: white !important;
        border: none !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.2) !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-bottom: 10px !important;
        white-space: pre-wrap !important;
    }

    /* 8 الگ اور گہرے رنگ (Deep Professional Gradients) */
    .c1 { background: linear-gradient(135deg, #1b5e20, #2e7d32); } /* Profit */
    .c2 { background: linear-gradient(135deg, #0d47a1, #1565c0); } /* Repairing */
    .c3 { background: linear-gradient(135deg, #b71c1c, #d32f2f); } /* Expense */
    .c4 { background: linear-gradient(135deg, #e65100, #ff9800); } /* Banking */
    
    /* بٹنوں کے مخصوص رنگ */
    button[key="b_new"] { background: linear-gradient(135deg, #4a148c, #7b1fa2) !important; } /* Entry - Purple */
    button[key="b_cred"] { background: linear-gradient(135deg, #006064, #00838f) !important; } /* Credit - Teal */
    button[key="b_hist"] { background: linear-gradient(135deg, #c2185b, #ad1457) !important; } /* History - Pink */
    button[key="b_home"] { background: linear-gradient(135deg, #263238, #37474f) !important; } /* Home - Slate */

    /* ہوور ایفیکٹ */
    div.stButton > button:hover { transform: scale(0.98); opacity: 0.95; }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو سیکشن
cl1, cl2, cl3 = st.columns([1, 0.4, 1])
with cl2:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)

# 4. ڈیٹا مینجمنٹ
DATA_FILE = "ali_shop_v21_final.csv"
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

# 5. ڈیٹا کیلکولیشن
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else df
cp = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
rep = t_df[t_df['کیٹیگری']=="Repairing"]['منافع'].sum()
he = t_df[t_df['کیٹیگری']=="Home Expense"]['فروخت'].sum()
bank = t_df[t_df['کیٹیگری']=="Banking"]['فروخت'].sum()

# --- 8 بڑے رنگین ڈبے (2 Columns Grid) ---

# Row 1 (Metrics)
r1c1, r1c2 = st.columns(2)
with r1c1: st.markdown(f"<div class='metric-tile c1'><div class='t-name'>کل نقد پرافٹ</div><div class='t-data'>{cp}</div></div>", unsafe_allow_html=True)
with r1c2: st.markdown(f"<div class='metric-tile c2'><div class='t-name'>ریپیرنگ پرافٹ</div><div class='t-data'>{rep}</div></div>", unsafe_allow_html=True)

# Row 2 (Metrics)
r2c1, r2c2 = st.columns(2)
with r2c1: st.markdown(f"<div class='metric-tile c3'><div class='t-name'>گھر کا خرچ</div><div class='t-data'>{he}</div></div>", unsafe_allow_html=True)
with r2c2: st.markdown(f"<div class='metric-tile c4'><div class='t-name'>ایزی پیسہ سیل</div><div class='t-data'>{bank}</div></div>", unsafe_allow_html=True)

# Row 3 (Buttons - اب یہ بھی بڑے اور رنگین ہیں)
r3c1, r3c2 = st.columns(2)
with r3c1: 
    if st.button("➕\nنئی انٹری\n(ENTRY)", key="b_new"): nav("new")
with r3c2: 
    if st.button("📓\nادھار لسٹ\n(CREDIT)", key="b_cred"): nav("credit")

# Row 4 (Buttons)
r4c1, r4c2 = st.columns(2)
with r4c1: 
    if st.button("📅\nمکمل ہسٹری\n(HISTORY)", key="b_hist"): nav("history")
with r4_c2: 
    if st.button("🏠\nہوم پیج\n(HOME)", key="b_home"): nav("home")

st.divider()

# 6. پیجز کا ڈیٹا
if st.session_state.page == "home":
    st.subheader("📋 آج کی سیل کا ریکارڈ")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نیا ڈیٹا درج کریں")
    with st.form("ali_f"):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        v1, v2 = st.columns(2)
        cost = v1.number_input("لاگت (Cost)", min_value=0)
        sale = v2.number_input("وصولی (Sale)", min_value=0)
        if st.form_submit_button("محفوظ کریں"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            nr = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": p, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([nr])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("ریکارڈ محفوظ ہو گیا!"); nav("home")

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار کی لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    if not cl.empty:
        st.table(cl[["تاریخ", "تفصیل", "فروخت"]])
        st.error(f"کل ادھار: {cl['فروخت'].sum()} PKR")
    else: st.info("کوئی ادھار باقی نہیں ہے۔")

elif st.session_state.page == "history":
    st.subheader("📅 دکان کا مکمل ڈیٹا")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
    
