import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی ڈیزائن (EasyPaisa & JazzCash Style)
st.markdown("""
    <style>
    /* مین بیک گراؤنڈ */
    .stApp { background-color: #f4f6f9; }
    
    /* ٹائٹل بار */
    .header-box {
        background: linear-gradient(90deg, #d32f2f, #b71c1c);
        padding: 20px;
        border-radius: 0px 0px 30px 30px;
        text-align: center;
        color: white;
        margin-top: -60px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
    }
    
    /* کلر فل کارڈز (Summary) */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        text-align: center;
        border-bottom: 5px solid #d32f2f;
    }
    
    /* بڑے ایکشن بٹن (Boxes) */
    div.stButton > button {
        height: 120px;
        width: 100%;
        border-radius: 25px;
        font-size: 20px;
        font-weight: bold;
        color: white;
        border: none;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.15);
        transition: 0.3s;
    }
    /* بٹنوں کے الگ الگ رنگ */
    button[kind="secondary"]:nth-child(1) { background: linear-gradient(45deg, #FF512F, #DD2476); } /* New Entry */
    
    .stTable { background-color: white; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو اور ہیڈر
col_l, col_m, col_r = st.columns([1, 2, 1])
with col_m:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<div style='text-align:center; color:#d32f2f; font-weight:bold;'>[Logo Placeholder]</div>", unsafe_allow_html=True)

st.markdown("""
    <div class="header-box">
        <h1 style='margin:0;'>Ali Mobiles & Communication</h1>
        <p style='margin:0; opacity:0.8;'>Professional Shop Management</p>
    </div>
    """, unsafe_allow_html=True)

# 4. ڈیٹا مینجمنٹ
DATA_FILE = "ali_shop_vip_v7.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()

if 'page' not in st.session_state: st.session_state.page = "home"
def go_to(p): st.session_state.page = p

# 5. رنگین ڈیش بورڈ (Today Summary)
st.write("## ")
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else df

# کیٹیگری وائز حساب
rep_p = t_df[t_df['کیٹیگری'] == "Repairing"]['منافع'].sum()
acc_p = t_df[t_df['کیٹیگری'] == "Accessories"]['منافع'].sum()
bank_p = t_df[t_df['کیٹیگری'] == "Banking"]['فروخت'].sum() # Banking normally means commission
home_e = t_df[t_df['کیٹیگری'] == "Home Expense"]['فروخت'].sum()
total_p = (rep_p + acc_p + bank_p) - home_e

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='metric-card'><p style='color:green;margin:0;'>کل پرافٹ</p><h2 style='margin:0;'>{total_p}</h2></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='metric-card' style='border-color:blue;'><p style='color:blue;margin:0;'>ریپیرنگ</p><h2 style='margin:0;'>{rep_p}</h2></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='metric-card' style='border-color:orange;'><p style='color:orange;margin:0;'>بینکنگ</p><h2 style='margin:0;'>{bank_p}</h2></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='metric-card' style='border-color:red;'><p style='color:red;margin:0;'>گھر خرچ</p><h2 style='margin:0;'>{home_e}</h2></div>", unsafe_allow_html=True)

# 6. ایکشن بٹن (EasyPaisa Style Tiles)
st.write("## ")
b1, b2, b3, b4 = st.columns(4)
with b1: 
    if st.button("➕\nNew Entry", key="b1"): go_to("new")
with b2: 
    if st.button("📓\nCredit List", key="b2"): go_to("credit")
with b3: 
    if st.button("📅\nHistory", key="b3"): go_to("history")
with b4: 
    if st.button("🏠\nHome", key="b4"): go_to("home")

st.divider()

# 7. پیجز کی تفصیل
if st.session_state.page == "home":
    st.subheader("📋 آج کی کارکردگی")
    if not t_df.empty:
        st.table(t_df[["کیٹیگری", "تفصیل", "فروخت", "منافع", "اسٹیٹس"]].sort_index(ascending=False))
    else:
        st.info("آج ابھی تک کوئی انٹری نہیں ہوئی۔")

elif st.session_state.page == "new":
    st.subheader("📝 نیا ریکارڈ شامل کریں")
    with st.form("vip_form", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری منتخب کریں", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل (آئٹم یا گاہک کا نام)")
        pay = st.radio("ادائیگی", ["Cash", "Credit"], horizontal=True) if cat != "Home Expense" else "Cash"
        
        col1, col2 = st.columns(2)
        cost = col1.number_input("خریداری قیمت (Cost)", min_value=0)
        sale = col2.number_input("فروخت قیمت (Sale)", min_value=0)
        
        if st.form_submit_button("Save Record"):
            prof = 0 if cat == "Home Expense" else (sale - cost)
            new_r = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": prof, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([new_r])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("ریکارڈ سیو ہو گیا!")
            st.rerun()

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار کی لسٹ")
    c_list = df[df['اسٹیٹس'] == "Credit"]
    if not c_list.empty:
        st.table(c_list[["تاریخ", "تفصیل", "فروخت"]])
        st.error(f"ٹوٹل ادھار: {c_list['فروخت'].sum()} PKR")
    else: st.success("کوئی ادھار نہیں ہے!")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ہسٹری")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
