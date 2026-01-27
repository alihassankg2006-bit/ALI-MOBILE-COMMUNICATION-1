import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی سپلٹ ڈیزائن (CSS)
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 1rem !important; }
    .stApp { background-color: #ffffff; }
    
    /* سپلٹ کارڈ ڈیزائن */
    .split-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: white !important;
        border-radius: 12px;
        margin-bottom: 10px;
        height: 75px;
        overflow: hidden;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    .left-side { width: 55%; padding-left: 15px; text-align: left; }
    .divider { width: 2px; height: 50px; background: rgba(255,255,255,0.3); }
    .right-side { width: 45%; }
    
    .m-label { font-size: 11px; font-weight: bold; opacity: 0.8; text-transform: uppercase; }
    .m-val { font-size: 22px; font-weight: 900; }

    /* بٹنوں کو ڈبوں میں فکس کرنا */
    div.stButton > button {
        height: 75px !important;
        width: 100%;
        border-radius: 0px !important;
        font-size: 16px;
        font-weight: bold;
        color: white !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    div.stButton > button:hover { background: rgba(255,255,255,0.1) !important; }
    
    /* مخصوص رنگ (Deep Colors) */
    .row-green { background: #1b5e20; } /* Profit & Entry */
    .row-purple { background: #4a148c; } /* Repairing & Credit */
    .row-orange { background: #e65100; } /* Banking & History */
    .row-red { background: #b71c1c; }    /* Expense & Home */
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو
cl1, cl2, cl3 = st.columns([1, 0.5, 1])
with cl2:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)

# 4. ڈیٹا لوڈنگ
DATA_FILE = "ali_shop_split_v13.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()
if 'page' not in st.session_state: st.session_state.page = "home"
def nav(p): st.session_state.page = p

# 5. ڈیٹا کیلکولیشن
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else df
cp = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
he = t_df[t_df['کیٹیگری']=="Home Expense"]['فروخت'].sum()
ut = t_df[t_df['اسٹیٹس']=="ادھار"]['فروخت'].sum()
rep = t_df[t_df['کیٹیگری']=="Repairing"]['منافع'].sum()
bank = t_df[t_df['کیٹیگری']=="Banking"]['فروخت'].sum()

# --- سپلٹ ٹائل ڈیزائن (4 Rows) ---

# Row 1: Profit | New Entry (Green)
c1_left, c1_right = st.columns([1.5, 1])
with c1_left:
    st.markdown(f"<div class='split-card row-green'><div class='left-side'><div class='m-label'>کل نقد پرافٹ</div><div class='m-val'>{cp}</div></div><div class='divider'></div></div>", unsafe_allow_html=True)
with c1_right:
    if st.button("➕ ENTRY", key="e"): nav("new")

# Row 2: Repairing | Credit List (Purple)
c2_left, c2_right = st.columns([1.5, 1])
with c2_left:
    st.markdown(f"<div class='split-card row-purple'><div class='left-side'><div class='m-label'>ریپیرنگ پرافٹ</div><div class='m-val'>{rep}</div></div><div class='divider'></div></div>", unsafe_allow_html=True)
with c2_right:
    if st.button("📓 CREDIT", key="c"): nav("credit")

# Row 3: Banking | History (Orange)
c3_left, c3_right = st.columns([1.5, 1])
with c3_left:
    st.markdown(f"<div class='split-card row-orange'><div class='left-side'><div class='m-label'>ایزی پیسہ سیل</div><div class='m-val'>{bank}</div></div><div class='divider'></div></div>", unsafe_allow_html=True)
with c3_right:
    if st.button("📅 HISTORY", key="h"): nav("history")

# Row 4: Home Expense | Home (Red)
c4_left, c4_right = st.columns([1.5, 1])
with c4_left:
    st.markdown(f"<div class='split-card row-red'><div class='left-side'><div class='m-label'>گھر کا خرچ</div><div class='m-val'>{he}</div></div><div class='divider'></div></div>", unsafe_allow_html=True)
with c4_right:
    if st.button("🏠 HOME", key="hm"): nav("home")

st.divider()

# 6. پیجز کا ڈیٹا
if st.session_state.page == "home":
    st.subheader("📋 آج کی سیل")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نئی انٹری")
    with st.form("vip_f"):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        cx, sx = st.columns(2)
        cost = cx.number_input("لاگت", min_value=0)
        sale = sx.number_input("وصولی", min_value=0)
        if st.form_submit_button("محفوظ کریں"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            nr = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": p, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([nr])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("محفوظ ہو گیا!"); st.rerun()

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    st.table(cl[["تاریخ", "تفصیل", "فروخت"]]) if not cl.empty else st.info("کوئی ادھار نہیں")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ریکارڈ")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
    
