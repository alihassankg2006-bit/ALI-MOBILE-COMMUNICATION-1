import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobiles", layout="wide")

# 2. الٹرا کومپیکٹ ڈیزائن (CSS)
st.markdown("""
    <style>
    /* اسکرین کی فالتو جگہ ختم کرنا */
    .block-container { padding: 0.5rem 0.5rem !important; }
    .stApp { background-color: #ffffff; }
    
    /* چھوٹے رنگین ڈبوں (Tiles) کا ڈیزائن */
    .tile {
        color: white !important;
        padding: 5px;
        border-radius: 8px;
        text-align: center;
        height: 70px; /* اونچائی مزید کم کر دی گئی ہے */
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.2);
        margin-bottom: 5px;
    }
    .t-label { font-size: 10px; font-weight: bold; opacity: 0.9; }
    .t-val { font-size: 18px; font-weight: 900; }

    /* بٹنوں کو ڈبوں جیسا بنانا */
    div.stButton > button {
        height: 70px !important;
        width: 100%;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
        color: white !important;
        border: none;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.2);
        padding: 0 !important;
    }
    
    /* فالتو گیپ ختم کرنا */
    [data-testid="column"] { padding: 0 2px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو (انتہائی چھوٹا)
cl1, cl2, cl3 = st.columns([1, 0.4, 1])
with cl2:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)

# 4. ڈیٹا لوڈنگ
DATA_FILE = "ali_shop_compact_v12.csv"
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
p_t = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
s_t = t_df[t_df['کیٹیگری']!="Home Expense"]['فروخت'].sum()
h_t = t_df[t_df['کیٹیگری']=="Home Expense"]['فروخت'].sum()
u_t = t_df[t_df['اسٹیٹس']=="ادھار"]['فروخت'].sum()
rep_t = t_df[t_df['کیٹیگری']=="Repairing"]['منافع'].sum()
bank_t = t_df[t_df['کیٹیگری']=="Banking"]['فروخت'].sum()

# --- 10 کلر فل ٹائلز گرڈ (4 Columns per row) ---

# پہلی لائن: حساب کتاب
r1_c1, r1_c2, r1_c3, r1_c4 = st.columns(4)
with r1_c1: st.markdown(f"<div class='tile' style='background:#1b5e20;'><div class='t-label'>پرافٹ</div><div class='t-val'>{p_t}</div></div>", unsafe_allow_html=True)
with r1_c2: st.markdown(f"<div class='tile' style='background:#0d47a1;'><div class='t-label'>کل سیل</div><div class='t-val'>{s_t}</div></div>", unsafe_allow_html=True)
with r1_c3: st.markdown(f"<div class='tile' style='background:#b71c1c;'><div class='t-label'>گھر خرچ</div><div class='t-val'>{h_t}</div></div>", unsafe_allow_html=True)
with r1_c4: st.markdown(f"<div class='tile' style='background:#e65100;'><div class='t-label'>ادھار</div><div class='t-val'>{u_t}</div></div>", unsafe_allow_html=True)

# دوسری لائن: مخصوص ڈبے اور بٹن
r2_c1, r2_c2, r2_c3, r2_c4 = st.columns(4)
with r2_c1: st.markdown(f"<div class='tile' style='background:#4a148c;'><div class='t-label'>ریپیرنگ</div><div class='t-val'>{rep_t}</div></div>", unsafe_allow_html=True)
with r2_c2: st.markdown(f"<div class='tile' style='background:#fbc02d;'><div class='t-label' style='color:black;'>بینکنگ</div><div class='t-val' style='color:black;'>{bank_t}</div></div>", unsafe_allow_html=True)
with r2_c3: 
    if st.button("➕ ENTRY", key="e"): nav("new")
    st.markdown("<style>button[key='e'] { background: #c2185b !important; }</style>", unsafe_allow_html=True)
with r2_c4: 
    if st.button("📓 CREDIT", key="c"): nav("credit")
    st.markdown("<style>button[key='c'] { background: #5d4037 !important; }</style>", unsafe_allow_html=True)

# تیسری لائن: ہسٹری اور ہوم
r3_c1, r3_c2, r3_c3, r3_c4 = st.columns(4)
with r3_c1: 
    if st.button("📅 HISTORY", key="h"): nav("history")
    st.markdown("<style>button[key='h'] { background: #00796b !important; }</style>", unsafe_allow_html=True)
with r3_c2: 
    if st.button("🏠 HOME", key="hm"): nav("home")
    st.markdown("<style>button[key='hm'] { background: #455a64 !important; }</style>", unsafe_allow_html=True)

st.write("---")

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
        if st.form_submit_button("سیو کریں"):
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
    
