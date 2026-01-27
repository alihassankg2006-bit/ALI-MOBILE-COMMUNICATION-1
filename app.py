import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. پروفیشنل ہاف-ہاف ڈیزائن (CSS)
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 0.5rem !important; }
    .stApp { background-color: #f8f9fa; }
    
    /* میٹرک کارڈ (Left Side) */
    .metric-half {
        height: 100px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 15px 0px 0px 15px; /* صرف بائیں طرف سے گول */
        color: white !important;
        box-shadow: -2px 4px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    .m-label { font-size: 12px; font-weight: bold; opacity: 0.9; text-transform: uppercase; }
    .m-val { font-size: 26px; font-weight: 900; }

    /* اسٹریم لٹ بٹن کو کارڈ کے ساتھ جوڑنا (Right Side) */
    .stButton > button {
        height: 100px !important;
        width: 100% !important;
        border-radius: 0px 15px 15px 0px !important; /* صرف دائیں طرف سے گول */
        font-size: 18px !important;
        font-weight: bold !important;
        color: white !important;
        border: none !important;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.1) !important;
        margin-left: -1px !important; /* بالکل اٹیچ کرنے کے لیے */
    }

    /* رنگوں کی سیٹنگ */
    .bg-green { background: linear-gradient(135deg, #1b5e20, #2e7d32); }
    .bg-purple { background: linear-gradient(135deg, #4a148c, #6a1b9a); }
    .bg-orange { background: linear-gradient(135deg, #e65100, #f57c00); }
    .bg-red { background: linear-gradient(135deg, #b71c1c, #d32f2f); }
    
    /* بٹن ہوور ایفیکٹ */
    .stButton > button:hover { opacity: 0.9; transform: scale(0.98); }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو سیکشن
cl1, cl2, cl3 = st.columns([1, 0.4, 1])
with cl2:
    if os.path.exists("logo.png"): 
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<div style='text-align:center; color:#b71c1c; font-weight:bold;'>ALI MOBILES</div>", unsafe_allow_html=True)

# 4. ڈیٹا ہینڈلنگ
DATA_FILE = "ali_shop_v15_final.csv"
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
he = t_df[t_df['کیٹیگری']=="Home Expense"]['فروخت'].sum()
ut = t_df[df['اسٹیٹس']=="ادھار"]['فروخت'].sum()
rep = t_df[t_df['کیٹیگری']=="Repairing"]['منافع'].sum()
bank = t_df[t_df['کیٹیگری']=="Banking"]['فروخت'].sum()

# 6. ہاف-ہاف گرڈ (4 Rows)

# Row 1: نقد پرافٹ | ENTRY (GREEN)
c1_m, c1_b = st.columns(2)
with c1_m:
    st.markdown(f"<div class='metric-half bg-green'><div class='m-label'>کل نقد پرافٹ</div><div class='m-val'>{cp}</div></div>", unsafe_allow_html=True)
with c1_b:
    if st.button("➕ NEW ENTRY", key="e"): nav("new")
    st.markdown("<style>div[data-testid='column']:nth-of-type(2) button { background: #2e7d32 !important; }</style>", unsafe_allow_html=True)

# Row 2: ریپیرنگ | CREDIT (PURPLE)
c2_m, c2_b = st.columns(2)
with c2_m:
    st.markdown(f"<div class='metric-half bg-purple'><div class='m-label'>ریپیرنگ پرافٹ</div><div class='m-val'>{rep}</div></div>", unsafe_allow_html=True)
with c2_b:
    if st.button("📓 CREDIT LIST", key="c"): nav("credit")
    st.markdown("<style>div[data-testid='column']:nth-of-type(4) button { background: #6a1b9a !important; }</style>", unsafe_allow_html=True)

# Row 3: ایزی پیسہ | HISTORY (ORANGE)
c3_m, c3_b = st.columns(2)
with c3_m:
    st.markdown(f"<div class='metric-half bg-orange'><div class='m-label'>ایزی پیسہ سیل</div><div class='m-val'>{bank}</div></div>", unsafe_allow_html=True)
with c3_b:
    if st.button("📅 FULL HISTORY", key="h"): nav("history")
    st.markdown("<style>div[data-testid='column']:nth-of-type(6) button { background: #f57c00 !important; }</style>", unsafe_allow_html=True)

# Row 4: گھر کا خرچ | HOME (RED)
c4_m, c4_b = st.columns(2)
with c4_m:
    st.markdown(f"<div class='metric-half bg-red'><div class='m-label'>گھر کا خرچ</div><div class='m-val'>{he}</div></div>", unsafe_allow_html=True)
with c4_b:
    if st.button("🏠 DASHBOARD", key="hm"): nav("home")
    st.markdown("<style>div[data-testid='column']:nth-of-type(8) button { background: #d32f2f !important; }</style>", unsafe_allow_html=True)

st.divider()

# 7. پیجز کا ڈیٹا
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
    
