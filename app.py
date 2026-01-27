import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی بگ ٹائل ڈیزائن (CSS)
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 0.5rem !important; }
    .stApp { background-color: #ffffff; }
    
    /* میٹرک ڈبوں کا ڈیزائن (پہلے 4 ڈبے) */
    .big-tile {
        height: 140px; 
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: white !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.2);
        margin-bottom: 15px;
    }
    .tile-name { font-size: 13px; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
    .tile-data { font-size: 34px; font-weight: 900; }

    /* مینو بٹنوں کا ڈیزائن (نیچے والے 4 ڈبے) */
    div.stButton > button {
        height: 140px !important;
        width: 100% !important;
        border-radius: 20px !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        color: white !important;
        border: none !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.2) !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-bottom: 15px !important;
        white-space: pre-wrap !important; /* نام کو ڈبے کے اندر سیٹ کرنے کے لیے */
    }

    /* 8 گہرے اور مستقل رنگ (Deep Solid Colors) */
    .bg-green { background: linear-gradient(135deg, #1b5e20, #2e7d32); } /* پرافٹ */
    .bg-blue { background: linear-gradient(135deg, #0d47a1, #1e88e5); }  /* ریپیرنگ */
    .bg-red { background: linear-gradient(135deg, #b71c1c, #d32f2f); }   /* خرچہ */
    .bg-orange { background: linear-gradient(135deg, #e65100, #ff9800); } /* بینکنگ */
    
    /* بٹنوں کے مخصوص گہرے رنگ */
    button[key="btn_new"] { background: linear-gradient(135deg, #4a148c, #6a1b9a) !important; } /* انٹری - جامنی */
    button[key="btn_credit"] { background: linear-gradient(135deg, #006064, #00838f) !important; } /* کریڈٹ - ٹیل */
    button[key="btn_hist"] { background: linear-gradient(135deg, #c2185b, #ad1457) !important; } /* ہسٹری - گلابی */
    button[key="btn_home"] { background: linear-gradient(135deg, #263238, #37474f) !important; } /* ہوم - سلیٹی */

    /* بٹن ہوور ایفیکٹ */
    div.stButton > button:hover { transform: scale(0.98); opacity: 0.95; }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو (صرف اگر فائل موجود ہو)
cl1, cl2, cl3 = st.columns([1, 0.4, 1])
with cl2:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)

# 4. ڈیٹا ہینڈلنگ
DATA_FILE = "ali_shop_v20_final.csv"
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

# --- 8 بڑے رنگین ڈبے (2 Columns) ---

# پہلی قطار (حساب)
r1_c1, r1_c2 = st.columns(2)
with r1_c1: st.markdown(f"<div class='big-tile bg-green'><div class='tile-name'>کل نقد پرافٹ</div><div class='tile-data'>{cp}</div></div>", unsafe_allow_html=True)
with r1_c2: st.markdown(f"<div class='big-tile bg-blue'><div class='tile-name'>ریپیرنگ پرافٹ</div><div class='tile-data'>{rep}</div></div>", unsafe_allow_html=True)

# دوسری قطار (حساب)
r2_c1, r2_c2 = st.columns(2)
with r2_c1: st.markdown(f"<div class='big-tile bg-red'><div class='tile-name'>گھر کا خرچ</div><div class='tile-data'>{he}</div></div>", unsafe_allow_html=True)
with r2_c2: st.markdown(f"<div class='big-tile bg-orange'><div class='tile-name'>ایزی پیسہ سیل</div><div class='tile-data'>{bank}</div></div>", unsafe_allow_html=True)

# تیسری قطار (بٹن - اب یہ بھی بڑے اور رنگین ہیں)
r3_c1, r3_c2 = st.columns(2)
with r3_c1: 
    if st.button("➕\nنئی انٹری\n(NEW ENTRY)", key="btn_new"): nav("new")
with r3_c2: 
    if st.button("📓\nادھار لسٹ\n(CREDIT LIST)", key="btn_credit"): nav("credit")

# چوتھی قطار (بٹن)
r4_c1, r4_c2 = st.columns(2)
with r4_c1: 
    if st.button("📅\nمکمل ہسٹری\n(HISTORY)", key="btn_hist"): nav("history")
with r4_c2: 
    if st.button("🏠\nہوم پیج\n(HOME)", key="btn_home"): nav("home")

st.divider()

# 6. پیجز کی تفصیل
if st.session_state.page == "home":
    st.subheader("📋 آج کی کارکردگی")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نیا ڈیٹا درج کریں")
    with st.form("ali_form"):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        v1, v2 = st.columns(2)
        cost = v1.number_input("لاگت (Cost)", min_value=0)
        sale = v2.number_input("وصولی (Sale)", min_value=0)
        if st.form_submit_button("سیو کریں"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            new_r = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": p, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([new_r])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("محفوظ ہو گیا!"); nav("home")

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار کی لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    if not cl.empty:
        st.table(cl[["تاریخ", "تفصیل", "فروخت"]])
        st.error(f"کل واجب الادا رقم: {cl['فروخت'].sum()}")
    else: st.info("کوئی ادھار نہیں ہے۔")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ریکارڈ")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
    
