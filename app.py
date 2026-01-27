import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. الٹرا وی آئی پی ایکول باکس ڈیزائن (CSS)
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 0.5rem !important; }
    .stApp { background-color: #ffffff; }
    
    /* تمام ڈبوں کا ایک جیسا ڈیزائن */
    .equal-tile {
        height: 120px;
        border-radius: 15px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: white !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
        margin-bottom: 10px;
        padding: 10px;
    }
    .tile-label { font-size: 12px; font-weight: bold; text-transform: uppercase; opacity: 0.9; }
    .tile-val { font-size: 30px; font-weight: 900; margin-top: 5px; }

    /* بٹنوں کو بھی بالکل ویسا ہی بنانا */
    div.stButton > button {
        height: 120px !important;
        width: 100% !important;
        border-radius: 15px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        color: white !important;
        border: none !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15) !important;
        margin-bottom: 10px !important;
        text-transform: uppercase;
    }
    div.stButton > button:hover { opacity: 0.9; transform: translateY(-2px); transition: 0.2s; }

    /* ہر ڈبے کا اپنا الگ گہرا رنگ */
    .bg-1 { background: linear-gradient(135deg, #1b5e20, #2e7d32); } /* کل پرافٹ - ہرا */
    .bg-2 { background: linear-gradient(135deg, #0d47a1, #1976d2); } /* ریپیرنگ - نیلا */
    .bg-3 { background: linear-gradient(135deg, #b71c1c, #d32f2f); } /* گھر خرچ - سرخ */
    .bg-4 { background: linear-gradient(135deg, #e65100, #fb8c00); } /* بینکنگ - نارنجی */
    
    /* بٹنوں کے رنگ */
    button[key="btn_new"] { background: linear-gradient(135deg, #4a148c, #7b1fa2) !important; } /* انٹری - جامنی */
    button[key="btn_credit"] { background: linear-gradient(135deg, #006064, #0097a7) !important; } /* ادھار - ٹیل */
    button[key="btn_hist"] { background: linear-gradient(135deg, #c2185b, #e91e63) !important; } /* ہسٹری - گلابی */
    button[key="btn_home"] { background: linear-gradient(135deg, #37474f, #546e7a) !important; } /* ہوم - سلیٹی */
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو
cl1, cl2, cl3 = st.columns([1, 0.4, 1])
with cl2:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)

# 4. ڈیٹا ہینڈلنگ
DATA_FILE = "ali_shop_v16_equal.csv"
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

# --- 8 برابر سائز کے رنگین باکسز ---

# پہلی قطار: پرافٹ اور ریپیرنگ
r1_c1, r1_c2 = st.columns(2)
with r1_c1: st.markdown(f"<div class='equal-tile bg-1'><div class='tile-label'>کل نقد پرافٹ</div><div class='tile-val'>{cp}</div></div>", unsafe_allow_html=True)
with r1_c2: st.markdown(f"<div class='equal-tile bg-2'><div class='tile-label'>ریپیرنگ پرافٹ</div><div class='tile-val'>{rep}</div></div>", unsafe_allow_html=True)

# دوسری قطار: گھر خرچ اور بینکنگ
r2_c1, r2_c2 = st.columns(2)
with r2_c1: st.markdown(f"<div class='equal-tile bg-3'><div class='tile-label'>گھر کا خرچ</div><div class='tile-val'>{he}</div></div>", unsafe_allow_html=True)
with r2_c2: st.markdown(f"<div class='equal-tile bg-4'><div class='tile-label'>بینکنگ سیل</div><div class='tile-val'>{bank}</div></div>", unsafe_allow_html=True)

# تیسری قطار: نئی انٹری اور ادھار لسٹ (بٹن)
r3_c1, r3_c2 = st.columns(2)
with r3_c1: 
    if st.button("➕ NEW ENTRY", key="btn_new"): nav("new")
with r3_c2: 
    if st.button("📓 CREDIT LIST", key="btn_credit"): nav("credit")

# چوتھی قطار: مکمل ہسٹری اور ہوم (بٹن)
r4_c1, r4_c2 = st.columns(2)
with r4_c1: 
    if st.button("📅 HISTORY", key="btn_hist"): nav("history")
with r4_c2: 
    if st.button("🏠 DASHBOARD", key="btn_home"): nav("home")

st.divider()

# 6. پیجز کا ڈیٹا
if st.session_state.page == "home":
    st.subheader("📋 آج کی سیل")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نئی انٹری")
    with st.form("vip_form"):
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
            st.success("ریکارڈ محفوظ!")
            nav("home")

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    st.table(cl[["تاریخ", "تفصیل", "فروخت"]]) if not cl.empty else st.info("کوئی ادھار نہیں")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ریکارڈ")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
    
