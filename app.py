import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی ریڈ ڈیزائن (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    
    /* ڈیش بورڈ کے بڑے سرخ ڈبے */
    .full-red-box {
        background: #D32F2F; color: white !important;
        padding: 25px; border-radius: 25px; text-align: center;
        border: 2px solid #ffffff; box-shadow: 0px 10px 20px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .box-value { font-size: 50px; font-weight: 900; }
    
    /* مینیو کے لمبے بٹن */
    div.stButton > button {
        height: 150px; width: 100%; border-radius: 25px;
        font-size: 24px; font-weight: bold; color: white;
        background: #d32f2f; border: none;
        box-shadow: 0px 8px 15px rgba(211, 47, 47, 0.3);
    }
    
    /* ٹیبل ڈیزائن */
    .stDataFrame { background: white; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو ڈسپلے کرنا (صرف لوگو نظر آئے گا)
col_left, col_mid, col_right = st.columns([1, 1, 1])
with col_mid:
    image_name = "logo.png" 
    if os.path.exists(image_name):
        st.image(image_name, use_container_width=True)
    else:
        st.error("⚠️ لوگو فائل نہیں ملی! نام چیک کریں")

st.write("---") # لوگو کے نیچے ایک باریک لائن

# 4. ڈیٹا مینجمنٹ
DATA_FILE = "ali_pro_data_v9.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()
if 'page' not in st.session_state: st.session_state.page = "home"
def go_to(p): st.session_state.page = p

# 5. ڈیش بورڈ کے سرخ کارڈز
st.write("## ")
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else df

cash_p = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
home_e = t_df[t_df['کیٹیگری'] == "Home Expense"]['فروخت'].sum()
udhaar = t_df[t_df['اسٹیٹس'] == "ادھار"]['فروخت'].sum()

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='full-red-box'><p>نقد پرافٹ</p><div class='box-value'>{cash_p}</div></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='full-red-box'><p>گھر خرچ</p><div class='box-value'>{home_e}</div></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='full-red-box'><p>ٹوٹل ادھار</p><div class='box-value'>{udhaar}</div></div>", unsafe_allow_html=True)

# 6. مین مینیو بٹن
st.write("## ")
b1, b2, b3, b4 = st.columns(4)
with b1: 
    if st.button("➕\nNew Entry"): go_to("new")
with b2: 
    if st.button("📓\nCredit List"): go_to("credit")
with b3: 
    if st.button("📅\nHistory"): go_to("history")
with b4: 
    if st.button("🏠\nHome"): go_to("home")

st.divider()

# 7. پیجز کی تفصیل
if st.session_state.page == "home":
    st.subheader("📋 آج کی کارکردگی")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نئی انٹری")
    with st.form("vip_form"):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        cost = st.number_input("لاگت (Cost)", min_value=0)
        sale = st.number_input("فروخت (Sale)", min_value=0)
        if st.form_submit_button("محفوظ کریں"):
            prof = 0 if cat == "Home Expense" else (sale - cost)
            new_r = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": prof, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([new_r])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("ریکارڈ محفوظ!")
            st.rerun()

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار کی لسٹ")
    c_list = df[df['اسٹیٹس'] == "ادھار"]
    st.table(c_list[["تاریخ", "تفصیل", "فروخت"]]) if not c_list.empty else st.success("کوئی ادھار نہیں!")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ہسٹری")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
