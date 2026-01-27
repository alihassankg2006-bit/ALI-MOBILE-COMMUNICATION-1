import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی کومپیکٹ ڈیزائن (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    
    /* فالتو جگہ ختم کرنا */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    
    /* ڈیش بورڈ ڈبوں کا ڈیزائن */
    .metric-card {
        color: white !important;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2px; /* نیچے والے بٹن کے ساتھ جوڑنے کے لیے */
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    .m-title { font-size: 12px; font-weight: bold; opacity: 0.9; text-transform: uppercase; margin-bottom: 5px; }
    .m-val { font-size: 24px; font-weight: 900; }

    /* مینیو بٹنوں کا ڈیزائن */
    div.stButton > button {
        height: 80px !important; /* اونچائی کم کی تاکہ سب اوپر نظر آئے */
        width: 100%;
        border-radius: 12px;
        font-size: 18px;
        font-weight: bold;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.2);
        box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
        margin-top: 0px;
    }
    
    /* بٹنوں کے گہرے رنگ */
    /* Column 1 Button - Deep Red */
    div[data-testid="column"]:nth-of-type(1) button { background: #b71c1c !important; }
    /* Column 2 Button - Deep Purple */
    div[data-testid="column"]:nth-of-type(2) button { background: #4a148c !important; }
    /* Column 3 Button - Deep Green */
    div[data-testid="column"]:nth-of-type(3) button { background: #1b5e20 !important; }
    /* Column 4 Button - Deep Blue */
    div[data-testid="column"]:nth-of-type(4) button { background: #0d47a1 !important; }

    /* ڈیٹا ٹیبل ڈیزائن */
    .stDataFrame { border: 1px solid #ddd; border-radius: 10px; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو (چھوٹا اور سینٹرڈ)
col_l, col_m, col_r = st.columns([1, 0.8, 1])
with col_m:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)

# 4. ڈیٹا مینجمنٹ
DATA_FILE = "ali_shop_v11_compact.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()
if 'page' not in st.session_state: st.session_state.page = "home"
def nav(p): st.session_state.page = p

# 5. اٹیچڈ گرڈ (حساب کتاب + بٹن ایک ہی ساتھ)
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else df

# ڈیٹا نکالنا
cp = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
he = t_df[t_df['کیٹیگری'] == "Home Expense"]['فروخت'].sum()
ut = t_df[t_df['اسٹیٹس'] == "ادھار"]['فروخت'].sum()
sv = cp - he

# گرڈ بنانا
c1, c2, c3, c4 = st.columns(4)

# پہلی لائن (حساب کتاب)
with c1: st.markdown(f"<div class='metric-card' style='background:#1b5e20;'><div class='m-title'>نقد پرافٹ</div><div class='m-val'>{cp}</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='metric-card' style='background:#b71c1c;'><div class='m-title'>گھر کا خرچ</div><div class='m-val'>{he}</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='metric-card' style='background:#e65100;'><div class='m-title'>آج ادھار</div><div class='m-val'>{ut}</div></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='metric-card' style='background:#0d47a1;'><div class='m-title'>خالص بچت</div><div class='m-val'>{sv}</div></div>", unsafe_allow_html=True)

# دوسری لائن (بٹن - بالکل نیچے اٹیچڈ)
with c1: 
    if st.button("➕ Entry", key="e"): nav("new")
with c2: 
    if st.button("📓 Credit", key="c"): nav("credit")
with c3: 
    if st.button("📅 History", key="h"): nav("history")
with c4: 
    if st.button("🏠 Home", key="hm"): nav("home")

st.divider()

# 6. پیجز کی تفصیل
if st.session_state.page == "home":
    st.subheader("📋 آج کا ریکارڈ")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نئی انٹری")
    with st.form("f", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل")
        stat = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        cx, sx = st.columns(2)
        cost = cx.number_input("لاگت (Cost)", min_value=0)
        sale = sx.number_input("وصولی (Sale)", min_value=0)
        if st.form_submit_button("محفوظ کریں"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            nr = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": p, "اسٹیٹس": stat}
            df = pd.concat([df, pd.DataFrame([nr])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("محفوظ ہو گیا!"); st.rerun()

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    st.table(cl[["تاریخ", "تفصیل", "فروخت"]]) if not cl.empty else st.success("کوئی ادھار نہیں ہے!")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ہسٹری")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
    
