import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی سپلٹ گرڈ ڈیزائن (CSS)
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 0.5rem !important; }
    .stApp { background-color: #ffffff; }
    
    /* ڈیش بورڈ ڈبوں کا ڈیزائن */
    .metric-tile {
        color: white !important;
        padding: 10px;
        border-radius: 15px;
        text-align: center;
        height: 90px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
        margin-bottom: 8px;
    }
    .m-label { font-size: 11px; font-weight: bold; opacity: 0.8; text-transform: uppercase; }
    .m-val { font-size: 26px; font-weight: 900; }

    /* مینو بٹنوں کا ڈیزائن (بالکل برابر سائز) */
    div.stButton > button {
        height: 90px !important;
        width: 100%;
        border-radius: 15px;
        font-size: 18px;
        font-weight: bold;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.2);
        box-shadow: 0px 4px 8px rgba(0,0,0,0.3);
        margin-bottom: 8px;
    }
    
    /* کالمز کے انفرادی گہرے رنگ */
    /* Row 1: Deep Green */
    [data-testid="column"]:nth-of-type(1) .metric-tile { background: #1b5e20 !important; }
    [data-testid="column"]:nth-of-type(2) button { background: #1b5e20 !important; }
    
    /* Row 2: Deep Purple */
    [data-testid="column"]:nth-of-type(3) .metric-tile { background: #4a148c !important; }
    [data-testid="column"]:nth-of-type(4) button { background: #4a148c !important; }
    
    /* Row 3: Deep Orange */
    [data-testid="column"]:nth-of-type(5) .metric-tile { background: #e65100 !important; }
    [data-testid="column"]:nth-of-type(6) button { background: #e65100 !important; }
    
    /* Row 4: Deep Red */
    [data-testid="column"]:nth-of-type(7) .metric-tile { background: #b71c1c !important; }
    [data-testid="column"]:nth-of-type(8) button { background: #b71c1c !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو
cl1, cl2, cl3 = st.columns([1, 0.4, 1])
with cl2:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)

# 4. ڈیٹا مینجمنٹ
DATA_FILE = "ali_shop_v14_pro.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()
if 'page' not in st.session_state: st.session_state.page = "home"
def nav(p): st.session_state.page = p

# 5. حساب کتاب
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else df
cp = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
he = t_df[t_df['کیٹیگری']=="Home Expense"]['فروخت'].sum()
ut = t_df[t_df['اسٹیٹس']=="ادھار"]['فروخت'].sum()
rep = t_df[t_df['کیٹیگری']=="Repairing"]['منافع'].sum()
bank = t_df[t_df['کیٹیگری']=="Banking"]['فروخت'].sum()

# --- سپلٹ گرڈ (Left: Metrics | Right: Actions) ---

# Row 1: Profit & Entry
c1_m, c1_b = st.columns(2)
with c1_m: st.markdown(f"<div class='metric-tile'><div class='m-label'>کل نقد پرافٹ</div><div class='m-val'>{cp}</div></div>", unsafe_allow_html=True)
with c1_b: 
    if st.button("➕ NEW ENTRY", key="e"): nav("new")

# Row 2: Repairing & Credit List
c2_m, c2_b = st.columns(2)
with c2_m: st.markdown(f"<div class='metric-tile'><div class='m-label'>ریپیرنگ پرافٹ</div><div class='m-val'>{rep}</div></div>", unsafe_allow_html=True)
with c2_b: 
    if st.button("📓 CREDIT LIST", key="c"): nav("credit")

# Row 3: EasyPaisa & History
c3_m, c3_b = st.columns(2)
with c3_m: st.markdown(f"<div class='metric-tile'><div class='m-label'>بینکنگ / ایزی پیسہ</div><div class='m-val'>{bank}</div></div>", unsafe_allow_html=True)
with c3_b: 
    if st.button("📅 FULL HISTORY", key="h"): nav("history")

# Row 4: Home Expense & Dashboard
c4_m, c4_b = st.columns(2)
with c4_m: st.markdown(f"<div class='metric-tile'><div class='m-label'>گھر کا خرچ</div><div class='m-val'>{he}</div></div>", unsafe_allow_html=True)
with c4_b: 
    if st.button("🏠 DASHBOARD", key="hm"): nav("home")

st.divider()

# 6. پیجز کا ڈیٹا
if st.session_state.page == "home":
    st.subheader("📋 آج کی سیل")
    st.dataframe(t_df.sort_index(ascending=False), use_container_width=True)

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
            st.success("ریکارڈ محفوظ!"); st.rerun()

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    st.table(cl[["تاریخ", "تفصیل", "فروخت"]]) if not cl.empty else st.info("کوئی ادھار نہیں")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ریکارڈ")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
