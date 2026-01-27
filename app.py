import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی بگ ٹائل ڈیزائن (CSS)
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 0.5rem !important; }
    .stApp { background-color: #ffffff; }
    
    /* ڈبوں کا ڈیزائن */
    .big-tile {
        height: 140px; 
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: white !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.2);
        margin-bottom: -140px; /* بٹن کو اس کے اوپر لانے کے لیے */
        position: relative;
        z-index: 1;
    }
    
    .tile-name { font-size: 15px; font-weight: bold; text-transform: uppercase; margin-bottom: 8px; }
    .tile-data { font-size: 34px; font-weight: 900; }
    .tile-icon { font-size: 32px; margin-bottom: 5px; }
    .tile-button-text { font-size: 16px; font-weight: 800; line-height: 1.2; }

    /* رنگین گریڈینٹس */
    .bg-purple { background: linear-gradient(135deg, #4a148c, #6a1b9a); border: 2px solid #ab47bc; }
    .bg-green { background: linear-gradient(135deg, #1b5e20, #2e7d32); border: 2px solid #4caf50; }
    .bg-blue { background: linear-gradient(135deg, #0d47a1, #1e88e5); border: 2px solid #42a5f5; }
    .bg-teal { background: linear-gradient(135deg, #006064, #00838f); border: 2px solid #26a69a; }
    .bg-orange { background: linear-gradient(135deg, #e65100, #ff9800); border: 2px solid #ffb74d; }
    .bg-pink { background: linear-gradient(135deg, #c2185b, #ad1457); border: 2px solid #ec407a; }
    .bg-red { background: linear-gradient(135deg, #b71c1c, #d32f2f); border: 2px solid #ef5350; }
    .bg-slate { background: linear-gradient(135deg, #263238, #37474f); border: 2px solid #78909c; }

    /* ٹرانسپیرنٹ بٹن جو پورے ڈبے کو کور کرے گا تاکہ کلک کام کرے */
    .stButton > button {
        height: 140px !important;
        width: 100% !important;
        background: transparent !important;
        color: transparent !important;
        border: none !important;
        position: relative;
        z-index: 10; /* سب سے اوپر */
        cursor: pointer;
        padding: 0 !important;
        margin: 0 !important;
    }
    .stButton > button:hover { background: rgba(255,255,255,0.1) !important; }
    
    /* فارم کے بٹن کو اصلی دکھائیں */
    form .stButton > button {
        background: #1b5e20 !important;
        color: white !important;
        height: auto !important;
        padding: 10px 20px !important;
        z-index: 1;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو سیکشن
st.markdown("<div style='text-align: center; margin-bottom: 20px;'><h2 style='color: #1b5e20; font-weight: 800;'>ALI MOBILES & COMMUNICATION</h2><p style='color: #666; font-size: 14px;'>Premium Shop Management System (Pakistan)</p></div>", unsafe_allow_html=True)

# 4. ڈیٹا ہینڈلنگ
DATA_FILE = "ali_shop_v20_final.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()

# پیج نیویگیشن
if 'page' not in st.session_state: st.session_state.page = "home"

def nav(p):
    st.session_state.page = p
    st.rerun()

# 5. حساب کتاب
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else df
cp = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
rep = t_df[t_df['کیٹیگری']=="Repairing"]['منافع'].sum()
he = t_df[t_df['کیٹیگری']=="Home Expense"]['فروخت'].sum()
bank = t_df[t_df['کیٹیگری']=="Banking"]['فروخت'].sum()

# --- 8 بڑے ڈبے ---

# Row 1: نئی انٹری اور کل پرافٹ
r1c1, r1c2 = st.columns(2)
with r1c1:
    st.markdown("<div class='big-tile bg-purple'><div class='tile-icon'>➕</div><div class='tile-button-text'>نئی انٹری<br>(NEW ENTRY)</div></div>", unsafe_allow_html=True)
    if st.button(" ", key="btn_new"): nav("new")
with r1c2:
    st.markdown(f"<div class='big-tile bg-green'><div class='tile-name'>کل نقد پرافٹ</div><div class='tile-data'>PKR {cp}</div></div>", unsafe_allow_html=True)
    if st.button(" ", key="btn_profit"): nav("profit_details")

# Row 2: ریپیرنگ اور ادھار
r2c1, r2c2 = st.columns(2)
with r2c1:
    st.markdown(f"<div class='big-tile bg-blue'><div class='tile-name'>ریپیرنگ پرافٹ</div><div class='tile-data'>PKR {rep}</div></div>", unsafe_allow_html=True)
    if st.button(" ", key="btn_repair"): nav("repair_details")
with r2c2:
    st.markdown("<div class='big-tile bg-teal'><div class='tile-icon'>📓</div><div class='tile-button-text'>ادھار لسٹ<br>(CREDIT LIST)</div></div>", unsafe_allow_html=True)
    if st.button(" ", key="btn_credit"): nav("credit")

# Row 3: ایزی پیسہ اور ہسٹری
r3c1, r3c2 = st.columns(2)
with r3c1:
    st.markdown(f"<div class='big-tile bg-orange'><div class='tile-name'>ایزی پیسہ سیل</div><div class='tile-data'>PKR {bank}</div></div>", unsafe_allow_html=True)
    if st.button(" ", key="btn_banking"): nav("banking_details")
with r3c2:
    st.markdown("<div class='big-tile bg-pink'><div class='tile-icon'>📅</div><div class='tile-button-text'>مکمل ہسٹری<br>(HISTORY)</div></div>", unsafe_allow_html=True)
    if st.button(" ", key="btn_history"): nav("history")

# Row 4: خرچہ اور ہوم
r4c1, r4c2 = st.columns(2)
with r4c1:
    st.markdown(f"<div class='big-tile bg-red'><div class='tile-name'>گھر کا خرچ</div><div class='tile-data'>PKR {he}</div></div>", unsafe_allow_html=True)
    if st.button(" ", key="btn_expense"): nav("expense_details")
with r4c2:
    st.markdown("<div class='big-tile bg-slate'><div class='tile-icon'>🏠</div><div class='tile-button-text'>ہوم پیج<br>(HOME)</div></div>", unsafe_allow_html=True)
    if st.button(" ", key="btn_home"): nav("home")

st.divider()

# 6. کلک کے بعد نیچے ظاہر ہونے والے حصے (پیجز)
if st.session_state.page == "new":
    st.markdown("### 📝 نئی انٹری شامل کریں")
    with st.form("ali_form", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل درج کریں")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        v1, v2 = st.columns(2)
        cost = v1.number_input("خریداری قیمت (Cost)", min_value=0)
        sale = v2.number_input("فروخت قیمت (Sale)", min_value=0)
        if st.form_submit_button("💾 ریکارڈ محفوظ کریں"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            new_r = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": p, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([new_r])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ ریکارڈ محفوظ ہو گیا!"); st.balloons(); nav("home")

elif st.session_state.page == "home":
    st.subheader("📋 آج کی کارکردگی")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار کی لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    if not cl.empty:
        st.dataframe(cl, use_container_width=True)
        st.error(f"کل ادھار رقم: PKR {cl['فروخت'].sum()}")
    else: st.success("🎉 کوئی ادھار نہیں ہے!")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ہسٹری")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)

elif st.session_state.page == "profit_details":
    st.subheader("💰 نقد پرافٹ کی تفصیل")
    st.dataframe(t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")], use_container_width=True)

elif st.session_state.page == "repair_details":
    st.subheader("🔧 ریپیرنگ کی تفصیل")
    st.dataframe(t_df[t_df['کیٹیگری'] == "Repairing"], use_container_width=True)

# فوٹر
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666; font-size: 12px;'>© 2024 Ali Mobiles & Communication | Premium Shop Management System</p>", unsafe_allow_html=True)
