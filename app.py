import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. الٹرا ڈیپ کلر ڈیزائن (CSS)
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 0.5rem !important; }
    .stApp { background-color: #ffffff; }
    
    /* میٹرک ڈبوں کا ڈیزائن (پرافٹ، ریپیرنگ وغیرہ) */
    .metric-card {
        height: 140px; border-radius: 20px;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        text-align: center; color: white !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.2);
        margin-bottom: 15px;
    }
    .m-label { font-size: 14px; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
    .m-val { font-size: 34px; font-weight: 900; }

    /* تمام بٹنوں کو زبردستی رنگین بنانا */
    .stButton > button {
        height: 140px !important;
        width: 100% !important;
        border-radius: 20px !important;
        font-size: 22px !important;
        font-weight: 800 !important;
        color: white !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.2) !important;
        margin-bottom: 15px !important;
        border: none !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        white-space: pre-wrap !important;
    }

    /* ہر ڈبے اور بٹن کا اپنا پکا گہرا رنگ (Solid Gradients) */
    .bg-green { background: linear-gradient(135deg, #1b5e20, #2e7d32) !important; } /* Profit */
    .bg-blue { background: linear-gradient(135deg, #0d47a1, #1e88e5) !important; }  /* Repair */
    .bg-orange { background: linear-gradient(135deg, #e65100, #ff9800) !important; } /* Banking */
    .bg-red { background: linear-gradient(135deg, #b71c1c, #d32f2f) !important; }    /* Expense */

    /* بٹنوں کے رنگوں کو فکس کرنا (CSS کے ذریعے) */
    div.stButton > button[key="n"] { background: linear-gradient(135deg, #4a148c, #6a1b9a) !important; } /* Entry */
    div.stButton > button[key="c"] { background: linear-gradient(135deg, #006064, #00838f) !important; } /* Credit */
    div.stButton > button[key="h"] { background: linear-gradient(135deg, #c2185b, #ad1457) !important; } /* History */
    div.stButton > button[key="hm"] { background: linear-gradient(135deg, #263238, #37474f) !important; } /* Home */

    /* بٹن ہوور ایفیکٹ */
    .stButton > button:hover { opacity: 0.9; transform: scale(0.98); transition: 0.2s; }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو سیکشن (لوگو ہمیشہ رہے گا)
cl1, cl2, cl3 = st.columns([1, 0.4, 1])
with cl2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("<h2 style='text-align:center; color:#1b5e20;'>ALI MOBILES</h2>", unsafe_allow_html=True)

# 4. ڈیٹا لوڈنگ
DATA_FILE = "ali_shop_pro_v23.csv"
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

# 5. ڈیٹا کیلکولیشن
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else pd.DataFrame()
cp = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
rep = t_df[t_df['کیٹیگری']=="Repairing"]['منافع'].sum()
he = t_df[t_df['کیٹیگری']=="Home Expense"]['فروخت'].sum()
bank = t_df[t_df['کیٹیگری']=="Banking"]['فروخت'].sum()

# --- 8 بڑے رنگین ڈبے (Metrics & Buttons) ---

# Row 1: انٹری اور پرافٹ
row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    if st.button("➕\nنئی انٹری\n(ENTRY)", key="n"): nav("new")
with row1_col2:
    st.markdown(f"<div class='metric-card bg-green'><div class='m-label'>کل نقد پرافٹ</div><div class='m-val'>Rs. {cp}</div></div>", unsafe_allow_html=True)

# Row 2: ریپیرنگ اور کریڈٹ
row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    st.markdown(f"<div class='metric-card bg-blue'><div class='m-label'>ریپیرنگ پرافٹ</div><div class='m-val'>Rs. {rep}</div></div>", unsafe_allow_html=True)
with row2_col2:
    if st.button("📓\nادھار لسٹ\n(CREDIT)", key="c"): nav("credit")

# Row 3: ایزی پیسہ اور ہسٹری
row3_col1, row3_col2 = st.columns(2)
with row3_col1:
    st.markdown(f"<div class='metric-card bg-orange'><div class='m-label'>ایزی پیسہ سیل</div><div class='m-val'>Rs. {bank}</div></div>", unsafe_allow_html=True)
with row3_col2:
    if st.button("📅\nہسٹری\n(HISTORY)", key="h"): nav("history")

# Row 4: خرچہ اور ہوم
row4_col1, row4_col2 = st.columns(2)
with row4_col1:
    st.markdown(f"<div class='metric-card bg-red'><div class='m-label'>گھر کا خرچ</div><div class='m-val'>Rs. {he}</div></div>", unsafe_allow_html=True)
with row4_col2:
    if st.button("🏠\nہوم پیج\n(HOME)", key="hm"): nav("home")

st.divider()

# 6. پیجز کی تفصیل (بٹن دبانے پر یہاں کھلیں گے)
if st.session_state.page == "new":
    st.markdown("### 📝 نئی انٹری درج کریں")
    with st.form("ali_form", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل درج کریں")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        v1, v2 = st.columns(2)
        cost = v1.number_input("خریداری (Cost)", min_value=0)
        sale = v2.number_input("وصولی (Sale)", min_value=0)
        if st.form_submit_button("💾 ریکارڈ محفوظ کریں"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            nr = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": p, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([nr])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ ریکارڈ محفوظ ہو گیا!"); st.balloons(); st.session_state.page = "home"; st.rerun()

elif st.session_state.page == "home":
    st.subheader("📋 آج کی سیل کا ریکارڈ")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    if not cl.empty:
        st.dataframe(cl, use_container_width=True)
        st.error(f"کل ادھار: Rs. {cl['فروخت'].sum()}")
    else: st.info("کوئی ادھار نہیں ہے۔")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ہسٹری")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
    
