import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی سپلٹ ڈیزائن (CSS) - UPDATED
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 1rem !important; }
    .stApp { background-color: #ffffff; }
    
    /* سپلٹ کارڈ ڈیزائن - UPDATED */
    .split-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: white !important;
        border-radius: 12px;
        margin-bottom: 10px;
        height: 90px;
        overflow: hidden;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    .card-content {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }
    
    .m-label { font-size: 14px; font-weight: bold; opacity: 0.9; text-transform: uppercase; }
    .m-val { font-size: 28px; font-weight: 900; margin-top: 5px; }

    /* بٹنوں کا ڈیزائن - UPDATED */
    .button-card {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 90px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: bold;
        color: white !important;
        margin-bottom: 10px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        cursor: pointer;
    }
    .button-card:hover { opacity: 0.9; }
    
    /* مخصوص رنگ */
    .row-green { background: #1b5e20; } /* Profit */
    .row-green-light { background: #2e7d32; } /* Entry Button */
    .row-purple { background: #4a148c; } /* Repairing */
    .row-purple-light { background: #6a1b9a; } /* Credit Button */
    .row-orange { background: #e65100; } /* Banking */
    .row-orange-light { background: #f57c00; } /* History Button */
    .row-red { background: #b71c1c; }    /* Expense */
    .row-red-light { background: #d32f2f; } /* Home Button */
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو
cl1, cl2, cl3 = st.columns([1, 0.5, 1])
with cl2:
    if os.path.exists("logo.png"): 
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("""
        <div style='text-align:center; background:#f5f5f5; padding:10px; border-radius:10px;'>
            <span style='color:#b71c1c; font-weight:bold; font-size:16px;'>ALI MOBILES</span>
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

# 6. 4 قطاریں برابر چوڑائی میں - UPDATED LAYOUT
# ہر قطار میں دو برابر کالم

# Row 1: کل نقد پرافٹ | ENTRY
row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    st.markdown(f"""
    <div class='split-card row-green'>
        <div class='card-content'>
            <div class='m-label'>کل نقد پرافٹ</div>
            <div class='m-val'>{cp}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with row1_col2:
    if st.button("➕ ENTRY", key="e"):
        nav("new")
    # CSS کے ذریعے بٹن کو کارڈ کی شکل دینا
    st.markdown("""
    <style>
    div[data-testid="column"]:nth-of-type(2) button {
        background: #2e7d32 !important;
        color: white !important;
        height: 90px !important;
        width: 100% !important;
        border-radius: 12px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2) !important;
        margin-bottom: 10px !important;
    }
    div[data-testid="column"]:nth-of-type(2) button:hover {
        background: #1b5e20 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Row 2: ریپیرنگ پرافٹ | CREDIT
row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    st.markdown(f"""
    <div class='split-card row-purple'>
        <div class='card-content'>
            <div class='m-label'>ریپیرنگ پرافٹ</div>
            <div class='m-val'>{rep}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with row2_col2:
    if st.button("📓 CREDIT", key="c"):
        nav("credit")
    st.markdown("""
    <style>
    div[data-testid="column"]:nth-of-type(4) button {
        background: #6a1b9a !important;
        color: white !important;
        height: 90px !important;
        width: 100% !important;
        border-radius: 12px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2) !important;
        margin-bottom: 10px !important;
    }
    div[data-testid="column"]:nth-of-type(4) button:hover {
        background: #4a148c !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Row 3: ایزی پیسہ سیل | HISTORY
row3_col1, row3_col2 = st.columns(2)
with row3_col1:
    st.markdown(f"""
    <div class='split-card row-orange'>
        <div class='card-content'>
            <div class='m-label'>ایزی پیسہ سیل</div>
            <div class='m-val'>{bank}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with row3_col2:
    if st.button("📅 HISTORY", key="h"):
        nav("history")
    st.markdown("""
    <style>
    div[data-testid="column"]:nth-of-type(6) button {
        background: #f57c00 !important;
        color: white !important;
        height: 90px !important;
        width: 100% !important;
        border-radius: 12px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2) !important;
        margin-bottom: 10px !important;
    }
    div[data-testid="column"]:nth-of-type(6) button:hover {
        background: #e65100 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Row 4: گھر کا خرچ | HOME
row4_col1, row4_col2 = st.columns(2)
with row4_col1:
    st.markdown(f"""
    <div class='split-card row-red'>
        <div class='card-content'>
            <div class='m-label'>گھر کا خرچ</div>
            <div class='m-val'>{he}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with row4_col2:
    if st.button("🏠 HOME", key="hm"):
        nav("home")
    st.markdown("""
    <style>
    div[data-testid="column"]:nth-of-type(8) button {
        background: #d32f2f !important;
        color: white !important;
        height: 90px !important;
        width: 100% !important;
        border-radius: 12px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2) !important;
        margin-bottom: 10px !important;
    }
    div[data-testid="column"]:nth-of-type(8) button:hover {
        background: #b71c1c !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.divider()

# 7. پیجز کا ڈیٹا (یہ وہی رہے گا)
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
