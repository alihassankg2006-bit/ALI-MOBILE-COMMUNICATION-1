import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی "لانگ ٹائل" ڈیزائن (CSS)
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 0.5rem !important; }
    .stApp { background-color: #ffffff; }
    
    /* ڈیش بورڈ میٹرک باکسز */
    .tile {
        height: 130px; /* ڈبوں کو لمبا کر دیا گیا ہے */
        border-radius: 18px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: white !important;
        box-shadow: 0px 6px 12px rgba(0,0,0,0.2);
        margin-bottom: 12px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .t-label { font-size: 13px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
    .t-val { font-size: 34px; font-weight: 900; margin-top: 5px; }

    /* مینو ایکشن بٹنز */
    div.stButton > button {
        height: 130px !important; /* بٹنز کو بھی لمبا کر دیا گیا ہے */
        width: 100% !important;
        border-radius: 18px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        color: white !important;
        border: none !important;
        box-shadow: 0px 6px 12px rgba(0,0,0,0.2) !important;
        margin-bottom: 12px !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    div.stButton > button:hover { transform: translateY(-3px); box-shadow: 0px 8px 15px rgba(0,0,0,0.3) !important; transition: 0.3s; }

    /* 8 انفرادی گہرے رنگ (Deep Professional Gradients) */
    .bg-p { background: linear-gradient(135deg, #1b5e20, #2e7d32); } /* کل پرافٹ - ہرا */
    .bg-r { background: linear-gradient(135deg, #0d47a1, #1e88e5); } /* ریپیرنگ - نیلا */
    .bg-e { background: linear-gradient(135deg, #b71c1c, #d32f2f); } /* گھر خرچ - سرخ */
    .bg-b { background: linear-gradient(135deg, #e65100, #ff9800); } /* بینکنگ - نارنجی */
    
    /* بٹنوں کے مخصوص گہرے رنگ */
    button[key="btn_new"] { background: linear-gradient(135deg, #4a148c, #8e24aa) !important; } /* نئی انٹری - جامنی */
    button[key="btn_credit"] { background: linear-gradient(135deg, #006064, #0097a7) !important; } /* ادھار لسٹ - ٹیل */
    button[key="btn_hist"] { background: linear-gradient(135deg, #c2185b, #e91e63) !important; } /* مکمل ہسٹری - گلابی */
    button[key="btn_home"] { background: linear-gradient(135deg, #263238, #455a64) !important; } /* ہوم پیج - سلیٹی */
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو سیکشن
cl1, cl2, cl3 = st.columns([1, 0.4, 1])
with cl2:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)

# 4. ڈیٹا ہینڈلنگ
DATA_FILE = "ali_shop_v18_final.csv"
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

# --- 8 لانگ ٹائلز گرڈ (2 Columns) ---

# قطار 1: حساب کتاب
r1_c1, r1_c2 = st.columns(2)
with r1_c1: st.markdown(f"<div class='tile bg-p'><div class='t-label'>کل نقد پرافٹ</div><div class='t-val'>{cp}</div></div>", unsafe_allow_html=True)
with r1_c2: st.markdown(f"<div class='tile bg-r'><div class='t-label'>ریپیرنگ پرافٹ</div><div class='t-val'>{rep}</div></div>", unsafe_allow_html=True)

# قطار 2: خرچہ اور بینکنگ
r2_c1, r2_c2 = st.columns(2)
with r2_c1: st.markdown(f"<div class='tile bg-e'><div class='t-label'>گھر کا خرچ</div><div class='t-val'>{he}</div></div>", unsafe_allow_html=True)
with r2_c2: st.markdown(f"<div class='tile bg-b'><div class='t-label'>ایزی پیسہ سیل</div><div class='t-val'>{bank}</div></div>", unsafe_allow_html=True)

# قطار 3: انٹری اور ادھار (بٹنز)
r3_c1, r3_c2 = st.columns(2)
with r3_c1: 
    if st.button("➕\nنئی انٹری\n(NEW ENTRY)", key="btn_new"): nav("new")
with r3_c2: 
    if st.button("📓\nادھار لسٹ\n(CREDIT LIST)", key="btn_credit"): nav("credit")

# قطار 4: ہسٹری اور ہوم (بٹنز)
r4_c1, r4_c2 = st.columns(2)
with r4_c1: 
    if st.button("📅\nمکمل ہسٹری\n(HISTORY)", key="btn_hist"): nav("history")
with r4_c2: 
    if st.button("🏠\nہوم پیج\n(HOME)", key="btn_home"): nav("home")

st.divider()

# 6. پیجز کی تفصیل
if st.session_state.page == "home":
    st.subheader("📋 آج کی سیل کا ریکارڈ")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نئی انٹری شامل کریں")
    with st.form("ali_form"):
        cat = st.selectbox("کیٹیگری منتخب کریں", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل (گاہک یا آئٹم)")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        c1, c2 = st.columns(2)
        cost = c1.number_input("لاگت (Cost)", min_value=0)
        sale = c2.number_input("فروخت (Sale)", min_value=0)
        if st.form_submit_button("محفوظ کریں"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            nr = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": p, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([nr])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("ریکارڈ محفوظ ہو گیا!")
            nav("home")

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    if not cl.empty:
        st.table(cl[["تاریخ", "تفصیل", "فروخت"]])
        st.error(f"ٹوٹل واجب الادا ادھار: {cl['فروخت'].sum()} PKR")
    else: st.info("کوئی ادھار باقی نہیں ہے۔")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل دکان کا ریکارڈ")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
    
