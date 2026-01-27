import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی کومپیکٹ ڈیزائن (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .block-container { padding: 0.5rem 1rem !important; }
    
    /* ٹائل ڈیزائن */
    .half-card {
        width: 100%; height: 110px; border-radius: 12px;
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); color: white;
        margin-bottom: 5px; border: 1px solid rgba(255,255,255,0.2);
    }
    .card-title { font-size: 11px; font-weight: bold; text-transform: uppercase; opacity: 0.9; }
    .card-value { font-size: 26px; font-weight: 900; }
    
    /* گہرے گریڈینٹ کلرز */
    .c-blue { background: linear-gradient(135deg, #0d47a1, #1976d2); }
    .c-green { background: linear-gradient(135deg, #1b5e20, #388e3c); }
    .c-orange { background: linear-gradient(135deg, #e65100, #f57c00); }
    .c-purple { background: linear-gradient(135deg, #4a148c, #7b1fa2); }
    .c-teal { background: linear-gradient(135deg, #006064, #0097a7); }
    .c-red { background: linear-gradient(135deg, #b71c1c, #d32f2f); }

    /* بٹن سیٹنگ */
    .stButton > button {
        width: 100%; border-radius: 8px; font-weight: bold;
        height: 35px; background-color: #f1f3f4; color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ڈیٹا لوڈنگ (Safe Mode)
DATA_FILE = "ali_shop_pro_v16.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            # تاریخ کو صاف کرنا (ایرر سے بچنے کے لیے)
            df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
            df = df.dropna(subset=['تاریخ'])
            return df
        except:
            return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

# سٹیٹ مینیجمنٹ
if 'page' not in st.session_state: st.session_state.page = "home"
def nav(p):
    st.session_state.page = p
    # ورژن کے لحاظ سے ری رن
    if hasattr(st, "rerun"): st.rerun()
    else: st.experimental_rerun()

df = load_data()

# 4. لوگو اور ٹائٹل
st.markdown("<h3 style='text-align:center; color:#1b5e20; margin-bottom:0;'>ALI MOBILES & COMMUNICATION</h3>", unsafe_allow_html=True)
st.write("---")

# 5. حساب کتاب
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else pd.DataFrame()

p_total = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
r_total = t_df[t_df['کیٹیگری'] == "Repairing"]['منافع'].sum()
b_total = t_df[t_df['کیٹیگری'] == "Banking"]['فروخت'].sum()
u_total = df[df['اسٹیٹس'] == "ادھار"]['فروخت'].sum()
h_total = len(df)
e_total = t_df[t_df['کیٹیگری'] == "Home Expense"]['فروخت'].sum()

# 6. ڈیش بورڈ (2 Columns - Half Half Layout)
col1, col2 = st.columns(2)

with col1:
    st.markdown(f'<div class="half-card c-blue"><div class="card-title">نقد پرافٹ</div><div class="card-value">{p_total}</div></div>', unsafe_allow_html=True)
    if st.button("تفصیل دیکھیں 📈", key="k1"): nav("home")

with col2:
    st.markdown(f'<div class="half-card c-green"><div class="card-title">ریپیرنگ</div><div class="card-value">{r_total}</div></div>', unsafe_allow_html=True)
    if st.button("ریکارڈ کھولیں 🔧", key="k2"): nav("history")

col3, col4 = st.columns(2)
with col3:
    st.markdown(f'<div class="half-card c-orange"><div class="card-title">نئی انٹری</div><div class="card-value">➕</div></div>', unsafe_allow_html=True)
    if st.button("انٹری کریں 📝", key="k3"): nav("new")

with col4:
    st.markdown(f'<div class="half-card c-purple"><div class="card-title">کل ادھار</div><div class="card-value">{u_total}</div></div>', unsafe_allow_html=True)
    if st.button("ادھار لسٹ 📓", key="k4"): nav("credit")

col5, col6 = st.columns(2)
with col5:
    st.markdown(f'<div class="half-card c-teal"><div class="card-title">ٹوٹل ہسٹری</div><div class="card-value">{h_total}</div></div>', unsafe_allow_html=True)
    if st.button("ہسٹری دیکھیں 📅", key="k5"): nav("history")

with col6:
    st.markdown(f'<div class="half-card c-red"><div class="card-title">بینکنگ سیل</div><div class="card-value">{b_total}</div></div>', unsafe_allow_html=True)
    if st.button("بینکنگ ڈیٹا 💰", key="k6"): nav("banking")

st.divider()

# 7. پیجز کی تفصیل
if st.session_state.page == "home":
    st.subheader("📊 آج کی کارکردگی")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نئی انٹری")
    with st.form("ali_form", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        c_val = st.number_input("لاگت (Cost)", min_value=0)
        s_val = st.number_input("فروخت (Sale)", min_value=0)
        if st.form_submit_button("محفوظ کریں"):
            prof = 0 if cat == "Home Expense" else (s_val - c_val)
            nr = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": c_val, "فروخت": s_val, "منافع": prof, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([nr])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("ریکارڈ سیو ہو گیا!")
            nav("home")

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار لسٹ")
    st.dataframe(df[df['اسٹیٹس'] == "ادھار"], use_container_width=True)

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ہسٹری")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)

elif st.session_state.page == "banking":
    st.subheader("💰 بینکنگ تفصیل")
    st.dataframe(df[df['کیٹیگری'] == "Banking"], use_container_width=True)
    
