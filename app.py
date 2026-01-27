import streamlit as st
import pandas as pd
from datetime import datetime
import os
from PIL import Image

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی ڈیزائن (CSS)
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    div.stButton > button {
        height: 120px;
        width: 100%;
        border-radius: 20px;
        font-size: 22px;
        font-weight: bold;
        background: linear-gradient(145deg, #d32f2f, #b71c1c);
        color: white;
        box-shadow: 0px 5px 15px rgba(183, 28, 28, 0.4);
    }
    [data-testid="stMetric"] {
        background-color: #fff5f5;
        border: 2px solid #ffcdd2;
        border-radius: 15px;
        text-align: center;
    }
    .shop-title {
        color: #b71c1c;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin-top: -10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. آپ کی تصویر اور لوگو (Header)
col_a, col_b, col_c = st.columns([1, 2, 1])
with col_b:
    # اگر آپ نے GitHub پر logo.png اپ لوڈ کی ہے تو یہ لائن اسے دکھائے گی
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        # اگر تصویر نہیں ملی تو یہ عارضی ڈیزائن دکھائے گا
        st.markdown("<div style='text-align: center; padding: 40px; border: 4px solid #b71c1c; border-radius: 20px; color: #b71c1c; font-weight: bold;'>Ali Mobiles VIP Logo & Photo Placeholder</div>", unsafe_allow_html=True)

st.markdown("<h1 class='shop-title'>Ali Mobiles & Communication</h1>", unsafe_allow_html=True)

# 4. ڈیٹا ہینڈلنگ
DATA_FILE = "ali_pro_v6.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()

# پیج کنٹرول
if 'page' not in st.session_state: st.session_state.page = "home"
def nav(p): st.session_state.page = p

# 5. آج کا خلاصہ
st.write("---")
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else df
cp = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
he = t_df[t_df['کیٹیگری']=="Home Expense"]['فروخت'].sum()
ut = t_df[t_df['اسٹیٹس']=="ادھار"]['فروخت'].sum()

m1, m2, m3, m4 = st.columns(4)
m1.metric("💰 Cash Profit", f"{cp}")
m2.metric("🏠 Home Exp", f"{he}")
m3.metric("📝 Credit", f"{ut}")
m4.metric("💵 Savings", f"{cp - he}")

# 6. مین مینیو بٹن
st.write("## ")
c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("➕\nNew Entry"): nav("new")
with c2: 
    if st.button("📓\nCredit List"): nav("udhaar")
with c3: 
    if st.button("📅\nHistory"): nav("hist")
with c4: 
    if st.button("🏠\nHome"): nav("home")

st.divider()

# 7. پیجز
if st.session_state.page == "home":
    st.subheader("📋 Today's Entries")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 Add Record")
    with st.form("f"):
        cat = st.selectbox("Category", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("Detail")
        stat = st.radio("Payment", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        cx, sx = st.columns(2)
        c_val = cx.number_input("Cost", min_value=0)
        s_val = sx.number_input("Sale", min_value=0)
        if st.form_submit_button("Save"):
            p = 0 if cat == "Home Expense" else (s_val - c_val)
            nr = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": c_val, "فروخت": s_val, "منافع": p, "اسٹیٹس": stat}
            df = pd.concat([df, pd.DataFrame([nr])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Saved!"); st.rerun()
