import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی ڈیزائن (CSS) - UPDATED GRID SYSTEM
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 1rem !important; }
    .stApp { background-color: #f5f5f5; }
    
    /* برابر باکس کا ڈیزائن */
    .equal-box {
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 15px;
        height: 110px;
        margin-bottom: 15px;
        box-shadow: 0px 6px 15px rgba(0,0,0,0.15);
        text-align: center;
        color: white;
        font-weight: bold;
        border: none;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .equal-box:hover {
        transform: translateY(-3px);
        box-shadow: 0px 8px 20px rgba(0,0,0,0.2);
    }
    
    /* پرافٹ باکس کے اندر کا ڈیزائن */
    .box-content {
        padding: 15px;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .box-label { 
        font-size: 16px; 
        font-weight: 700; 
        text-transform: uppercase; 
        margin-bottom: 5px;
        opacity: 0.9;
    }
    .box-value { 
        font-size: 32px; 
        font-weight: 900; 
        line-height: 1;
    }
    
    /* بٹن والے باکس کے لیے */
    .button-box {
        font-size: 22px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 5px;
    }
    .button-icon { font-size: 28px; }
    
    /* مخصوص رنگ */
    .profit-box { 
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        border: 3px solid #4caf50;
    }
    .entry-button { 
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 100%);
        border: 3px solid #42a5f5;
    }
    .repair-box { 
        background: linear-gradient(135deg, #4a148c 0%, #6a1b9a 100%);
        border: 3px solid #ab47bc;
    }
    .credit-button { 
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 100%);
        border: 3px solid #ef5350;
    }
    .banking-box { 
        background: linear-gradient(135deg, #e65100 0%, #f57c00 100%);
        border: 3px solid #ff9800;
    }
    .history-button { 
        background: linear-gradient(135deg, #004d40 0%, #00796b 100%);
        border: 3px solid #26a69a;
    }
    .expense-box { 
        background: linear-gradient(135deg, #880e4f 0%, #ad1457 100%);
        border: 3px solid #ec407a;
    }
    .home-button { 
        background: linear-gradient(135deg, #37474f 0%, #546e7a 100%);
        border: 3px solid #78909c;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو
cl1, cl2, cl3 = st.columns([1, 0.5, 1])
with cl2:
    if os.path.exists("logo.png"): 
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("""
        <div style='text-align:center; background:#f5f5f5; padding:15px; border-radius:10px; border: 2px solid #d32f2f;'>
            <span style='color:#d32f2f; font-weight:bold; font-size:18px;'>ALI MOBILES & COMMUNICATION</span>
        </div>
        """, unsafe_allow_html=True)

# 4. ڈیٹا لوڈنگ
DATA_FILE = "ali_shop_split_v13.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()
if 'page' not in st.session_state: st.session_state.page = "home"
def nav(p): st.session_state.page = p

# 5. ڈیٹا کیلکولیشن
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else df
cp = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
he = t_df[t_df['کیٹیگری']=="Home Expense"]['فروخت'].sum()
ut = t_df[t_df['اسٹیٹس']=="ادھار"]['فروخت'].sum()
rep = t_df[t_df['کیٹیگری']=="Repairing"]['منافع'].sum()
bank = t_df[t_df['کیٹیگری']=="Banking"]['فروخت'].sum()

# 6. 4 قطاریں - ہر قطار میں 2 برابر باکس
# سبھی باکس ایک ہی سائز کے ہوں گے

# Row 1: کل نقد پرافٹ | ENTRY
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    # پرافٹ باکس
    st.markdown(f"""
    <div class='equal-box profit-box'>
        <div class='box-content'>
            <div class='box-label'>کل نقد پرافٹ</div>
            <div class='box-value'>{cp}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with row1_col2:
    # انٹری بٹن باکس
    if st.button("", key="entry_box"):
        nav("new")
    # CSS کے ذریعے بٹن کو باکس کی شکل دینا
    st.markdown("""
    <style>
    div[data-testid="column"]:nth-of-type(2) button {
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 100%) !important;
        color: white !important;
        height: 110px !important;
        width: 100% !important;
        border-radius: 15px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border: 3px solid #42a5f5 !important;
        box-shadow: 0px 6px 15px rgba(0,0,0,0.15) !important;
        margin-bottom: 15px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 5px !important;
    }
    div[data-testid="column"]:nth-of-type(2) button:hover {
        transform: translateY(-3px);
        box-shadow: 0px 8px 20px rgba(0,0,0,0.2) !important;
    }
    div[data-testid="column"]:nth-of-type(2) button:before {
        content: "➕";
        font-size: 28px;
    }
    div[data-testid="column"]:nth-of-type(2) button:after {
        content: "ENTRY";
        font-size: 22px;
    }
    </style>
    """, unsafe_allow_html=True)

# Row 2: ریپیرنگ پرافٹ | CREDIT
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    # ریپیرنگ پرافٹ باکس
    st.markdown(f"""
    <div class='equal-box repair-box'>
        <div class='box-content'>
            <div class='box-label'>ریپیرنگ پرافٹ</div>
            <div class='box-value'>{rep}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with row2_col2:
    # کریڈٹ بٹن باکس
    if st.button("", key="credit_box"):
        nav("credit")
    st.markdown("""
    <style>
    div[data-testid="column"]:nth-of-type(4) button {
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 100%) !important;
        color: white !important;
        height: 110px !important;
        width: 100% !important;
        border-radius: 15px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border: 3px solid #ef5350 !important;
        box-shadow: 0px 6px 15px rgba(0,0,0,0.15) !important;
        margin-bottom: 15px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 5px !important;
    }
    div[data-testid="column"]:nth-of-type(4) button:hover {
        transform: translateY(-3px);
        box-shadow: 0px 8px 20px rgba(0,0,0,0.2) !important;
    }
    div[data-testid="column"]:nth-of-type(4) button:before {
        content: "📓";
        font-size: 28px;
    }
    div[data-testid="column"]:nth-of-type(4) button:after {
        content: "CREDIT";
        font-size: 22px;
    }
    </style>
    """, unsafe_allow_html=True)

# Row 3: ایزی پیسہ سیل | HISTORY
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    # بینکنگ باکس
    st.markdown(f"""
    <div class='equal-box banking-box'>
        <div class='box-content'>
            <div class='box-label'>ایزی پیسہ سیل</div>
            <div class='box-value'>{bank}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with row3_col2:
    # ہسٹری بٹن باکس
    if st.button("", key="history_box"):
        nav("history")
    st.markdown("""
    <style>
    div[data-testid="column"]:nth-of-type(6) button {
        background: linear-gradient(135deg, #004d40 0%, #00796b 100%) !important;
        color: white !important;
        height: 110px !important;
        width: 100% !important;
        border-radius: 15px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border: 3px solid #26a69a !important;
        box-shadow: 0px 6px 15px rgba(0,0,0,0.15) !important;
        margin-bottom: 15px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 5px !important;
    }
    div[data-testid="column"]:nth-of-type(6) button:hover {
        transform: translateY(-3px);
        box-shadow: 0px 8px 20px rgba(0,0,0,0.2) !important;
    }
    div[data-testid="column"]:nth-of-type(6) button:before {
        content: "📅";
        font-size: 28px;
    }
    div[data-testid="column"]:nth-of-type(6) button:after {
        content: "HISTORY";
        font-size: 22px;
    }
    </style>
    """, unsafe_allow_html=True)

# Row 4: گھر کا خرچ | HOME
row4_col1, row4_col2 = st.columns(2)

with row4_col1:
    # خرچ باکس
    st.markdown(f"""
    <div class='equal-box expense-box'>
        <div class='box-content'>
            <div class='box-label'>گھر کا خرچ</div>
            <div class='box-value'>{he}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with row4_col2:
    # ہوم بٹن باکس
    if st.button("", key="home_box"):
        nav("home")
    st.markdown("""
    <style>
    div[data-testid="column"]:nth-of-type(8) button {
        background: linear-gradient(135deg, #37474f 0%, #546e7a 100%) !important;
        color: white !important;
        height: 110px !important;
        width: 100% !important;
        border-radius: 15px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border: 3px solid #78909c !important;
        box-shadow: 0px 6px 15px rgba(0,0,0,0.15) !important;
        margin-bottom: 15px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 5px !important;
    }
    div[data-testid="column"]:nth-of-type(8) button:hover {
        transform: translateY(-3px);
        box-shadow: 0px 8px 20px rgba(0,0,0,0.2) !important;
    }
    div[data-testid="column"]:nth-of-type(8) button:before {
        content: "🏠";
        font-size: 28px;
    }
    div[data-testid="column"]:nth-of-type(8) button:after {
        content: "HOME";
        font-size: 22px;
    }
    </style>
    """, unsafe_allow_html=True)

st.divider()

# 7. پیجز کا ڈیٹا
if st.session_state.page == "home":
    st.subheader("📋 آج کی سیل")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نئی انٹری")
    with st.form("vip_f"):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        cx, sx = st.columns(2)
        cost = cx.number_input("لاگت", min_value=0)
        sale = sx.number_input("وصولی", min_value=0)
        if st.form_submit_button("محفوظ کریں"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            nr = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": p, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([nr])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("محفوظ ہو گیا!"); st.rerun()

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    if not cl.empty:
        st.table(cl[["تاریخ", "تفصیل", "فروخت"]])
        st.info(f"کل ادھار: {cl['فروخت'].sum()}")
    else:
        st.info("کوئی ادھار نہیں")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ریکارڈ")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)
