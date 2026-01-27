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
    
    /* تمام ڈبوں (Metrics & Buttons) کا ایک جیسا پروفیشنل ڈیزائن */
    .big-tile {
        height: 140px; 
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: white !important;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.2);
        margin-bottom: 15px;
        border: 2px solid rgba(255,255,255,0.1);
    }
    .tile-name { font-size: 14px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .tile-data { font-size: 36px; font-weight: 900; }

    /* اسٹریم لٹ بٹن کو ٹائل جیسا بنانا */
    div.stButton > button {
        height: 140px !important;
        width: 100% !important;
        border-radius: 20px !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        color: white !important;
        border: none !important;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.2) !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: 0.3s;
    }
    div.stButton > button:hover { transform: scale(0.97); opacity: 0.9; }

    /* 8 پروفیشنل گہرے رنگ */
    .bg-green { background: linear-gradient(135deg, #1b5e20, #2e7d32); }
    .bg-blue { background: linear-gradient(135deg, #0d47a1, #1e88e5); }
    .bg-red { background: linear-gradient(135deg, #b71c1c, #d32f2f); }
    .bg-orange { background: linear-gradient(135deg, #e65100, #ff9800); }
    
    /* بٹنوں کے رنگ */
    button[key="btn_new"] { background: linear-gradient(135deg, #4a148c, #8e24aa) !important; }
    button[key="btn_credit"] { background: linear-gradient(135deg, #006064, #0097a7) !important; }
    button[key="btn_hist"] { background: linear-gradient(135deg, #c2185b, #e91e63) !important; }
    button[key="btn_home"] { background: linear-gradient(135deg, #263238, #455a64) !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو
cl1, cl2, cl3 = st.columns([1, 0.4, 1])
with cl2:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)

# 4. ڈیٹا ہینڈلنگ
DATA_FILE = "ali_shop_v19_final.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()
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

# --- 8 بڑے رنگین ڈبے (2 Columns) ---

# Row 1
c1, c2 = st.columns(2)
with c1: st.markdown(f"<div class='big-tile bg-green'><div class='tile-name'>کل نقد پرافٹ</div><div class='tile-data'>{cp}</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='big-tile bg-blue'><div class='tile-name'>ریپیرنگ پرافٹ</div><div class='tile-data'>{rep}</div></div>", unsafe_allow_html=True)

# Row 2
c3, c4 = st.columns(2)
with c3: st.markdown(f"<div class='big-tile bg-red'><div class='tile-name'>گھر کا خرچ</div><div class='tile-data'>{he}</div></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='big-tile bg-orange'><div class='tile-name'>ایزی پیسہ سیل</div><div class='tile-data'>{bank}</div></div>", unsafe_allow_html=True)

# Row 3 (Buttons)
c5, c6 = st.columns(2)
with c5: 
    if st.button("➕\nنئی انٹری\n(NEW ENTRY)", key="btn_new"): nav("new")
with c6: 
    if st.button("📓\nادھار لسٹ\n(CREDIT LIST)", key="btn_credit"): nav("credit")

# Row 4 (Buttons)
c7, c8 = st.columns(2)
with c7: 
    if st.button("📅\nمکمل ہسٹری\n(HISTORY)", key="btn_hist"): nav("history")
with c8: 
    if st.button("🏠\nہوم پیج\n(HOME)", key="btn_home"): nav("home")

st.divider()

# 6. پیجز کا ڈیٹا
if st.session_state.page == "home":
    st.subheader("📋 آج کا ریکارڈ")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 ڈیٹا درج کریں")
    with st.form("ali_form"):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        v1, v2 = st.columns(2)
        cost = v1.number_input("خریداری (Cost)", min_value=0)
        sale = v2.number_input("وصولی (Sale)", min_value=0)
        if st.form_submit_button("محفوظ کریں"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            new_r = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": p, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([new_r])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("محفوظ ہو گیا!")
            nav("home")

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    if not cl.empty:
        st.table(cl[["تاریخ", "تفصیل", "فروخت"]])
        st.error(f"ٹوٹل ادھار: {cl['فروخت'].sum()} PKR")
    else: st.info("کوئی ادھار نہیں ہے۔")

elif st.session_state.page == "history":
    st.subheader("📅 دکان کا مکمل ڈیٹا")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
    
