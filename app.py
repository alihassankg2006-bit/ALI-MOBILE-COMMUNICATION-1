import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ سیٹنگ
st.set_page_config(page_title="Ali Mobiles", layout="wide")

# 2. الٹرا VIP کومپیکٹ CSS (مکمل رنگین اور اٹیچڈ)
st.markdown("""
    <style>
    /* فالتو جگہ بالکل ختم */
    .block-container { padding: 0.5rem 0.5rem !important; }
    .stApp { background-color: #ffffff; }
    
    /* ڈبوں کا ڈیزائن - اونچائی کم کر دی تاکہ سب اوپر آ جائیں */
    .tile-box {
        height: 85px; 
        border-radius: 12px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: white !important;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
        margin-bottom: 5px;
    }
    .t-label { font-size: 10px; font-weight: bold; text-transform: uppercase; opacity: 0.9; }
    .t-val { font-size: 20px; font-weight: 900; }

    /* مینو بٹنوں کو بھی ویسا ہی بنانا */
    div.stButton > button {
        height: 85px !important;
        width: 100% !important;
        border-radius: 12px !important;
        font-size: 14px !important;
        font-weight: 800 !important;
        color: white !important;
        border: none !important;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.2) !important;
        margin-bottom: 5px !important;
        line-height: 1.2 !important;
    }

    /* 8 مخصوص گہرے کلر گریڈینٹس */
    .bg-p { background: linear-gradient(135deg, #1b5e20, #2e7d32); } /* Profit */
    .bg-r { background: linear-gradient(135deg, #0d47a1, #1e88e5); } /* Repair */
    .bg-e { background: linear-gradient(135deg, #b71c1c, #d32f2f); } /* Expense */
    .bg-b { background: linear-gradient(135deg, #e65100, #ff9800); } /* Banking */
    
    /* بٹنوں کے رنگ */
    button[key="n"] { background: linear-gradient(135deg, #4a148c, #7b1fa2) !important; } /* Entry */
    button[key="c"] { background: linear-gradient(135deg, #006064, #00838f) !important; } /* Credit */
    button[key="h"] { background: linear-gradient(135deg, #c2185b, #ad1457) !important; } /* History */
    button[key="hm"] { background: linear-gradient(135deg, #263238, #37474f) !important; } /* Home */
    </style>
    """, unsafe_allow_html=True)

# 3. ڈیٹا ہینڈلنگ اور ریبوٹ
DATA_FILE = "ali_shop_v26.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

# سائیڈ بار ریبوٹ آپشن
with st.sidebar:
    st.header("⚙️ سسٹم سیٹنگ")
    if st.button("🚨 REBOOT SYSTEM", help="سارا ڈیٹا مٹانے کے لیے"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            st.warning("ڈیٹا صاف ہو گیا!")
            st.rerun()

df = load_data()
if 'page' not in st.session_state: st.session_state.page = "home"
def nav(p):
    st.session_state.page = p
    st.rerun()

# 4. حساب کتاب
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else df
cp = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
rep = t_df[t_df['کیٹیگری']=="Repairing"]['منافع'].sum()
he = t_df[t_df['کیٹیگری']=="Home Expense"]['فروخت'].sum()
bank = t_df[t_df['کیٹیگری']=="Banking"]['فروخت'].sum()

# 5. لوگو
c_l, c_m, c_r = st.columns([1, 0.4, 1])
with c_m:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)

# 6. 8 بڑے رنگین ڈبے (4 Columns per row - ٹوٹل 2 لائنیں)
r1_c1, r1_c2, r1_c3, r1_c4 = st.columns(4)
with r1_c1: st.markdown(f"<div class='tile-box bg-p'><div class='t-label'>پرافٹ</div><div class='t-val'>{cp}</div></div>", unsafe_allow_html=True)
with r1_c2: st.markdown(f"<div class='tile-box bg-r'><div class='t-label'>ریپیرنگ</div><div class='t-val'>{rep}</div></div>", unsafe_allow_html=True)
with r1_c3: st.markdown(f"<div class='tile-box bg-e'><div class='t-label'>خرچہ</div><div class='t-val'>{he}</div></div>", unsafe_allow_html=True)
with r1_c4: st.markdown(f"<div class='tile-box bg-b'><div class='t-label'>بینکنگ</div><div class='t-val'>{bank}</div></div>", unsafe_allow_html=True)

r2_c1, r2_c2, r2_c3, r2_c4 = st.columns(4)
with r2_c1: 
    if st.button("➕\nENTRY", key="n"): nav("new")
with r2_c2: 
    if st.button("📓\nCREDIT", key="c"): nav("credit")
with r2_c3: 
    if st.button("📅\nHISTORY", key="h"): nav("history")
with r2_c4: 
    if st.button("🏠\nHOME", key="hm"): nav("home")

st.divider()

# 7. پیجز کی تفصیل
if st.session_state.page == "new":
    st.subheader("📝 نئی انٹری")
    with st.form("ali_f", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        v1, v2 = st.columns(2)
        cost = v1.number_input("خریداری", min_value=0)
        sale = v2.number_input("وصولی", min_value=0)
        if st.form_submit_button("سیو کریں"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            nr = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": p, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([nr])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("محفوظ ہو گیا!"); nav("home")

elif st.session_state.page == "home":
    st.subheader("📋 آج کا ریکارڈ")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    st.table(cl[["تاریخ", "تفصیل", "فروخت"]]) if not cl.empty else st.info("کوئی ادھار نہیں")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ہسٹری")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
    
