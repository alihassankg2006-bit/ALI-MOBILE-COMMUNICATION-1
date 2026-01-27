import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. الٹرا وی آئی پی ریڈ ڈیزائن (Ultra VIP Red CSS)
st.markdown("""
    <style>
    /* مین بیک گراؤنڈ - ہلکا گرے تاکہ لال رنگ اٹھے */
    .stApp { background-color: #e9ecef; }
    
    /* ہیڈر سیکشن */
    .header-container {
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 100%);
        padding: 30px;
        border-radius: 0 0 40px 40px;
        text-align: center;
        color: white;
        margin-top: -60px;
        box-shadow: 0px 10px 25px rgba(183, 28, 28, 0.5);
    }
    .shop-name { font-size: 42px; font-weight: 900; margin: 0; letter-spacing: 1px; }
    .shop-tagline { font-size: 18px; opacity: 0.9; margin-top: 5px; }

    /* ڈیش بورڈ کے بڑے سرخ ڈبے (Solid Red Boxes) */
    .full-red-box {
        background: linear-gradient(145deg, #D32F2F, #C62828);
        color: white !important;
        padding: 25px;
        border-radius: 25px;
        box-shadow: 0px 15px 25px rgba(211, 47, 47, 0.4);
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 3px solid #E57373; /* ہلکا سا بارڈر */
    }
    /* ڈبوں کے اندر بڑی لکھائی */
    .box-label { font-size: 22px; font-weight: 700; text-transform: uppercase; opacity: 0.9; margin-bottom: 10px; }
    .box-value { font-size: 55px; font-weight: 900; line-height: 1; }

    /* مینیو کے لمبے اور بڑے بٹن (Taller Buttons) */
    div.stButton > button {
        height: 180px; /* اونچائی بڑھا دی گئی ہے */
        width: 100%;
        border-radius: 30px;
        font-size: 26px;
        font-weight: bold;
        color: white;
        border: none;
        background: linear-gradient(135deg, #ff5252 0%, #d32f2f 100%);
        box-shadow: 0px 10px 20px rgba(211, 47, 47, 0.3);
        transition: transform 0.2s;
    }
    div.stButton > button:active { transform: scale(0.98); }
    
    /* ٹیبل کا ڈیزائن */
    .stTable { background: white; border-radius: 20px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو اور ہیڈر (تصویر کا کوڈ وہی ہے)
col_l, col_m, col_r = st.columns([1, 2, 1])
with col_m:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        # اگر تصویر نہ ہو تو یہ خوبصورت پلیس ہولڈر آئے گا
        st.markdown("""
            <div style='text-align:center; background:white; width:150px; height:150px; margin:auto; border-radius:50%; border:5px solid #d32f2f; display:flex; align-items:center; justify-content:center;'>
                <span style='color:#d32f2f; font-weight:bold;'>Upload<br>logo.png</span>
            </div>
            """, unsafe_allow_html=True)

st.markdown("""
    <div class="header-container">
        <h1 class='shop-name'>ALI MOBILES & COMMUNICATION</h1>
        <p class='shop-tagline'>Premium Shop Management System</p>
    </div>
    """, unsafe_allow_html=True)

# 4. ڈیٹا لوڈنگ
DATA_FILE = "ali_shop_ultra_vip.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()
if 'page' not in st.session_state: st.session_state.page = "home"
def go_to(p): st.session_state.page = p

# 5. ڈیش بورڈ کے بڑے سرخ ڈبے (Big Red Dashboard Boxes)
st.write("## ") # تھوڑی جگہ
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else df

# حساب کتاب
total_profit = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
repair_profit = t_df[t_df['کیٹیگری'] == "Repairing"]['منافع'].sum()
banking_sales = t_df[t_df['کیٹیگری'] == "Banking"]['فروخت'].sum()
home_expense = t_df[t_df['کیٹیگری'] == "Home Expense"]['فروخت'].sum()

# چار بڑے سرخ ڈبے
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='full-red-box'><div class='box-label'>کل نقد پرافٹ</div><div class='box-value'>{total_profit}</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='full-red-box'><div class='box-label'>ریپیرنگ پرافٹ</div><div class='box-value'>{repair_profit}</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='full-red-box'><div class='box-label'>ایزی پیسہ/بینکنگ</div><div class='box-value'>{banking_sales}</div></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='full-red-box'><div class='box-label'>گھر کا خرچ</div><div class='box-value'>{home_expense}</div></div>", unsafe_allow_html=True)

# 6. لمبے اور پروفیشنل مینیو بٹن (Taller Buttons)
st.write("## ")
st.write("### 🔽 کوئیک مینیو")
b1, b2, b3, b4 = st.columns(4)
with b1: 
    if st.button("➕ New Entry", key="b1"): go_to("new")
with b2: 
    if st.button("📓 Credit List", key="b2"): go_to("credit")
with b3: 
    if st.button("📅 Full History", key="b3"): go_to("history")
with b4: 
    if st.button("🏠 Dashboard", key="b4"): go_to("home")

st.divider()

# 7. پیجز کی تفصیل
if st.session_state.page == "home":
    st.subheader("📋 آج کی حالیہ انٹریز")
    st.dataframe(t_df.sort_values(by="تاریخ", ascending=False), use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نیا ریکارڈ شامل کریں")
    with st.form("vip_form_2", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        c1, c2 = st.columns(2)
        cost = c1.number_input("لاگت (Cost)", min_value=0)
        sale = c2.number_input("وصولی (Sale)", min_value=0)
        if st.form_submit_button("Save Record 💾"):
            prof = 0 if cat == "Home Expense" else (sale - cost)
            new_r = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": prof, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([new_r])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("محفوظ ہو گیا!")
            st.rerun()

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار کی لسٹ")
    c_list = df[df['اسٹیٹس'] == "ادھار"]
    if not c_list.empty:
        st.table(c_list[["تاریخ", "تفصیل", "فروخت"]])
        st.error(f"کل واجب الادا رقم: {c_list['فروخت'].sum()} PKR")
    else: st.success("کوئی ادھار باقی نہیں!")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل دکان کا ریکارڈ")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
    
