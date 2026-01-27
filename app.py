import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobile Shop Pro", layout="wide")

# کسٹم اسٹائلنگ (ایرر فکسڈ)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# ڈیٹا فائل کا نام
DATA_FILE = "ali_mobile_pro_final.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    else:
        return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()

# مینو
st.sidebar.title("📱 علی موبائل مینو")
choice = st.sidebar.radio("سیکشن منتخب کریں", ["📊 ڈیش بورڈ", "📝 نئی انٹری", "📓 ادھار ریکارڈ", "📅 مکمل تاریخ"])

# --- ڈیش بورڈ ---
if choice == "📊 ڈیش بورڈ":
    st.title("🚀 علی موبائل شاپ ڈیش بورڈ")
    
    today = datetime.now().date()
    # اگر ڈیٹا خالی نہ ہو تو آج کا ریکارڈ فلٹر کریں
    if not df.empty:
        df['تاریخ_صرف'] = df['تاریخ'].dt.date
        today_df = df[df['تاریخ_صرف'] == today]
    else:
        today_df = df

    # حساب کتاب
    cash_profit = today_df[(today_df['اسٹیٹس'] == "نقد") & (today_df['کیٹیگری'] != "گھر کا خرچ")]['منافع'].sum()
    home_exp = today_df[today_df['کیٹیگری'] == "گھر کا خرچ"]['فروخت'].sum()
    today_udhaar = today_df[today_df['اسٹیٹس'] == "ادھار"]['فروخت'].sum()
    net_cash = cash_profit - home_exp

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 نقد منافع (آج)", f"{cash_profit} PKR")
    with col2:
        st.error(f"🏠 گھر خرچ: {home_exp}")
    with col3:
        st.warning(f"📝 آج کا ادھار: {today_udhaar}")
    with col4:
        st.info(f"💵 خالص بچت: {net_cash}")

    st.divider()
    st.subheader("آج کی تمام انٹریز")
    st.dataframe(today_df.drop(columns=['تاریخ_صرف'], errors='ignore'), use_container_width=True)

# --- نئی انٹری ---
elif choice == "📝 نئی انٹری":
    st.title("➕ نیا ریکارڈ درج کریں")
    with st.form("entry_form", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری", ["ایسیسریز", "ریپیرنگ", "ایزی پیسہ/جائز کیش", "گھر کا خرچ"])
        detail = st.text_input("تفصیل (آئٹم یا گاہک کا نام)")
        
        status = "نقد"
        if cat != "گھر کا خرچ":
            status = st.radio("ادائیگی کی قسم", ["نقد", "ادھار"], horizontal=True)
            
        col_a, col_b = st.columns(2)
        with col_a:
            cost = st.number_input("خریداری / لاگت", min_value=0)
        with col_b:
            sale = st.number_input("فروخت / وصولی", min_value=0)
            
        submit = st.form_submit_button("محفوظ کریں")
        
        if submit:
            profit = 0 if cat == "گھر کا خرچ" else (sale - cost)
            new_row = {
                "تاریخ": datetime.now(),
                "کیٹیگری": cat,
                "تفصیل": detail,
                "خریداری": cost,
                "فروخت": sale,
                "منافع": profit,
                "اسٹیٹس": status
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("ریکارڈ محفوظ ہو گیا!")

# --- ادھار ریکارڈ ---
elif choice == "📓 ادھار ریکارڈ":
    st.title("📓 ادھار کی لسٹ")
    udhaar_list = df[df['اسٹیٹس'] == "ادھار"]
    if not udhaar_list.empty:
        st.table(udhaar_list[["تاریخ", "تفصیل", "فروخت"]])
        st.subheader(f"کل واجب الادا ادھار: {udhaar_list['فروخت'].sum()} PKR")
    else:
        st.success("فی الحال کوئی ادھار نہیں ہے!")

# --- مکمل تاریخ ---
elif choice == "📅 مکمل تاریخ":
    st.title("📅 مکمل ریکارڈز")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
    
