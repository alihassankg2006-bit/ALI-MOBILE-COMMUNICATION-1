import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ سیٹنگ
st.set_page_config(page_title="Ali Mobiles", layout="wide")

# 2. الٹرا کومپیکٹ ڈیزائن (CSS)
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 0.5rem !important; }
    .stApp { background-color: #ffffff; }
    
    /* چھوٹے اور رنگین ڈبوں کا ڈیزائن */
    div.stButton > button {
        height: 90px !important;
        width: 100% !important;
        border-radius: 12px !important;
        font-size: 14px !important;
        font-weight: bold !important;
        color: white !important;
        border: none !important;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.2) !important;
        margin-bottom: 5px !important;
        white-space: pre-wrap !important;
        line-height: 1.1 !important;
    }
    
    /* 8 الگ گہرے رنگ */
    button[key="p"] { background: linear-gradient(135deg, #1b5e20, #2e7d32) !important; }
    button[key="r"] { background: linear-gradient(135deg, #0d47a1, #1e88e5) !important; }
    button[key="e"] { background: linear-gradient(135deg, #b71c1c, #d32f2f) !important; }
    button[key="b"] { background: linear-gradient(135deg, #e65100, #ff9800) !important; }
    button[key="new"] { background: linear-gradient(135deg, #4a148c, #6a1b9a) !important; }
    button[key="crd"] { background: linear-gradient(135deg, #006064, #00838f) !important; }
    button[key="hst"] { background: linear-gradient(135deg, #c2185b, #ad1457) !important; }
    button[key="hm"] { background: linear-gradient(135deg, #263238, #37474f) !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. ڈیٹا ہینڈلنگ اور ریبوٹ (Reset) فنکشن
DATA_FILE = "ali_shop_v25.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

# سائیڈ بار میں ریبوٹ کا آپشن
with st.sidebar:
    st.header("⚙️ سیٹنگز")
    if st.button("🚨 Reboot (Clear All Data)"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            st.success("سارا ڈیٹا ختم کر دیا گیا!")
            st.rerun()

df = load_data()
if 'page' not in st.session_state: st.session_state.page = "home"
def nav(p):
    st.session_state.page = p
    st.rerun()

# 4. حساب کتاب
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else df
cp = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
rep = t_df[t_df['کیٹیگری']=="Repairing"]['منافع'].sum()
he = t_df[t_df['کیٹیگری']=="Home Expense"]['فروخت'].sum()
bank = t_df[t_df['کیٹیگری']=="Banking"]['فروخت'].sum()

# 5. لوگو
cl1, cl2, cl3 = st.columns([1, 0.4, 1])
with cl2:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)

# 6. 8 چھوٹے ڈبے (4 Columns per row) - تاکہ اسکرول نہ کرنا پڑے
r1c1, r1c2, r1c3, r1c4 = st.columns(4)
with r1c1: 
    if st.button(f"📊\nنقد\n{cp}", key="p"): nav("home")
with r1c2: 
    if st.button(f"🔧\nریپیرنگ\n{rep}", key="r"): nav("history")
with r1c3: 
    if st.button(f"🏠\nخرچہ\n{he}", key="e"): nav("home")
with r1c4: 
    if st.button(f"💰\nبینکنگ\n{bank}", key="b"): nav("home")

r2c1, r2c2, r2c3, r2c4 = st.columns(4)
with r2c1: 
    if st.button("➕\nENTRY", key="new"): nav("new")
with r2c2: 
    if st.button("📓\nCREDIT", key="crd"): nav("credit")
with r2c3: 
    if st.button("📅\nHISTORY", key="hst"): nav("history")
with r2c4: 
    if st.button("🏠\nHOME", key="hm"): nav("home")

st.divider()

# 7. پیجز کی تفصیل
if st.session_state.page == "new":
    st.markdown("### 📝 نئی انٹری")
    with st.form("ali_f", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        c1, c2 = st.columns(2)
        cost = c1.number_input("خریداری", min_value=0)
        sale = c2.number_input("وصولی", min_value=0)
        if st.form_submit_button("محفوظ کریں"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            nr = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": p, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([nr])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("سیو ہو گیا!")
            nav("home")

elif st.session_state.page == "home":
    st.subheader("📋 آج کا ریکارڈ")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    st.table(cl[["تاریخ", "تفصیل", "فروخت"]]) if not cl.empty else st.info("کوئی ادھار نہیں")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ہسٹری")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
    
