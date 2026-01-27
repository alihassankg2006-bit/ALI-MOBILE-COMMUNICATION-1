import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ سیٹنگ
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# 2. وی آئی پی بگ ٹائل ڈیزائن (CSS) - UPDATED
st.markdown("""
    <style>
    .block-container { padding: 0.5rem 0.5rem !important; }
    .stApp { background-color: #ffffff; }
    
    /* لوگو کنٹینر */
    .logo-container {
        text-align: center;
        margin-bottom: 25px;
        padding: 10px;
    }
    .shop-title {
        color: #1b5e20;
        font-weight: 800;
        font-size: 28px;
        margin-bottom: 5px;
        letter-spacing: 0.5px;
    }
    .shop-subtitle {
        color: #666;
        font-size: 14px;
        margin-top: 0;
    }
    
    /* میٹرک ڈبوں کا ڈیزائن (تمام 8 ڈبے) */
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
        font-family: 'Segoe UI', system-ui, sans-serif;
        position: relative;
        overflow: hidden;
    }
    .big-tile:hover {
        transform: translateY(-5px);
        box-shadow: 0px 12px 20px rgba(0,0,0,0.25);
    }
    
    /* ڈبے کے اندر کے عناصر */
    .tile-name { 
        font-size: 15px; 
        font-weight: bold; 
        text-transform: uppercase; 
        margin-bottom: 8px;
        opacity: 0.95;
        letter-spacing: 0.5px;
    }
    
    /* پہلے 4 ڈبے کے لیے نمبر ڈسپلے */
    .tile-data { 
        font-size: 36px; 
        font-weight: 900;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    /* نیچے والے 4 ڈبے (بٹنز) کے لیے آئیکن اور ٹیکسٹ */
    .tile-icon { 
        font-size: 32px; 
        font-weight: 900;
        margin-bottom: 10px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    .tile-button-text { 
        font-size: 16px; 
        font-weight: 800;
        line-height: 1.3;
    }

    /* تمام 8 گہرے اور مستقل رنگ (Deep Solid Colors) */
    /* انٹری سب سے اوپر - جامنی رنگ */
    .bg-purple { 
        background: linear-gradient(135deg, #4a148c 0%, #6a1b9a 100%);
        border: 2px solid #ab47bc;
    } /* انٹری - جامنی */
    
    .bg-green { 
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        border: 2px solid #4caf50;
    } /* پرافٹ */
    
    .bg-blue { 
        background: linear-gradient(135deg, #0d47a1 0%, #1e88e5 100%);
        border: 2px solid #42a5f5;
    }  /* ریپیرنگ */
    
    .bg-red { 
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 100%);
        border: 2px solid #ef5350;
    }   /* خرچہ */
    
    .bg-orange { 
        background: linear-gradient(135deg, #e65100 0%, #ff9800 100%);
        border: 2px solid #ffb74d;
    } /* بینکنگ */
    
    /* باقی بٹنز کے رنگ */
    .bg-teal { 
        background: linear-gradient(135deg, #006064 0%, #00838f 100%);
        border: 2px solid #26a69a;
    } /* کریڈٹ - ٹیل */
    
    .bg-pink { 
        background: linear-gradient(135deg, #c2185b 0%, #ad1457 100%);
        border: 2px solid #ec407a;
    } /* ہسٹری - گلابی */
    
    .bg-slate { 
        background: linear-gradient(135deg, #263238 0%, #37474f 100%);
        border: 2px solid #78909c;
    } /* ہوم - سلیٹی */

    /* ریسپانسیو ڈیزائن */
    @media (max-width: 768px) {
        .shop-title {
            font-size: 22px;
        }
        .big-tile {
            height: 120px;
            border-radius: 15px;
        }
        .tile-name {
            font-size: 13px;
        }
        .tile-data {
            font-size: 30px;
        }
        .tile-icon {
            font-size: 28px;
        }
        .tile-button-text {
            font-size: 14px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو سیکشن
st.markdown('<div class="logo-container">', unsafe_allow_html=True)

# لوگو کی تصویر دکھائیں اگر موجود ہو
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align: center;">
            <h2 class="shop-title">ALI MOBILES & COMMUNICATION</h2>
            <p class="shop-subtitle">Premium Shop Management System</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 4. ڈیٹا ہینڈلنگ
DATA_FILE = "ali_shop_v20_final.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['تاریخ'] = pd.to_datetime(df['تاریخ'], errors='coerce')
        return df
    return pd.DataFrame(columns=["تاریخ", "کیٹیگری", "تفصیل", "خریداری", "فروخت", "منافع", "اسٹیٹس"])

df = load_data()
if 'page' not in st.session_state: 
    st.session_state.page = "home"

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

# --- 8 بڑے رنگین ڈبے (4 قطاریں، ہر قطار میں 2 ڈبے) ---

# پہلی قطار: انٹری اور پرافٹ
r1_c1, r1_c2 = st.columns(2)

with r1_c1: 
    # انٹری باکس - اب یہ بٹن ہے
    if st.button("➕\n\nنئی انٹری\n(NEW ENTRY)", key="btn_new"):
        nav("new")
    # CSS کے ذریعے بٹن کو باکس کی شکل دینا
    st.markdown("""
    <style>
    button[key="btn_new"] {
        background: linear-gradient(135deg, #4a148c 0%, #6a1b9a 100%) !important;
        color: white !important;
        height: 140px !important;
        width: 100% !important;
        border-radius: 20px !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        border: 2px solid #ab47bc !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.2) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        margin-bottom: 15px !important;
        white-space: pre-wrap !important;
        line-height: 1.4 !important;
        padding: 20px !important;
    }
    button[key="btn_new"]:hover {
        transform: translateY(-5px);
        box-shadow: 0px 12px 20px rgba(0,0,0,0.25) !important;
        background: linear-gradient(135deg, #6a1b9a 0%, #8e24aa 100%) !important;
    }
    </style>
    """, unsafe_allow_html=True)

with r1_c2: 
    # کل نقد پرافٹ
    st.markdown(f"""
    <div class='big-tile bg-green'>
        <div class='tile-name'>کل نقد پرافٹ</div>
        <div class='tile-data'>{cp}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("", key="profit_btn"):
        nav("profit_details")

# دوسری قطار: ریپیرنگ اور کریڈٹ
r2_c1, r2_c2 = st.columns(2)

with r2_c1: 
    # ریپیرنگ پرافٹ
    st.markdown(f"""
    <div class='big-tile bg-blue'>
        <div class='tile-name'>ریپیرنگ پرافٹ</div>
        <div class='tile-data'>{rep}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("", key="repair_btn"):
        nav("repair_details")

with r2_c2: 
    # کریڈٹ لسٹ
    if st.button("📓\n\nادھار لسٹ\n(CREDIT LIST)", key="btn_credit"):
        nav("credit")
    st.markdown("""
    <style>
    button[key="btn_credit"] {
        background: linear-gradient(135deg, #006064 0%, #00838f 100%) !important;
        color: white !important;
        height: 140px !important;
        width: 100% !important;
        border-radius: 20px !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        border: 2px solid #26a69a !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.2) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        margin-bottom: 15px !important;
        white-space: pre-wrap !important;
        line-height: 1.4 !important;
        padding: 20px !important;
    }
    button[key="btn_credit"]:hover {
        transform: translateY(-5px);
        box-shadow: 0px 12px 20px rgba(0,0,0,0.25) !important;
        background: linear-gradient(135deg, #00838f 0%, #0097a7 100%) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# تیسری قطار: ایزی پیسہ اور ہسٹری
r3_c1, r3_c2 = st.columns(2)

with r3_c1: 
    # ایزی پیسہ سیل
    st.markdown(f"""
    <div class='big-tile bg-orange'>
        <div class='tile-name'>ایزی پیسہ سیل</div>
        <div class='tile-data'>{bank}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("", key="banking_btn"):
        nav("banking_details")

with r3_c2: 
    # ہسٹری
    if st.button("📅\n\nمکمل ہسٹری\n(HISTORY)", key="btn_hist"):
        nav("history")
    st.markdown("""
    <style>
    button[key="btn_hist"] {
        background: linear-gradient(135deg, #c2185b 0%, #ad1457 100%) !important;
        color: white !important;
        height: 140px !important;
        width: 100% !important;
        border-radius: 20px !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        border: 2px solid #ec407a !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.2) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        margin-bottom: 15px !important;
        white-space: pre-wrap !important;
        line-height: 1.4 !important;
        padding: 20px !important;
    }
    button[key="btn_hist"]:hover {
        transform: translateY(-5px);
        box-shadow: 0px 12px 20px rgba(0,0,0,0.25) !important;
        background: linear-gradient(135deg, #ad1457 0%, #d81b60 100%) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# چوتھی قطار: گھر کا خرچ اور ہوم
r4_c1, r4_c2 = st.columns(2)

with r4_c1: 
    # گھر کا خرچ
    st.markdown(f"""
    <div class='big-tile bg-red'>
        <div class='tile-name'>گھر کا خرچ</div>
        <div class='tile-data'>{he}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("", key="expense_btn"):
        nav("expense_details")

with r4_c2: 
    # ہوم پیج
    if st.button("🏠\n\nہوم پیج\n(HOME)", key="btn_home"):
        nav("home")
    st.markdown("""
    <style>
    button[key="btn_home"] {
        background: linear-gradient(135deg, #263238 0%, #37474f 100%) !important;
        color: white !important;
        height: 140px !important;
        width: 100% !important;
        border-radius: 20px !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        border: 2px solid #78909c !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.2) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        margin-bottom: 15px !important;
        white-space: pre-wrap !important;
        line-height: 1.4 !important;
        padding: 20px !important;
    }
    button[key="btn_home"]:hover {
        transform: translateY(-5px);
        box-shadow: 0px 12px 20px rgba(0,0,0,0.25) !important;
        background: linear-gradient(135deg, #37474f 0%, #455a64 100%) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# چھوٹے سفید بٹنوں کو چھپانے کے لیے CSS
st.markdown("""
<style>
/* صرف چھوٹے سفید بٹنوں کو چھپائیں جو ڈیٹا والے باکس کے نیچے ہیں */
div[data-testid="column"] button[kind="secondary"],
div[data-testid="column"] button:not([key^="btn_"]) {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    width: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    opacity: 0 !important;
    position: absolute !important;
    left: -9999px !important;
}

/* بڑے رنگین بٹنز (btn_ والے) دکھائیں */
button[key^="btn_"] {
    display: flex !important;
    visibility: visible !important;
}

/* بڑے ڈیٹا والے باکس کے نیچے چھوٹے بٹن چھپائیں */
div[data-testid="column"] div:has(+ button:not([key^="btn_"])) + button:not([key^="btn_"]) {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

st.divider()

# 6. پیجز کی تفصیل - اب سب کام کریں گے!
if st.session_state.page == "home":
    st.subheader("📋 آج کی کارکردگی")
    if not t_df.empty:
        st.dataframe(t_df, use_container_width=True, 
                    column_config={
                        "تاریخ": st.column_config.DatetimeColumn(format="DD-MM-YYYY HH:mm"),
                        "منافع": st.column_config.NumberColumn(format="₹%d")
                    })
    else:
        st.info("آج کے لیے کوئی ڈیٹا موجود نہیں ہے۔")

elif st.session_state.page == "new":
    st.subheader("📝 نیا ڈیٹا درج کریں")
    with st.form("ali_form", clear_on_submit=True):
        cat = st.selectbox("کیٹیگری", ["Accessories", "Repairing", "Banking", "Home Expense"])
        det = st.text_input("تفصیل")
        pay = st.radio("ادائیگی", ["نقد", "ادھار"], horizontal=True) if cat != "Home Expense" else "نقد"
        v1, v2 = st.columns(2)
        cost = v1.number_input("لاگت (Cost)", min_value=0)
        sale = v2.number_input("وصولی (Sale)", min_value=0)
        
        if st.form_submit_button("💾 سیو کریں"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            new_r = {
                "تاریخ": datetime.now(), 
                "کیٹیگری": cat, 
                "تفصیل": det, 
                "خریداری": cost, 
                "فروخت": sale, 
                "منافع": p, 
                "اسٹیٹس": pay
            }
            df = pd.concat([df, pd.DataFrame([new_r])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ ڈیٹا محفوظ ہو گیا!")
            st.balloons()
            nav("home")

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار کی لسٹ")
    cl = df[df['اسٹیٹس'] == "ادھار"]
    if not cl.empty:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.dataframe(cl[["تاریخ", "کیٹیگری", "تفصیل", "فروخت"]], 
                        use_container_width=True)
        with col2:
            st.metric("کل ادھار", f"₹{cl['فروخت'].sum()}")
    else: 
        st.success("🎉 کوئی ادھار نہیں ہے!")

elif st.session_state.page == "history":
    st.subheader("📅 مکمل ریکارڈ")
    
    # فلٹرز
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("شروع کی تاریخ", datetime.now().date())
    with col2:
        end_date = st.date_input("اختتام کی تاریخ", datetime.now().date())
    
    # فلٹرڈ ڈیٹا
    filtered_df = df[
        (df['تاریخ'].dt.date >= start_date) & 
        (df['تاریخ'].dt.date <= end_date)
    ]
    
    if not filtered_df.empty:
        st.metric("کل انٹریز", len(filtered_df))
        st.dataframe(
            filtered_df.sort_values(by="تاریخ", ascending=False),
            use_container_width=True,
            column_config={
                "تاریخ": st.column_config.DatetimeColumn(format="DD-MM-YYYY"),
                "منافع": st.column_config.NumberColumn(format="₹%d")
            }
        )
    else:
        st.info("منتخب تاریخوں کے لیے کوئی ڈیٹا موجود نہیں ہے۔")

# اضافی پیجز (تفصیلات)
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

# فوٹر
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666; font-size: 12px;'>"
    "© 2024 Ali Mobiles & Communication | Premium Shop Management System"
    "</p>",
    unsafe_allow_html=True
        )
