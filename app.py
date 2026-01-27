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
        transition: transform 0.2s, box-shadow 0.2s;
        font-family: 'Segoe UI', system-ui, sans-serif;
        position: relative;
        overflow: hidden;
    }
    .big-tile:hover {
        transform: translateY(-5px);
        box-shadow: 0px 12px 20px rgba(0,0,0,0.25);
    }
    
    /* بٹن کے اندر کا ٹیکسٹ سٹائل */
    .big-tile button {
        background: transparent !important;
        border: none !important;
        width: 100% !important;
        height: 100% !important;
        color: white !important;
        font-family: inherit !important;
        padding: 0 !important;
        margin: 0 !important;
        cursor: pointer !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .big-tile button:hover {
        background: transparent !important;
    }
    .big-tile button:focus {
        outline: none !important;
        box-shadow: none !important;
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
    .bg-purple { 
        background: linear-gradient(135deg, #4a148c 0%, #6a1b9a 100%);
        border: 2px solid #ab47bc;
    }
    
    .bg-green { 
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        border: 2px solid #4caf50;
    }
    
    .bg-blue { 
        background: linear-gradient(135deg, #0d47a1 0%, #1e88e5 100%);
        border: 2px solid #42a5f5;
    }
    
    .bg-red { 
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 100%);
        border: 2px solid #ef5350;
    }
    
    .bg-orange { 
        background: linear-gradient(135deg, #e65100 0%, #ff9800 100%);
        border: 2px solid #ffb74d;
    }
    
    .bg-teal { 
        background: linear-gradient(135deg, #006064 0%, #00838f 100%);
        border: 2px solid #26a69a;
    }
    
    .bg-pink { 
        background: linear-gradient(135deg, #c2185b 0%, #ad1457 100%);
        border: 2px solid #ec407a;
    }
    
    .bg-slate { 
        background: linear-gradient(135deg, #263238 0%, #37474f 100%);
        border: 2px solid #78909c;
    }

    /* چھوٹے بٹنوں کو چھپانے کے لیے */
    .hidden-button {
        display: none !important;
    }
    
    /* بٹن کے اندر کے ٹیکسٹ کے لیے */
    .button-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
    }

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

# 5. سیشن اسٹیٹ میں صفحہ کا تعین
if 'page' not in st.session_state:
    st.session_state.page = "home"

# 6. حساب کتاب
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else df
cp = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
rep = t_df[t_df['کیٹیگری']=="Repairing"]['منافع'].sum()
he = t_df[t_df['کیٹیگری']=="Home Expense"]['فروخت'].sum()
bank = t_df[t_df['کیٹیگری']=="Banking"]['فروخت'].sum()

# 7. بڑے بٹنز بنانے کا فنکشن
def create_big_button(column, color_class, icon_or_data, text, page_key, is_data=False):
    with column:
        if is_data:
            # ڈیٹا والے بٹن (پرافٹ، خرچہ وغیرہ)
            button_html = f"""
            <div class='big-tile {color_class}'>
                <div class='button-content'>
                    <div class='tile-name'>{text}</div>
                    <div class='tile-data'>{icon_or_data}</div>
                </div>
            </div>
            """
        else:
            # آئیکن والے بٹن (انٹری، ہسٹری وغیرہ)
            button_html = f"""
            <div class='big-tile {color_class}'>
                <div class='button-content'>
                    <div class='tile-icon'>{icon_or_data}</div>
                    <div class='tile-button-text'>{text}</div>
                </div>
            </div>
            """
        
        # HTML دکھائیں
        st.markdown(button_html, unsafe_allow_html=True)
        
        # اس کے نیچے خفیہ بٹن
        if st.button("", key=f"btn_{page_key}", help=text):
            st.session_state.page = page_key
            st.rerun()

# 8. بڑے بٹنز کی قطاریں

# پہلی قطار: انٹری اور پرافٹ
r1_c1, r1_c2 = st.columns(2)
create_big_button(r1_c1, "bg-purple", "➕", "نئی انٹری<br><small>(NEW ENTRY)</small>", "new")
create_big_button(r1_c2, "bg-green", cp, "کل نقد پرافٹ", "profit_details", is_data=True)

# دوسری قطار: ریپیرنگ اور کریڈٹ
r2_c1, r2_c2 = st.columns(2)
create_big_button(r2_c1, "bg-blue", rep, "ریپیرنگ پرافٹ", "repair_details", is_data=True)
create_big_button(r2_c2, "bg-teal", "📓", "ادھار لسٹ<br><small>(CREDIT LIST)</small>", "credit")

# تیسری قطار: ایزی پیسہ اور ہسٹری
r3_c1, r3_c2 = st.columns(2)
create_big_button(r3_c1, "bg-orange", bank, "ایزی پیسہ سیل", "banking_details", is_data=True)
create_big_button(r3_c2, "bg-pink", "📅", "مکمل ہسٹری<br><small>(HISTORY)</small>", "history")

# چوتھی قطار: گھر کا خرچ اور ہوم
r4_c1, r4_c2 = st.columns(2)
create_big_button(r4_c1, "bg-red", he, "گھر کا خرچ", "expense_details", is_data=True)
create_big_button(r4_c2, "bg-slate", "🏠", "ہوم پیج<br><small>(HOME)</small>", "home")

st.divider()

# 9. پیجز کی تفصیل
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
            st.session_state.page = "home"
            st.rerun()

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

# واپس جانے کا بٹن (سب پیجز پر)
if st.session_state.page != "home":
    if st.button("← واپس ہوم پیج پر جائیں"):
        st.session_state.page = "home"
        st.rerun()

# فوٹر
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666; font-size: 12px;'>"
    "© 2024 Ali Mobiles & Communication | Premium Shop Management System"
    "</p>",
    unsafe_allow_html=True)
