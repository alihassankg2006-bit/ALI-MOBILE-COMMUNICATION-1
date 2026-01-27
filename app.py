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

# 2. پروفیشنل ڈیزائن CSS
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main > div { padding-top: 0.5rem; }
    
    /* ٹائل کارڈز کا ڈیزائن */
    .half-card {
        width: 100%;
        height: 130px;
        border-radius: 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        color: white;
        font-family: 'Segoe UI', sans-serif;
        margin-bottom: 5px;
    }
    
    .card-title { font-size: 14px; font-weight: 700; text-transform: uppercase; opacity: 0.9; }
    .card-value { font-size: 32px; font-weight: 800; margin-top: 5px; }
    
    /* رنگین گریڈینٹس */
    .profit-card { background: linear-gradient(145deg, #1e88e5, #0d47a1); }
    .repair-card { background: linear-gradient(145deg, #43a047, #1b5e20); }
    .entry-card { background: linear-gradient(145deg, #ff9800, #e65100); }
    .credit-card { background: linear-gradient(145deg, #9c27b0, #6a1b9a); }
    .history-card { background: linear-gradient(145deg, #00bcd4, #006064); }
    .easypaisa-card { background: linear-gradient(145deg, #f44336, #b71c1c); }

    /* بٹن کو ٹائل کے ساتھ جوڑنا */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        height: 40px;
        background-color: white;
        color: #333;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو اور ٹائٹل
st.markdown("""
<div style="text-align: center; padding: 10px;">
    <h2 style="color: #1b5e20; margin-bottom: 0px; font-weight: 800;">ALI MOBILES & COMMUNICATION</h2>
    <p style="color: #666; font-size: 14px;">Premium Shop Management System</p>
</div>
""", unsafe_allow_html=True)

# 4. ڈیٹا لوڈنگ
DATA_FILE = "ali_shop_v14_data.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()

# پیج نیویگیشن
if 'page' not in st.session_state:
    st.session_state.page = "home"

def nav(p):
    st.session_state.page = p

# 5. ڈیٹا کیلکولیشن
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else pd.DataFrame()

# حساب کتاب (PKR میں)
total_profit = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
repair_profit = t_df[t_df['کیٹیگری'] == "Repairing"]['منافع'].sum()
easypaisa_sales = t_df[t_df['کیٹیگری'] == "Banking"]['فروخت'].sum()
total_credit = df[df['اسٹیٹس'] == "ادھار"]['فروخت'].sum()
total_history = len(df)

# 6. ڈیش بورڈ لے آؤٹ (2 Columns)
row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    st.markdown(f'<div class="half-card profit-card"><div class="card-title">کل نقد پرافٹ</div><div class="card-value">{total_profit}</div></div>', unsafe_allow_html=True)
    if st.button("آج کی تفصیل 📊", key="btn_p"): nav("home")

with row1_col2:
    st.markdown(f'<div class="half-card repair-card"><div class="card-title">ریپیرنگ پرافٹ</div><div class="card-value">{repair_profit}</div></div>', unsafe_allow_html=True)
    if st.button("ریپیرنگ لسٹ 🔧", key="btn_r"): nav("history")

row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    st.markdown(f'<div class="half-card entry-card"><div class="card-title">نئی انٹری</div><div class="card-value">➕</div></div>', unsafe_allow_html=True)
    if st.button("کھولیں 📝", key="btn_e"): nav("new")

with row2_col2:
    st.markdown(f'<div class="half-card credit-card"><div class="card-title">کل ادھار</div><div class="card-value">{total_credit}</div></div>', unsafe_allow_html=True)
    if st.button("ادھار لسٹ 📓", key="btn_c"): nav("credit")

row3_col1, row3_col2 = st.columns(2)
with row3_col1:
    st.markdown(f'<div class="half-card history-card"><div class="card-title">ٹوٹل ریکارڈ</div><div class="card-value">{total_history}</div></div>', unsafe_allow_html=True)
    if st.button("ہسٹری دیکھیں 📅", key="btn_h"): nav("history")

with row3_col2:
    st.markdown(f'<div class="half-card easypaisa-card"><div class="card-title">ایزی پیسہ سیل</div><div class="card-value">{easypaisa_sales}</div></div>', unsafe_allow_html=True)
    if st.button("بینکنگ تفصیل 💰", key="btn_b"): nav("easypaisa_details")

st.divider()

# 7. پیجز کی منطق
if st.session_state.page == "home":
    st.subheader("📊 آج کی کارکردگی")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نیا ریکارڈ شامل کریں")
    with st.form("new_form", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        desc = st.text_input("تفصیل")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        c1, c2 = st.columns(2)
        cost = c1.number_input("لاگت (Cost)", min_value=0)
        sale = c2.number_input("فروخت (Sale)", min_value=0)
        
        if st.form_submit_button("💾 محفوظ کریں"):
            prof = 0 if cat == "Home Expense" else (sale - cost)
            new_data = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": desc, "خریداری": cost, "فروخت": sale, "منافع": prof, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("ریکارڈ محفوظ ہو گیا!")
            st.rerun()

elif st.session_state.page == "credit":
    st.subheader("📋 ادھار کا ریکارڈ")
    credit_df = df[df['اسٹیٹس'] == "ادھار"]
    st.dataframe(credit_df, use_container_width=True)
    st.metric("کل واجب الادا رقم", f"Rs. {total_credit}")

elif st.session_state.page == "history":
    st.subheader("📜 مکمل ہسٹری")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)

elif st.session_state.page == "easypaisa_details":
    st.subheader("💰 بینکنگ تفصیلات")
    st.dataframe(df[df['کیٹیگری'] == "Banking"], use_container_width=True)
    
