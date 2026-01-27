import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobile Shop Pro", layout="wide")

# ڈیٹا فائل لوڈ کرنا
DATA_FILE = "ali_shop_pro_v2.csv"
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
    
    today = datetime.now().date()
    today_df = df[df['تاریخ'].dt.date == today]
    
    # حساب کتاب
    total_profit = today_df[today_df['کیٹیگری'] != "گھر کا خرچ"]['منافع'].sum()
    home_exp = today_df[today_df['کیٹیگری'] == "گھر کا خرچ"]['فروخت/آمدن'].sum()
    net_savings = total_profit - home_exp

    # رنگین کارڈز
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success(f"💰 آج کا کل پرافٹ: {total_profit} PKR")
    with col2:
        st.error(f"🏠 گھر کا خرچ: {home_exp} PKR")
    with col3:
        st.info(f"💵 باقی بچت: {net_savings} PKR")

    st.divider()
    
    # کیٹیگری وائز بریک ڈاؤن
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("🛠 ریپیرنگ پرافٹ:", today_df[today_df['کیٹیگری'] == "ریپیرنگ"]['منافع'].sum())
    with c2:
        st.write("🎧 ایسیسریز پرافٹ:", today_df[today_df['کیٹیگری'] == "ایسیسریز"]['منافع'].sum())
    with c3:
        st.write("💸 بینکنگ پرافٹ:", today_df[today_df['کیٹیگری'] == "ایزی پیسہ/جائز کیش"]['منافع'].sum())

    st.subheader("📝 آج کی تمام انٹریز")
    st.dataframe(today_df.sort_values(by="تاریخ", ascending=False), use_container_width=True)

# --- نئی انٹری ---
elif choice == "📝 نئی انٹری":
    st.title("➕ نیا ریکارڈ درج کریں")
    
    with st.form("entry_form", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری منتخب کریں", ["ایسیسریز", "ریپیرنگ", "ایزی پیسہ/جائز کیش", "گھر کا خرچ"])
        item = st.text_input("آئٹم / تفصیل (مثلاً: سبزی کے لیے، یا گاہک کا نام)")
        
        if cat == "گھر کا خرچ":
            amount = st.number_input("کتنے پیسے لے کر گئے؟", min_value=0)
            cost, sale = 0, amount
        else:
            col_a, col_b = st.columns(2)
            with col_a:
                cost = st.number_input("خریداری قیمت / لاگت", min_value=0)
            with col_b:
                sale = st.number_input("فروخت قیمت / وصولی", min_value=0)
        
        submit = st.form_submit_button("سیو کریں")
        
        if submit:
            profit = 0 if cat == "گھر کا خرچ" else (sale - cost)
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
            st.success("ریکارڈ محفوظ ہو گیا!")

# --- ریکارڈ ہسٹری ---
elif choice == "📅 ریکارڈ ہسٹری":
    st.title("📂 ریکارڈ چیک کریں")
    filter_type = st.radio("فلٹر", ["ڈیلی", "منتھلی", "سالانہ"], horizontal=True)
    
    if filter_type == "ڈیلی":
        pick_date = st.date_input("تاریخ", datetime.now())
        f_df = df[df['تاریخ'].dt.date == pick_date]
    elif filter_type == "منتھلی":
        m = st.selectbox("مہینہ", range(1, 13), index=datetime.now().month-1)
        f_df = df[(df['تاریخ'].dt.month == m) & (df['تاریخ'].dt.year == datetime.now().year)]
    else:
        y = st.selectbox("سال", [2025, 2026, 2027])
        f_df = df[df['تاریخ'].dt.year == y]
        
    st.table(f_df)
    st.write(f"### اس پیریڈ کا ٹوٹل پرافٹ: {f_df[f_df['کیٹیگری'] != 'گھر کا خرچ']['منافع'].sum()} PKR")
    st.write(f"### اس پیریڈ کا ٹوٹل گھر کا خرچ: {f_df[f_df['کیٹیگری'] == 'گھر کا خرچ']['فروخت/آمدن'].sum()} PKR")
