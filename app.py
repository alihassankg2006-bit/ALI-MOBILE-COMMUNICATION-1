import streamlit as st
import pandas as pd
from datetime import datetime

# ایپ کی سیٹنگ
st.set_page_config(page_title="Ali Mobile Shop", layout="centered")
st.title("📱 علی موبائل شاپ - ریکارڈ")

# ڈیٹا اسٹور کرنے کا سسٹم
if 'shop_data' not in st.session_state:
    st.session_state.shop_data = pd.DataFrame(columns=["تاریخ", "آئٹم", "خریداری", "فروخت", "منافع"])

# انٹری فارم
with st.form("entry_form", clear_on_submit=True):
    st.write("### نئی سیل درج کریں")
    item = st.text_input("آئٹم (مثلاً: کیبل)")
    cost = st.number_input("خریداری قیمت", min_value=0)
    sale = st.number_input("فروخت قیمت", min_value=0)
    
    submit = st.form_submit_button("سیو کریں")
    
    if submit:
        profit = sale - cost
        new_row = {"تاریخ": datetime.now().strftime("%Y-%m-%d"), "آئٹم": item, "خریداری": cost, "فروخت": sale, "منافع": profit}
        st.session_state.shop_data = pd.concat([st.session_state.shop_data, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"محفوظ ہو گیا! منافع: {profit}")

# آج کا ریکارڈ
st.divider()
total_profit = st.session_state.shop_data["منافع"].sum()
st.metric("آج کا کل منافع", f"{total_profit} PKR")
st.dataframe(st.session_state.shop_data)
  
