import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی ایکول گرڈ ڈیزائن (CSS)
st.markdown("""
    <style>
    /* فالتو سفید جگہ ختم کرنا */
    .block-container { padding-top: 0.5rem !important; padding-bottom: 0rem !important; }
    .stApp { background-color: #ffffff; }
    
    /* ڈیش بورڈ ڈبوں کا ڈیزائن */
    .tile {
        color: white !important;
        padding: 15px 5px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 5px;
        height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
    }
    .tile-title { font-size: 11px; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
    .tile-val { font-size: 22px; font-weight: 900; }

    /* بٹنوں کا ڈیزائن (بالکل ڈبوں کے برابر) */
    div.stButton > button {
        height: 80px !important;
        width: 100%;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
        margin-top: 0px;
        text-transform: uppercase;
    }
    
    /* کالمز کے انفرادی گہرے رنگ (حساب اور بٹن دونوں کے لیے) */
    /* Column 1: Deep Green */
    [data-testid="column"]:nth-of-type(1) .tile { background: #1b5e20 !important; }
    [data-testid="column"]:nth-of-type(1) button { background: #1b5e20 !important; }
    
    /* Column 2: Deep Red */
    [data-testid="column"]:nth-of-type(2) .tile { background: #b71c1c !important; }
    [data-testid="column"]:nth-of-type(2) button { background: #b71c1c !important; }
    
    /* Column 3: Deep Orange */
    [data-testid="column"]:nth-of-type(3) .tile { background: #e65100 !important; }
    [data-testid="column"]:nth-of-type(3) button { background: #e65100 !important; }
    
    /* Column 4: Deep Blue */
    [data-testid="column"]:nth-of-type(4) .tile { background: #0d47a1 !important; }
    [data-testid="column"]:nth-of-type(4) button { background: #0d47a1 !important; }

    /* فارم اور ٹیبل کو صاف دکھانا */
    .stForm { background: #f8f9fa; padding: 15px; border-radius: 15px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو (انتہائی کومپیکٹ)
c_l, c_m, c_r = st.columns([1, 0.6, 1])
with c_m:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)

# 4. ڈیٹا مینجمنٹ
DATA_FILE = "ali_shop_equal_grid.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()
if 'page' not in st.session_state: st.session_state.page = "home"
def nav(p): st.session_state.page = p

# 5. ایکول گرڈ (حساب کتاب + بٹن)
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else df

cp = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
he = t_df[t_df['کیٹیگری'] == "Home Expense"]['فروخت'].sum()
ut = t_df[t_df['اسٹیٹس'] == "ادھار"]['فروخت'].sum()
sv = cp - he

# گرڈ کا ڈھانچہ
col1, col2, col3, col4 = st.columns(4)

# پہلی لائن (حساب کتاب کے ڈبے)
with col1: st.markdown(f"<div class='tile'><div class='tile-title'>نقد پرافٹ</div><div class='tile-val'>{cp}</div></div>", unsafe_allow_html=True)
with col2: st.markdown(f"<div class='tile'><div class='tile-title'>گھر کا خرچ</div><div class='tile-val'>{he}</div></div>", unsafe_allow_html=True)
with col3: st.markdown(f"<div class='tile'><div class='tile-title'>آج ادھار</div><div class='tile-val'>{ut}</div></div>", unsafe_allow_html=True)
with col4: st.markdown(f"<div class='tile'><div class='tile-title'>خالص بچت</div><div class='tile-val'>{sv}</div></div>", unsafe_allow_html=True)

# دوسری لائن (بٹنز - بالکل برابر نیچے)
with col1: 
    if st.button("➕ ENTRY", key="e"): nav("new")
with col2: 
    if st.button("📓 CREDIT", key="c"): nav("credit")
with col3: 
    if st.button("📅 HISTORY", key="h"): nav("history")
with col4: 
    if st.button("🏠 HOME", key="hm"): nav("home")

st.write("---")

# 6. پیجز (جو بٹن دبانے پر نیچے کھلیں گے)
if st.session_state.page == "home":
    st.subheader("📋 آج کی سیل")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نئی انٹری")
    with st.form("entry_form", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل")
        stat = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        ca, sa = st.columns(2)
        cost = ca.number_input("خریداری (Cost)", min_value=0)
        sale = sa.number_input("وصولی (Sale)", min_value=0)
        if st.form_submit_button("سیو کریں 💾"):
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
    
