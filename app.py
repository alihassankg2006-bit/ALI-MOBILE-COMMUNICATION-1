import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobile Shop Pro", layout="wide")

# کسٹم کلر اسٹائلنگ
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_stdio=True)

# ڈیٹا فائل لوڈ کرنا
DATA_FILE = "ali_shop_pro.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'])
        return df
    else:
        return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "آئٹم/تفصیل", "خریداری/کوسٹ", "فروخت/آمدن", "منافع"])

df = load_data()

# سائیڈ بار مینو
st.sidebar.title("📱 علی موبائل مینو")
menu = ["📊 ڈیش بورڈ", "📝 نئی انٹری", "📅 ریکارڈ ہسٹری"]
choice = st.sidebar.radio("کدھر جانا ہے؟", menu)

# --- ڈیش بورڈ ---
if choice == "📊 ڈیش بورڈ":
    st.title("🚀 علی موبائل شاپ ڈیش بورڈ")
    
    # آج کا ڈیٹا
    today = datetime.now().date()
    today_df = df[df['تاریخ'].dt.date == today]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("آج کا کل منافع", f"{today_df['منافع'].sum()} PKR", delta_color="normal")
    with col2:
        rep_p = today_df[today_df['کیٹیگری'] == "ریپیرنگ"]['منافع'].sum()
        st.info(f"🛠 ریپیرنگ منافع: {rep_p}")
    with col3:
        acc_p = today_df[today_df['کیٹیگری'] == "ایسیسریز"]['منافع'].sum()
        st.success(f"🎧 ایسیسریز منافع: {acc_p}")
    with col4:
        bank_p = today_df[today_df['کیٹیگری'] == "ایزی پیسہ/جائز کیش"]['منافع'].sum()
        st.warning(f"💸 بینکنگ منافع: {bank_p}")

    st.divider()
    st.subheader("📈 حالیہ فروخت")
    st.dataframe(today_df.sort_values(by="تاریخ", ascending=False), use_container_width=True)

# --- نئی انٹری ---
elif choice == "📝 نئی انٹری":
    st.title("➕ نیا ریکارڈ درج کریں")
    
    with st.form("entry_form", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری منتخب کریں", ["ایسیسریز", "ریپیرنگ", "ایزی پیسہ/جائز کیش"])
        item = st.text_input("آئٹم یا گاہک کا نام")
        
        col_a, col_b = st.columns(2)
        with col_a:
            cost = st.number_input("خریداری قیمت / لاگت", min_value=0)
        with col_b:
            sale = st.number_input("فروخت قیمت / کل وصولی", min_value=0)
        
        submit = st.form_submit_button("سیو کریں")
        
        if submit:
            profit = sale - cost
            new_row = {
                "تاریخ": datetime.now(),
                "کیٹیگری": cat,
                "آئٹم/تفصیل": item,
                "خریداری/کوسٹ": cost,
                "فروخت/آمدن": sale,
                "منافع": profit
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success(f"ریکارڈ محفوظ! منافع: {profit} PKR")

# --- ریکارڈ ہسٹری ---
elif choice == "📅 ریکارڈ ہسٹری":
    st.title("📂 مکمل ریکارڈ دیکھیں")
    
    filter_type = st.radio("کیسا ریکارڈ دیکھنا ہے؟", ["ڈیلی", "منتھلی", "سالانہ"], horizontal=True)
    
    if filter_type == "ڈیلی":
        pick_date = st.date_input("تاریخ منتخب کریں", datetime.now())
        filtered_df = df[df['تاریخ'].dt.date == pick_date]
    elif filter_type == "منتھلی":
        month = st.selectbox("مہینہ", range(1, 13), index=datetime.now().month-1)
        filtered_df = df[(df['تاریخ'].dt.month == month) & (df['تاریخ'].dt.year == datetime.now().year)]
    else:
        year = st.selectbox("سال", [2025, 2026, 2027])
        filtered_df = df[df['تاریخ'].dt.year == year]
        
    st.write(f"### نتائج: {len(filtered_df)} انٹریز ملیں")
    st.table(filtered_df)
    st.metric("اس دورانیے کا کل منافع", f"{filtered_df['منافع'].sum()} PKR")
