import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(
    page_title="Ali Mobiles & Communication", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. پروفیشنل ڈیزائن (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .half-card {
        width: 100%; height: 120px; border-radius: 15px;
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1); color: white;
        margin-bottom: 5px; font-family: sans-serif;
    }
    .card-title { font-size: 14px; font-weight: bold; text-transform: uppercase; }
    .card-value { font-size: 30px; font-weight: 800; }
    
    /* رنگین تھیمز */
    .profit-card { background: linear-gradient(45deg, #1e88e5, #0d47a1); }
    .repair-card { background: linear-gradient(45deg, #43a047, #1b5e20); }
    .entry-card { background: linear-gradient(45deg, #ff9800, #e65100); }
    .credit-card { background: linear-gradient(45deg, #9c27b0, #6a1b9a); }
    .history-card { background: linear-gradient(45deg, #00bcd4, #006064); }
    .easypaisa-card { background: linear-gradient(45deg, #f44336, #b71c1c); }

    .stButton > button { width: 100%; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. ڈیٹا لوڈنگ فنکشن (بہتر ایرر ہینڈلنگ کے ساتھ)
DATA_FILE = "ali_shop_management_v15.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            df['تاریخ'] = pd.to_datetime(df['تاریخ'])
            return df
        except Exception as e:
            st.error(f"ڈیٹا فائل لوڈ کرنے میں مسئلہ: {e}")
            return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

# سٹیٹ مینیجمنٹ
if 'page' not in st.session_state:
    st.session_state.page = "home"

def nav(p):
    st.session_state.page = p
    st.rerun() if hasattr(st, "rerun") else st.experimental_rerun()

df = load_data()

# 4. ہیڈر
st.markdown("<h2 style='text-align:center; color:#1b5e20;'>ALI MOBILES & COMMUNICATION</h2>", unsafe_allow_html=True)

# 5. ڈیٹا کیلکولیشن
today_date = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today_date] if not df.empty else pd.DataFrame()

profit = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
repair = t_df[t_df['کیٹیگری'] == "Repairing"]['منافع'].sum()
banking = t_df[t_df['کیٹیگری'] == "Banking"]['فروخت'].sum()
credit = df[df['اسٹیٹس'] == "ادھار"]['فروخت'].sum()
history_count = len(df)

# 6. ڈیش بورڈ گرڈ (2 Columns)
c1, c2 = st.columns(2)
with c1:
    st.markdown(f'<div class="half-card profit-card"><div class="card-title">کل منافع</div><div class="card-value">{profit}</div></div>', unsafe_allow_html=True)
    if st.button("تفصیل دیکھیں 📊", key="b1"): nav("home")

with c2:
    st.markdown(f'<div class="half-card repair-card"><div class="card-title">ریپیرنگ</div><div class="card-value">{repair}</div></div>', unsafe_allow_html=True)
    if st.button("ہسٹری کھولیں 🔧", key="b2"): nav("history")

c3, c4 = st.columns(2)
with c3:
    st.markdown(f'<div class="half-card entry-card"><div class="card-title">نئی انٹری</div><div class="card-value">➕</div></div>', unsafe_allow_html=True)
    if st.button("انٹری کریں 📝", key="b3"): nav("new")

with c4:
    st.markdown(f'<div class="half-card credit-card"><div class="card-title">کل ادھار</div><div class="card-value">{credit}</div></div>', unsafe_allow_html=True)
    if st.button("ادھار لسٹ 📓", key="b4"): nav("credit")

c5, c6 = st.columns(2)
with c5:
    st.markdown(f'<div class="half-card history-card"><div class="card-title">ٹوٹل ریکارڈ</div><div class="card-value">{history_count}</div></div>', unsafe_allow_html=True)
    if st.button("فل ریکارڈ 📅", key="b5"): nav("history")

with c6:
    st.markdown(f'<div class="half-card easypaisa-card"><div class="card-title">بینکنگ سیل</div><div class="card-value">{banking}</div></div>', unsafe_allow_html=True)
    if st.button("بینکنگ ڈیٹا 💰", key="b6"): nav("banking")

st.divider()

# 7. پیجز کنٹرول
if st.session_state.page == "home":
    st.subheader("📋 آج کی سیل")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نئی انٹری")
    with st.form("my_form", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        desc = st.text_input("تفصیل")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        col_a, col_b = st.columns(2)
        cost = col_a.number_input("لاگت", min_value=0)
        sale = col_b.number_input("فروخت", min_value=0)
        
        if st.form_submit_button("محفوظ کریں"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            new_row = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": desc, "خریداری": cost, "فروخت": sale, "منافع": p, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("ریکارڈ سیو ہو گیا!")
            st.rerun() if hasattr(st, "rerun") else st.experimental_rerun()

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار لسٹ")
    st.dataframe(df[df['اسٹیٹس'] == "ادھار"], use_container_width=True)

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ہسٹری")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)

elif st.session_state.page == "banking":
    st.subheader("💰 بینکنگ تفصیل")
    st.dataframe(df[df['کیٹیگری'] == "Banking"], use_container_width=True)
    
