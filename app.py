import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ایپ کی سیٹنگ
st.set_page_config(page_title="Ali Mobile Shop Pro", layout="wide")

# کسٹم کلر اسٹائلنگ (EasyPaisa اسٹائل)
st.markdown("""
    <style>
    div.stButton > button {
        height: 100px;
        width: 100%;
        border-radius: 15px;
        font-size: 20px;
        font-weight: bold;
        color: white;
        border: none;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    /* بٹنوں کے رنگ */
    .st-emotion-cache-16idsys p { font-size: 22px; }
    </style>
    """, unsafe_allow_html=True)

# ڈیٹا لوڈنگ
DATA_FILE = "ali_mobile_final_v4.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    else:
        return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()

# پیج کنٹرولر (فرنٹ پیج کے لیے)
if 'page' not in st.session_state:
    st.session_state.page = "home"

def set_page(page_name):
    st.session_state.page = page_name

# --- فرنٹ پیج (EasyPaisa اسٹائل) ---
st.title("🚀 علی موبائل شاپ - ہوم")
st.divider()

# آج کا حساب کتاب (اوپر والے رنگین باکس)
today = datetime.now().date()
today_df = df[df['تاریخ'].dt.date == today] if not df.empty else df
cash_profit = today_df[(today_df['اسٹیٹس'] == "نقد") & (today_df['کیٹیگری'] != "گھر کا خرچ")]['منافع'].sum()
home_exp = today_df[today_df['کیٹیگری'] == "گھر کا خرچ"]['فروخت'].sum()
today_udhaar = today_df[today_df['اسٹیٹس'] == "ادھار"]['فروخت'].sum()
net_cash = cash_profit - home_exp

m1, m2, m3, m4 = st.columns(4)
with m1: st.success(f"💰 نقد منافع\n\n {cash_profit} PKR")
with m2: st.error(f"🏠 گھر خرچ\n\n {home_exp} PKR")
with m3: st.warning(f"📝 آج کا ادھار\n\n {today_udhaar} PKR")
with m4: st.info(f"💵 خالص بچت\n\n {net_cash} PKR")

st.write("## ") # تھوڑی جگہ چھوڑنے کے لیے

# مین مینیو باکسز (بڑے رنگین بٹن)
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("➕\nنئی انٹری", key="btn_new", use_container_width=True): set_page("new")
with c2:
    if st.button("📓\nادھار لسٹ", key="btn_udhaar", use_container_width=True): set_page("udhaar")
with c3:
    if st.button("📅\nمکمل ہسٹری", key="btn_hist", use_container_width=True): set_page("history")
with c4:
    if st.button("🏠\nہوم پیج", key="btn_home", use_container_width=True): set_page("home")

st.divider()

# --- پیجز کے فنکشنز ---

if st.session_state.page == "home":
    st.subheader("📋 آج کی حالیہ انٹریز")
    st.dataframe(today_df.sort_values(by="تاریخ", ascending=False), use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نیا ریکارڈ درج کریں")
    with st.form("entry_form", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری منتخب کریں", ["ایسیسریز", "ریپیرنگ", "ایزی پیسہ/جائز کیش", "گھر کا خرچ"])
        detail = st.text_input("تفصیل (آئٹم یا گاہک کا نام)")
        status = "نقد"
        if cat != "گھر کا خرچ":
            status = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True)
        col_a, col_b = st.columns(2)
        with col_a: cost = st.number_input("خریداری / لاگت", min_value=0)
        with col_b: sale = st.number_input("فروخت / وصولی", min_value=0)
        if st.form_submit_button("محفوظ کریں"):
            profit = 0 if cat == "گھر کا خرچ" else (sale - cost)
            new_row = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": detail, "خریداری": cost, "فروخت": sale, "منافع": profit, "اسٹیٹس": status}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("ریکارڈ محفوظ ہو گیا!")
            st.rerun()

elif st.session_state.page == "udhaar":
    st.subheader("📓 ادھار کی مکمل تفصیل")
    u_list = df[df['اسٹیٹس'] == "ادھار"]
    if not u_list.empty:
        st.table(u_list[["تاریخ", "تفصیل", "فروخت"]])
        st.error(f"ٹوٹل واجب الادا رقم: {u_list['فروخت'].sum()} PKR")
    else:
        st.success("کوئی ادھار باقی نہیں ہے!")

elif st.session_state.page == "history":
    st.subheader("📅 تمام پرانا ریکارڈ")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
        
