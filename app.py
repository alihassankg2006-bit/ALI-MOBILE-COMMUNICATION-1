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
    
    /* میٹرک ڈبوں کا ڈیزائن (پہلے 4 ڈبے) */
    .big-tile {
        height: 140px; 
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: white !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.2);
        margin-bottom: 15px;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .big-tile:hover {
        transform: translateY(-5px);
        box-shadow: 0px 12px 20px rgba(0,0,0,0.25);
    }
    .tile-name { font-size: 13px; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
    .tile-data { font-size: 34px; font-weight: 900; }

    /* مینو بٹنوں کا ڈیزائن (نیچے والے 4 ڈبے) */
    .menu-tile {
        height: 140px; 
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: white !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.2);
        margin-bottom: 15px;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
        font-size: 18px;
        font-weight: 800;
        white-space: pre-wrap;
        line-height: 1.4;
        padding: 20px;
    }
    .menu-tile:hover {
        transform: translateY(-5px);
        box-shadow: 0px 12px 20px rgba(0,0,0,0.25);
    }

    /* 8 گہرے اور مستقل رنگ (Deep Solid Colors) */
    .bg-green { background: linear-gradient(135deg, #1b5e20, #2e7d32); } /* پرافٹ */
    .bg-blue { background: linear-gradient(135deg, #0d47a1, #1e88e5); }  /* ریپیرنگ */
    .bg-red { background: linear-gradient(135deg, #b71c1c, #d32f2f); }   /* خرچہ */
    .bg-orange { background: linear-gradient(135deg, #e65100, #ff9800); } /* بینکنگ */
    .bg-purple { background: linear-gradient(135deg, #4a148c, #6a1b9a); } /* انٹری - جامنی */
    .bg-teal { background: linear-gradient(135deg, #006064, #00838f); } /* کریڈٹ - ٹیل */
    .bg-pink { background: linear-gradient(135deg, #c2185b, #ad1457); } /* ہسٹری - گلابی */
    .bg-slate { background: linear-gradient(135deg, #263238, #37474f); } /* ہوم - سلیٹی */

    /* تمام بٹنوں کو ڈبوں کی شکل میں بنانے کے لیے */
    div.stButton > button {
        height: 140px !important;
        width: 100% !important;
        border-radius: 20px !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        color: white !important;
        border: none !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.2) !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-bottom: 15px !important;
        white-space: pre-wrap !important;
        line-height: 1.4 !important;
        padding: 20px !important;
    }
    div.stButton > button:hover { 
        transform: translateY(-5px);
        box-shadow: 0px 12px 20px rgba(0,0,0,0.25) !important;
    }
    
    /* مخصوص بٹنوں کے رنگ */
    button[kaya="btn_new"] { background: linear-gradient(135deg, #4a148c, #6a1b9a) !important; }
    button[kaya="btn_credit"] { background: linear-gradient(135deg, #006064, #00838f) !important; }
    button[kaya="btn_hist"] { background: linear-gradient(135deg, #c2185b, #ad1457) !important; }
    button[kaya="btn_home"] { background: linear-gradient(135deg, #263238, #37474f) !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو (صرف اگر فائل موجود ہو)
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

# --- 8 بڑے رنگین ڈبے (2 Columns) ---

# پہلی قطار (حساب)
r1_c1, r1_c2 = st.columns(2)
with r1_c1: 
    # کل نقد پرافٹ - اب بٹن ہے
    if st.button("📊\n\nکل نقد پرافٹ\n\n" + str(cp), key="btn_profit"):
        nav("profit_details")
with r1_c2: 
    # ریپیرنگ پرافٹ - اب بٹن ہے
    if st.button("🔧\n\nریپیرنگ پرافٹ\n\n" + str(rep), key="btn_repair"):
        nav("repair_details")

# دوسری قطار (حساب)
r2_c1, r2_c2 = st.columns(2)
with r2_c1: 
    # گھر کا خرچ - اب بٹن ہے
    if st.button("🏠\n\nگھر کا خرچ\n\n" + str(he), key="btn_expense"):
        nav("expense_details")
with r2_c2: 
    # ایزی پیسہ سیل - اب بٹن ہے
    if st.button("💰\n\nایزی پیسہ سیل\n\n" + str(bank), key="btn_banking"):
        nav("banking_details")

# تیسری قطار (بٹن - اب یہ بھی بڑے اور رنگین ہیں)
r3_c1, r3_c2 = st.columns(2)
with r3_c1: 
    if st.button("➕\n\nنئی انٹری\n(NEW ENTRY)", key="btn_new"): nav("new")
with r3_c2: 
    if st.button("📓\n\nادھار لسٹ\n(CREDIT LIST)", key="btn_credit"): nav("credit")

# چوتھی قطار (بٹن)
r4_c1, r4_c2 = st.columns(2)
with r4_c1: 
    if st.button("📅\n\nمکمل ہسٹری\n(HISTORY)", key="btn_hist"): nav("history")
with r4_c2: 
    if st.button("🏠\n\nہوم پیج\n(HOME)", key="btn_home"): nav("home")

# بٹنوں کو رنگ دینے کے لیے CSS
st.markdown("""
<style>
button[key="btn_profit"] { 
    background: linear-gradient(135deg, #1b5e20, #2e7d32) !important; 
    border: 2px solid #4caf50 !important;
}
button[key="btn_repair"] { 
    background: linear-gradient(135deg, #0d47a1, #1e88e5) !important; 
    border: 2px solid #42a5f5 !important;
}
button[key="btn_expense"] { 
    background: linear-gradient(135deg, #b71c1c, #d32f2f) !important; 
    border: 2px solid #ef5350 !important;
}
button[key="btn_banking"] { 
    background: linear-gradient(135deg, #e65100, #ff9800) !important; 
    border: 2px solid #ffb74d !important;
}
button[key="btn_new"] { 
    background: linear-gradient(135deg, #4a148c, #6a1b9a) !important; 
    border: 2px solid #ab47bc !important;
}
button[key="btn_credit"] { 
    background: linear-gradient(135deg, #006064, #00838f) !important; 
    border: 2px solid #26a69a !important;
}
button[key="btn_hist"] { 
    background: linear-gradient(135deg, #c2185b, #ad1457) !important; 
    border: 2px solid #ec407a !important;
}
button[key="btn_home"] { 
    background: linear-gradient(135deg, #263238, #37474f) !important; 
    border: 2px solid #78909c !important;
}

/* چھوٹے سفید بٹنوں کو چھپائیں جو کہیں بھی ہوں */
div.stButton > button:not([key^="btn_"]) {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

st.divider()

# 6. پیجز کی تفصیل
if st.session_state.page == "home":
    st.subheader("📋 آج کی کارکردگی")
    st.dataframe(t_df, use_container_width=True)

elif st.session_state.page == "new":
    st.subheader("📝 نیا ڈیٹا درج کریں")
    with st.form("ali_form"):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        v1, v2 = st.columns(2)
        cost = v1.number_input("لاگت (Cost)", min_value=0)
        sale = v2.number_input("وصولی (Sale)", min_value=0)
        if st.form_submit_button("سیو کریں"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            new_r = {"تاریخ": datetime.now(), "کیٹیگری": cat, "تفصیل": det, "خریداری": cost, "فروخت": sale, "منافع": p, "اسٹیٹس": pay}
            df = pd.concat([df, pd.DataFrame([new_r])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("محفوظ ہو گیا!"); nav("home")

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار کی لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    if not cl.empty:
        st.table(cl[["تاریخ", "تفصیل", "فروخت"]])
        st.error(f"کل واجب الادا رقم: {cl['فروخت'].sum()}")
    else: st.info("کوئی ادھار نہیں ہے۔")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ریکارڈ")
    st.dataframe(df.sort_values(by="تاریخ", ascending=False), use_container_width=True)

elif st.session_state.page == "profit_details":
    st.subheader("💰 کل نقد پرافٹ کی تفصیلات")
    profit_df = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]
    if not profit_df.empty:
        st.dataframe(profit_df, use_container_width=True)
        st.metric("کل نقد پرافٹ", f"₹{cp}")
    else:
        st.info("آج کے لیے کوئی نقد پرافٹ نہیں ہے۔")

elif st.session_state.page == "repair_details":
    st.subheader("🔧 ریپیرنگ پرافٹ کی تفصیلات")
    repair_df = t_df[t_df['کیٹیگری'] == "Repairing"]
    if not repair_df.empty:
        st.dataframe(repair_df, use_container_width=True)
        st.metric("ریپیرنگ پرافٹ", f"₹{rep}")
    else:
        st.info("آج کے لیے کوئی ریپیرنگ پرافٹ نہیں ہے۔")

elif st.session_state.page == "expense_details":
    st.subheader("🏠 گھر کے خرچ کی تفصیلات")
    expense_df = t_df[t_df['کیٹیگری'] == "Home Expense"]
    if not expense_df.empty:
        st.dataframe(expense_df, use_container_width=True)
        st.metric("کل گھر کا خرچ", f"₹{he}")
    else:
        st.info("آج کے لیے کوئی گھر کا خرچ نہیں ہے۔")

elif st.session_state.page == "banking_details":
    st.subheader("💰 ایزی پیسہ سیلز کی تفصیلات")
    banking_df = t_df[t_df['کیٹیگری'] == "Banking"]
    if not banking_df.empty:
        st.dataframe(banking_df, use_container_width=True)
        st.metric("کل ایزی پیسہ سیلز", f"₹{bank}")
    else:
        st.info("آج کے لیے کوئی ایزی پیسہ سیلز نہیں ہیں۔")
