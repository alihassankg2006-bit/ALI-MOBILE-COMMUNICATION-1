import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی کلر ڈیزائن (CSS)
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 0.5rem !important; }
    .stApp { background-color: #ffffff; }
    
    /* ڈیش بورڈ باکسز (Metrics) */
    .tile {
        height: 120px;
        border-radius: 15px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: white !important;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
        margin-bottom: 10px;
    }
    .t-label { font-size: 13px; font-weight: bold; text-transform: uppercase; opacity: 0.9; }
    .t-val { font-size: 32px; font-weight: 900; margin-top: 5px; }

    /* مینو بٹنز (Actions) */
    div.stButton > button {
        height: 120px !important;
        width: 100% !important;
        border-radius: 15px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        color: white !important;
        border: none !important;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.2) !important;
        margin-bottom: 10px !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    div.stButton > button:hover { transform: scale(0.98); transition: 0.2s; }

    /* 8 انفرادی گہرے رنگ (Deep Gradients) */
    .bg-profit { background: linear-gradient(135deg, #1b5e20, #2e7d32); } /* گہرا ہرا */
    .bg-repair { background: linear-gradient(135deg, #0d47a1, #1565c0); } /* گہرا نیلا */
    .bg-expense { background: linear-gradient(135deg, #b71c1c, #c62828); } /* گہرا سرخ */
    .bg-banking { background: linear-gradient(135deg, #e65100, #ef6c00); } /* گہرا نارنجی */
    
    /* بٹنوں کے رنگ */
    button[key="btn_e"] { background: linear-gradient(135deg, #4a148c, #6a1b9a) !important; } /* جامنی */
    button[key="btn_c"] { background: linear-gradient(135deg, #006064, #00838f) !important; } /* ٹیل (سبز مائل نیلا) */
    button[key="btn_h"] { background: linear-gradient(135deg, #c2185b, #ad1457) !important; } /* گلابی */
    button[key="btn_hm"] { background: linear-gradient(135deg, #263238, #37474f) !important; } /* سلیٹی */
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو سیکشن
cl1, cl2, cl3 = st.columns([1, 0.4, 1])
with cl2:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)

# 4. ڈیٹا ہینڈلنگ
DATA_FILE = "ali_shop_pro_v17.csv"
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

# --- 8 کلر فل ٹائلز گرڈ (2 کالمز) ---

# قطار 1: پرافٹ اور ریپیرنگ
r1_c1, r1_c2 = st.columns(2)
with r1_c1: st.markdown(f"<div class='tile bg-profit'><div class='t-label'>نقد پرافٹ</div><div class='t-val'>{cp}</div></div>", unsafe_allow_html=True)
with r1_c2: st.markdown(f"<div class='tile bg-repair'><div class='t-label'>ریپیرنگ پرافٹ</div><div class='t-val'>{rep}</div></div>", unsafe_allow_html=True)

# قطار 2: خرچہ اور بینکنگ
r2_c1, r2_c2 = st.columns(2)
with r2_c1: st.markdown(f"<div class='tile bg-expense'><div class='t-label'>گھر کا خرچ</div><div class='t-val'>{he}</div></div>", unsafe_allow_html=True)
with r2_c2: st.markdown(f"<div class='tile bg-banking'><div class='t-label'>بینکنگ سیل</div><div class='t-val'>{bank}</div></div>", unsafe_allow_html=True)

# قطار 3: انٹری اور کریڈٹ (بٹن)
r3_c1, r3_c2 = st.columns(2)
with r3_c1: 
    if st.button("➕\nENTRY", key="btn_e"): nav("new")
with r3_c2: 
    if st.button("📓\nCREDIT", key="btn_c"): nav("credit")

# قطار 4: ہسٹری اور ہوم (بٹن)
r4_c1, r4_c2 = st.columns(2)
with r4_c1: 
    if st.button("📅\nHISTORY", key="btn_h"): nav("history")
with r4_c2: 
    if st.button("🏠\nHOME", key="btn_hm"): nav("home")

st.divider()

# 6. پیجز کا ڈیٹا
if st.session_state.page == "home":
    st.subheader("📋 آج کی سیل")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نئی انٹری شامل کریں")
    with st.form("vip_form"):
        cat = st.selectbox("کیٹیگری منتخب کریں", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل (آئٹم کا نام)")
        pay = st.radio("ادائیگی کی قسم", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        c1, c2 = st.columns(2)
        cost = c1.number_input("خریداری (Cost)", min_value=0)
        sale = c2.number_input("فروخت (Sale)", min_value=0)
        if st.form_submit_button("محفوظ کریں"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            nr = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": p, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([nr])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("ریکارڈ محفوظ ہو گیا!")
            nav("home")

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار لینے والوں کی لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    st.table(cl[["تاریخ", "تفصیل", "فروخت"]]) if not cl.empty else st.info("فی الحال کوئی ادھار نہیں ہے۔")

elif st.session_state.page == "history":
    st.subheader("📅 دکان کا مکمل ریکارڈ")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
    
