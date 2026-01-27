import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ اور نام
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. کسٹم ریڈ (Red) تھیم ڈیزائن
st.markdown("""
    <style>
    /* مین بیک گراؤنڈ */
    .main { background-color: #ffffff; }
    
    /* بڑے بٹنوں (Boxes) کا ڈیزائن */
    div.stButton > button {
        height: 120px;
        width: 100%;
        border-radius: 20px;
        font-size: 22px;
        font-weight: bold;
        background-color: #D32F2F; /* Red Color */
        color: white;
        border: 2px solid #B71C1C;
        box-shadow: 0px 6px 15px rgba(211, 47, 47, 0.3);
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #FF5252;
        border-color: #D32F2F;
        color: white;
    }
    
    /* میٹرک باکسز (Summary) کا ڈیزائن */
    [data-testid="stMetric"] {
        background-color: #FFEBEE;
        border: 2px solid #FFCDD2;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    [data-testid="stMetricLabel"] { color: #B71C1C; font-weight: bold; }
    [data-testid="stMetricValue"] { color: #D32F2F; }
    
    /* ٹائٹل اسٹائل */
    .shop-title {
        color: #D32F2F;
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        margin-bottom: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو یا تصویر کے لیے جگہ
col_logo_left, col_logo_mid, col_logo_right = st.columns([1, 1, 1])
with col_logo_mid:
    # یہاں آپ اپنی تصویر کا لنک ڈال سکیں گے
    st.markdown("<div style='text-align: center; padding: 20px; border: 2px dashed #D32F2F; border-radius: 50%; color: #D32F2F;'>آپ کی تصویر یہاں آئے گی</div>", unsafe_allow_html=True)

# شاپ کا نام (English)
st.markdown("<h1 class='shop-title'>Ali Mobiles & Communication</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Professional Shop Management System</p>", unsafe_allow_html=True)

# 4. ڈیٹا لوڈنگ
DATA_FILE = "ali_pro_v5.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    else:
        return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()

# پیج کنٹرولر
if 'page' not in st.session_state: st.session_state.page = "home"
def set_page(page_name): st.session_state.page = page_name

# 5. آج کا حساب کتاب (Red Summary Boxes)
today = datetime.now().date()
today_df = df[df['تاریخ'].dt.date == today] if not df.empty else df
cash_p = today_df[(today_df['اسٹیٹس'] == "نقد") & (today_df['کیٹیگری'] != "گھر کا خرچ")]['منافع'].sum()
home_e = today_df[today_df['کیٹیگری'] == "گھر کا خرچ"]['فروخت'].sum()
udhaar_t = today_df[today_df['اسٹیٹس'] == "ادھار"]['فروخت'].sum()
savings = cash_p - home_e

st.write("---")
m1, m2, m3, m4 = st.columns(4)
m1.metric("نقد منافع", f"{cash_p} PKR")
m2.metric("گھر کا خرچ", f"{home_e} PKR")
m3.metric("آج کا ادھار", f"{udhaar_t} PKR")
m4.metric("خالص بچت", f"{savings} PKR")

st.write("## ") # Space

# 6. مین مینو بٹن (Red Tiles)
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("➕\nNew Entry", key="n"): set_page("new")
with c2:
    if st.button("📓\nCredit List", key="u"): set_page("udhaar")
with c3:
    if st.button("📅\nHistory", key="h"): set_page("hist")
with c4:
    if st.button("🏠\nHome", key="hm"): set_page("home")

st.divider()

# 7. پیجز کی تفصیل
if st.session_state.page == "home":
    st.subheader("📋 آج کی سیل کا ریکارڈ")
    st.dataframe(today_df.sort_values(by="تاریخ", ascending=False), use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نیا ریکارڈ درج کریں")
    with st.form("entry", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        detail = st.text_input("تفصیل")
        status = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        col_x, col_y = st.columns(2)
        cost = col_x.number_input("لاگت (Cost)", min_value=0)
        sale = col_y.number_input("وصولی (Sale)", min_value=0)
        if st.form_submit_button("Save Record"):
            profit = 0 if cat == "Home Expense" else (sale - cost)
            new_data = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": detail, "خریداری": cost, "فروخت": sale, "منافع": profit, "اسٹیٹس": status}
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("ریکارڈ محفوظ ہو گیا!")
            st.rerun()

elif st.session_state.page == "udhaar":
    st.subheader("📓 ادھار کی لسٹ")
    u_list = df[df['اسٹیٹس'] == "ادھار"]
    st.table(u_list[["تاریخ", "تفصیل", "فروخت"]]) if not u_list.empty else st.info("کوئی ادھار نہیں ہے")

elif st.session_state.page == "hist":
    st.subheader("📅 مکمل تاریخ")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
