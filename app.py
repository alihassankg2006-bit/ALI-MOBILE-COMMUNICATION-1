import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. کسٹم CSS (رنگین بٹن اور چھوٹے باکسز)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    
    /* ڈیش بورڈ کے چھوٹے ڈبے */
    .metric-box {
        color: white !important;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 10px;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
    }
    .box-title { font-size: 14px; font-weight: bold; opacity: 0.9; text-transform: uppercase; }
    .box-val { font-size: 28px; font-weight: 900; }

    /* مینو بٹنوں کے انفرادی گہرے رنگ */
    div.stButton > button {
        height: 100px;
        width: 100%;
        border-radius: 20px;
        font-size: 22px;
        font-weight: bold;
        color: white !important;
        border: none;
        box-shadow: 0px 6px 12px rgba(0,0,0,0.2);
        margin-bottom: 15px;
    }
    
    /* ہر بٹن کا الگ رنگ */
    /* New Entry - Deep Blue */
    div[data-testid="column"]:nth-of-type(1) > div > div > div > button { background: #0d47a1 !important; }
    /* Credit List - Deep Purple */
    div[data-testid="column"]:nth-of-type(2) > div > div > div > button { background: #4a148c !important; }
    /* History - Deep Green */
    div[data-testid="column"]:nth-of-type(3) > div > div > div > button { background: #1b5e20 !important; }
    /* Home - Deep Slate */
    div[data-testid="column"]:nth-of-type(4) > div > div > div > button { background: #263238 !important; }

    /* فارم ڈیزائن */
    .stForm { background: #f1f3f4; padding: 20px; border-radius: 20px; border: 2px solid #d32f2f; }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو
col_l, col_m, col_r = st.columns([1, 1, 1])
with col_m:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
st.write("---")

# 4. ڈیٹا مینجمنٹ
DATA_FILE = "ali_shop_pro_v10.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()
if 'page' not in st.session_state: st.session_state.page = "home"
def nav(p): st.session_state.page = p

# 5. چھوٹے ڈیش بورڈ باکسز (2x2 Grid)
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else df

cp = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
he = t_df[t_df['کیٹیگری'] == "Home Expense"]['فروخت'].sum()
ut = t_df[t_df['اسٹیٹس'] == "ادھار"]['فروخت'].sum()
sv = cp - he

# پہلی لائن
r1_c1, r1_c2 = st.columns(2)
r1_c1.markdown(f"<div class='metric-box' style='background:#1b5e20;'><div class='box-title'>نقد پرافٹ</div><div class='box-val'>{cp}</div></div>", unsafe_allow_html=True)
r1_c2.markdown(f"<div class='metric-box' style='background:#b71c1c;'><div class='box-title'>گھر کا خرچ</div><div class='box-val'>{he}</div></div>", unsafe_allow_html=True)

# دوسری لائن
r2_c1, r2_c2 = st.columns(2)
r2_c1.markdown(f"<div class='metric-box' style='background:#e65100;'><div class='box-title'>آج کا ادھار</div><div class='box-val'>{ut}</div></div>", unsafe_allow_html=True)
r2_c2.markdown(f"<div class='metric-box' style='background:#0d47a1;'><div class='box-title'>خالص بچت</div><div class='box-val'>{sv}</div></div>", unsafe_allow_html=True)

st.write("## ")

# 6. رنگین مینو بٹن (لمبے اور گہرے رنگ)
m1, m2, m3, m4 = st.columns(4)
with m1: 
    if st.button("➕\nEntry", key="btn_new"): nav("new")
with m2: 
    if st.button("📓\nCredit", key="btn_credit"): nav("credit")
with m3: 
    if st.button("📅\nHistory", key="btn_hist"): nav("history")
with m4: 
    if st.button("🏠\nHome", key="btn_home"): nav("home")

st.divider()

# 7. پیجز کی تفصیل
if st.session_state.page == "home":
    st.subheader("📋 آج کا ریکارڈ")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نئی انٹری شامل کریں")
    with st.form("entry_form"):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل")
        stat = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        cx, sx = st.columns(2)
        c_val = cx.number_input("لاگت (Cost)", min_value=0)
        s_val = sx.number_input("وصولی (Sale)", min_value=0)
        if st.form_submit_button("Save Record 💾"):
            p = 0 if cat == "Home Expense" else (s_val - c_val)
            nr = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": c_val, "فروخت": s_val, "منافع": p, "اسٹیٹس": stat}
            df = pd.concat([df, pd.DataFrame([nr])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("ریکارڈ محفوظ ہو گیا!")
            st.rerun()

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار لینے والوں کی لسٹ")
    c_list = df[df['اسٹیٹس'] == "ادھار"]
    if not c_list.empty:
        # ادھار ختم کرنے کا فیچر (اختیاری)
        st.table(c_list[["تاریخ", "تفصیل", "فروخت"]])
        st.error(f"ٹوٹل ادھار: {c_list['فروخت'].sum()} PKR")
    else: st.success("کوئی ادھار باقی نہیں ہے!")

elif st.session_state.page == "history":
    st.subheader("📅 دکان کا مکمل ڈیٹا")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
    
