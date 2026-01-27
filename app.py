import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی ڈیزائن (CSS) - مکمل فکسڈ
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 0.5rem !important; }
    .stApp { background-color: #ffffff; }
    
    /* تمام بٹنوں کو بڑے ڈبوں کی شکل دینا */
    div.stButton > button {
        height: 150px !important;
        width: 100% !important;
        border-radius: 20px !important;
        font-size: 22px !important;
        font-weight: 800 !important;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.2) !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-bottom: 10px !important;
        white-space: pre-wrap !important;
        line-height: 1.2 !important;
    }

    /* ہوور ایفیکٹ */
    div.stButton > button:hover { 
        transform: translateY(-5px);
        box-shadow: 0px 12px 20px rgba(0,0,0,0.3) !important;
        transition: 0.3s;
    }

    /* ہر بٹن کے لیے الگ اور پکا گہرا رنگ */
    /* Row 1 */
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) button { background: linear-gradient(135deg, #1b5e20, #2e7d32) !important; }
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) button { background: linear-gradient(135deg, #0d47a1, #1e88e5) !important; }
    
    /* Row 2 */
    div[data-testid="stHorizontalBlock"]:nth-of-type(3) > div:nth-child(1) button { background: linear-gradient(135deg, #b71c1c, #d32f2f) !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(3) > div:nth-child(2) button { background: linear-gradient(135deg, #e65100, #ff9800) !important; }
    
    /* Row 3 */
    div[data-testid="stHorizontalBlock"]:nth-of-type(4) > div:nth-child(1) button { background: linear-gradient(135deg, #4a148c, #6a1b9a) !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(4) > div:nth-child(2) button { background: linear-gradient(135deg, #006064, #00838f) !important; }
    
    /* Row 4 */
    div[data-testid="stHorizontalBlock"]:nth-of-type(5) > div:nth-child(1) button { background: linear-gradient(135deg, #c2185b, #ad1457) !important; }
    div[data-testid="stHorizontalBlock"]:nth-of-type(5) > div:nth-child(2) button { background: linear-gradient(135deg, #263238, #37474f) !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو
col1, col2, col3 = st.columns([1, 0.4, 1])
with col2:
    if os.path.exists("logo.png"): st.image("logo.png", use_container_width=True)

# 4. ڈیٹا ہینڈلنگ
DATA_FILE = "ali_shop_v20_final.csv"
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

# --- 8 بڑے رنگین بٹن (ڈیش بورڈ) ---

# قطار 1
r1_c1, r1_c2 = st.columns(2)
with r1_c1: 
    if st.button(f"📊\n\nکل نقد پرافٹ\n\nRs. {cp}", key="btn_p"): nav("profit_details")
with r1_c2: 
    if st.button(f"🔧\n\nریپیرنگ پرافٹ\n\nRs. {rep}", key="btn_r"): nav("repair_details")

# قطار 2
r2_c1, r2_c2 = st.columns(2)
with r2_c1: 
    if st.button(f"🏠\n\nگھر کا خرچ\n\nRs. {he}", key="btn_e"): nav("expense_details")
with r2_c2: 
    if st.button(f"💰\n\nایزی پیسہ سیل\n\nRs. {bank}", key="btn_b"): nav("banking_details")

# قطار 3
r3_c1, r3_c2 = st.columns(2)
with r3_c1: 
    if st.button("➕\n\nنئی انٹری\n(NEW ENTRY)", key="btn_new"): nav("new")
with r3_c2: 
    if st.button("📓\n\nادھار لسٹ\n(CREDIT LIST)", key="btn_credit"): nav("credit")

# قطار 4
r4_c1, r4_c2 = st.columns(2)
with r4_c1: 
    if st.button("📅\n\nمکمل ہسٹری\n(HISTORY)", key="btn_hist"): nav("history")
with r4_c2: 
    if st.button("🏠\n\nہوم پیج\n(HOME)", key="btn_home"): nav("home")

st.divider()

# 6. پیجز کی تفصیل (بٹن دبانے پر یہاں کھلیں گے)
if st.session_state.page == "home":
    st.subheader("📋 آج کی کارکردگی")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نیا ڈیٹا درج کریں")
    with st.form("ali_form", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        v1, v2 = st.columns(2)
        cost = v1.number_input("لاگت (Cost)", min_value=0)
        sale = v2.number_input("وصولی (Sale)", min_value=0)
        if st.form_submit_button("سیو کریں 💾"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            new_r = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": p, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([new_r])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("ریکارڈ محفوظ ہو گیا!"); nav("home")

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار کی لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    st.table(cl[["تاریخ", "تفصیل", "فروخت"]]) if not cl.empty else st.info("کوئی ادھار نہیں ہے۔")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ریکارڈ")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)

elif st.session_state.page == "profit_details":
    st.subheader("💰 نقد پرافٹ کی تفصیلات")
    st.dataframe(df[(df['اسٹیٹس']=="نقد") & (df['کیٹیگری']!="Home Expense")], use_container_width=True)

elif st.session_state.page == "repair_details":
    st.subheader("🔧 ریپیرنگ کی تفصیلات")
    st.dataframe(df[df['کیٹیگری'] == "Repairing"], use_container_width=True)

elif st.session_state.page == "expense_details":
    st.subheader("🏠 گھر کے خرچ کی تفصیل")
    st.dataframe(df[df['کیٹیگری'] == "Home Expense"], use_container_width=True)

elif st.session_state.page == "banking_details":
    st.subheader("💰 بینکنگ تفصیلات")
    st.dataframe(df[df['کیٹیگری'] == "Banking"], use_container_width=True)
    
