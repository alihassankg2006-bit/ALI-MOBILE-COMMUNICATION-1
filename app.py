import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. ایپ کی بنیادی سیٹنگ
st.set_page_config(
    page_title="Ali Mobiles & Communication", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. پروفیشنل ڈیزائن CSS
st.markdown("""
    <style>
    /* بیک گراؤنڈ اور بنیادی سیٹنگ */
    .stApp { background-color: #f8f9fa; }
    .main > div { padding-top: 1rem; }
    
    /* برابر سائز کے باکس */
    .half-card {
        width: 100%;
        height: 140px;
        border-radius: 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        color: white;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    
    /* ہوور ایفیکٹ */
    .half-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* باکس کے اندر کے عناصر */
    .card-title {
        font-size: 16px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
        opacity: 0.95;
    }
    
    .card-value {
        font-size: 38px;
        font-weight: 800;
        line-height: 1;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
        margin-top: 5px;
        color: white !important;
        background: transparent !important;
    }
    
    /* راؤ کا اسٹائل */
    .card-row {
        display: flex;
        gap: 15px;
        margin-bottom: 15px;
    }
    
    /* ہر باکس کا مخصوص رنگ */
    .profit-card {
        background: linear-gradient(145deg, #1e88e5, #0d47a1);
    }
    
    .repair-card {
        background: linear-gradient(145deg, #43a047, #1b5e20);
    }
    
    .entry-card {
        background: linear-gradient(145deg, #ff9800, #e65100);
    }
    
    .credit-card {
        background: linear-gradient(145deg, #9c27b0, #6a1b9a);
    }
    
    .history-card {
        background: linear-gradient(145deg, #00bcd4, #006064);
    }
    
    .easypaisa-card {
        background: linear-gradient(145deg, #f44336, #b71c1c);
    }
    
    /* لوگو سیکشن */
    .logo-container {
        text-align: center;
        padding: 10px 0;
        margin-bottom: 20px;
    }
    
    /* موبائل ریسپانسیو */
    @media (max-width: 768px) {
        .half-card {
            height: 130px;
            padding: 15px;
        }
        .card-title {
            font-size: 14px;
        }
        .card-value {
            font-size: 32px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. لوگو سیکشن
st.markdown("""
<div class="logo-container">
    <h2 style="color: #1b5e20; margin-bottom: 5px; font-weight: 800;">ALI MOBILES & COMMUNICATION</h2>
    <p style="color: #666; font-size: 14px; margin-top: 0;">Premium Shop Management System</p>
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
if 'page' not in st.session_state: 
    st.session_state.page = "home"

def nav(p): 
    st.session_state.page = p

# 5. ڈیٹا کیلکولیشن
today = datetime.now().date()
t_df = df[df['تاریخ'].dt.date == today] if not df.empty else pd.DataFrame()

# حساب کتاب
total_profit = t_df[(t_df['اسٹیٹس']=="نقد") & (t_df['کیٹیگری']!="Home Expense")]['منافع'].sum()
repair_profit = t_df[t_df['کیٹیگری'] == "Repairing"]['منافع'].sum()
easypaisa_sales = t_df[t_df['کیٹیگری'] == "Banking"]['فروخت'].sum()
home_expense = t_df[t_df['کیٹیگری'] == "Home Expense"]['فروخت'].sum()
total_credit = df[df['اسٹیٹس'] == "ادھار"]['فروخت'].sum()
total_history = len(df)

# 6. ڈیش بورڈ لے آؤٹ - 3 قطاریں، ہر قطار میں 2 برابر کے باکس

# پہلی قطار: پرافٹ اور ریپیرنگ
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown(f"""
    <div class="half-card profit-card" onclick="window.dashboardClick('profit')">
        <div class="card-title">کل نقد پرافٹ</div>
        <div class="card-value">{total_profit}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("", key="profit_btn", help="کل نقد پرافٹ"):
        nav("profit_details")

with row1_col2:
    st.markdown(f"""
    <div class="half-card repair-card" onclick="window.dashboardClick('repair')">
        <div class="card-title">ریپیرنگ پرافٹ</div>
        <div class="card-value">{repair_profit}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("", key="repair_btn", help="ریپیرنگ پرافٹ"):
        nav("repair_details")

# دوسری قطار: انٹری اور کریڈٹ
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown(f"""
    <div class="half-card entry-card" onclick="window.dashboardClick('entry')">
        <div class="card-title">نیا انٹری</div>
        <div class="card-value">+</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("", key="entry_btn", help="نیا انٹری شامل کریں"):
        nav("new")

with row2_col2:
    st.markdown(f"""
    <div class="half-card credit-card" onclick="window.dashboardClick('credit')">
        <div class="card-title">کل کریڈٹ</div>
        <div class="card-value">{total_credit}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("", key="credit_btn", help="کریڈٹ کی تفصیلات"):
        nav("credit")

# تیسری قطار: ہسٹری اور ایزی پیسہ
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.markdown(f"""
    <div class="half-card history-card" onclick="window.dashboardClick('history')">
        <div class="card-title">ٹوٹل ہسٹری</div>
        <div class="card-value">{total_history}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("", key="history_btn", help="مکمل ریکارڈ"):
        nav("history")

with row3_col2:
    st.markdown(f"""
    <div class="half-card easypaisa-card" onclick="window.dashboardClick('easypaisa')">
        <div class="card-title">ایزی پیسہ سیل</div>
        <div class="card-value">{easypaisa_sales}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("", key="easypaisa_btn", help="ایزی پیسہ سیلز"):
        nav("easypaisa_details")

# JavaScript for click handling
st.markdown("""
<script>
window.dashboardClick = function(type) {
    // یہاں آپ کلک ہینڈلنگ کا کوڈ شامل کر سکتے ہیں
    console.log('Card clicked:', type);
}
</script>
""", unsafe_allow_html=True)

st.divider()

# 7. پیجز کا ڈیٹا
if st.session_state.page == "home" or st.session_state.page == "profit_details":
    st.subheader("📊 آج کی کارکردگی")
    if not t_df.empty:
        st.dataframe(t_df, use_container_width=True, 
                    column_config={
                        "تاریخ": st.column_config.DatetimeColumn(format="DD-MM-YYYY HH:mm"),
                        "منافع": st.column_config.NumberColumn(format="%d")
                    })
    else:
        st.info("آج کے لیے کوئی ڈیٹا موجود نہیں ہے۔")

elif st.session_state.page == "new":
    st.subheader("📝 نیا ریکارڈ شامل کریں")
    with st.form("new_record_form", clear_on_submit=True):
        category = st.selectbox("کیٹیگری منتخب کریں", 
                              ["Accessories", "Repairing", "Banking", "Home Expense"])
        description = st.text_input("تفصیل درج کریں")
        
        if category != "Home Expense":
            payment_type = st.radio("ادائیگی کی قسم", ["نقد", "ادھار"], horizontal=True)
        else:
            payment_type = "نقد"
            
        col1, col2 = st.columns(2)
        with col1:
            cost = st.number_input("لاگت (Cost)", min_value=0, step=100)
        with col2:
            sale = st.number_input("فروخت (Sale)", min_value=0, step=100)
            
        submitted = st.form_submit_button("💾 ریکارڈ محفوظ کریں")
        
        if submitted:
            if category == "Home Expense":
                profit = 0
            else:
                profit = sale - cost
                
            new_record = {
                "تاریخ": datetime.now(),
                "کیٹیگری": category,
                "تفصیل": description,
                "خریداری": cost,
                "فروخت": sale,
                "منافع": profit,
                "اسٹیٹس": payment_type
            }
            
            df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ ریکارڈ کامیابی سے محفوظ ہو گیا!")
            st.balloons()
            st.rerun()

elif st.session_state.page == "credit":
    st.subheader("📋 کریڈٹ ریکارڈز")
    credit_df = df[df['اسٹیٹس'] == "ادھار"]
    
    if not credit_df.empty:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.dataframe(credit_df[["تاریخ", "کیٹیگری", "تفصیل", "فروخت"]], 
                        use_container_width=True)
        with col2:
            st.metric("کل واجب الادا", f"₹{total_credit}")
            
        # کریڈٹ کلیئر کرنے کا آپشن
        with st.expander("کریڈٹ کلیئر کریں"):
            clear_desc = st.text_input("تفصیل")
            clear_amount = st.number_input("رقم", min_value=0, step=100)
            if st.button("کریڈٹ کلیئر کریں"):
                st.success("کریڈٹ کلیئر کر دیا گیا")
    else:
        st.success("🎉 تمام کریڈٹ کلیئر ہیں!")

elif st.session_state.page == "history":
    st.subheader("📜 مکمل کاروباری ریکارڈ")
    
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
        # سمری میٹرکس
        st.metric("کل انٹریز", len(filtered_df))
        
        # ڈیٹا ٹیبل
        st.dataframe(
            filtered_df.sort_values(by="تاریخ", ascending=False),
            use_container_width=True,
            column_config={
                "تاریخ": st.column_config.DatetimeColumn(format="DD-MM-YYYY"),
                "منافع": st.column_config.NumberColumn(format="₹%d")
            }
        )
        
        # ایکسپورٹ کا آپشن
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 ڈیٹا ڈاؤن لوڈ کریں",
            data=csv,
            file_name=f"business_record_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("منتخب تاریخوں کے لیے کوئی ڈیٹا موجود نہیں ہے۔")

elif st.session_state.page == "easypaisa_details":
    st.subheader("💰 ایزی پیسہ ٹرانزیکشنز")
    easypaisa_df = df[df['کیٹیگری'] == "Banking"]
    
    if not easypaisa_df.empty:
        st.dataframe(easypaisa_df, use_container_width=True)
        st.metric("کل ایزی پیسہ سیلز", f"₹{easypaisa_sales}")
    else:
        st.info("ایزی پیسہ کا کوئی ریکارڈ موجود نہیں ہے۔")

# فوٹر
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666; font-size: 12px;'>"
    "© 2024 Ali Mobiles & Communication | Premium Shop Management System"
    "</p>",
    unsafe_allow_html=True
)
