import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Ali Mobiles & Communication", page_icon="📱", layout="wide")

# --- Custom CSS (Vohi Purana Wala Design) ---
st.markdown("""
    <style>
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #4e5d6c; }
    .target-card { background-color: #1e2130; padding: 20px; border-radius: 15px; text-align: center; border: 2px solid #00cc66; margin-bottom: 20px; }
    .today-card { background-color: #262730; padding: 15px; border-radius: 10px; border-left: 5px solid #00cc66; }
    h1, h2, h3 { color: #00cc66 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- Google Sheets Connection ---
# Yeh aapka data Google Account ke saath jorh dega
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        # Google Sheet se data uthayega
        df = conn.read(ttl="0")
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except:
        cols = ['Date', 'Category', 'Item', 'Cost', 'Sale', 'Profit', 'Payment']
        return pd.DataFrame(columns=cols)

df = load_data()

# --- Header & Logo ---
# Logo ka purana link (ya aap yahan apna naya link bhi daal sakte hain)
logo_url = "https://raw.githubusercontent.com/AliHassan/mobile-shop/main/IMG-20260127-WA0094.jpg" 
st.markdown("<h1 style='text-align: center;'>Ali Mobiles & Communication</h1>", unsafe_allow_html=True)
st.image(logo_url, width=200) # Agar URL kaam na kare toh local file bhi lag sakti hai

st.markdown("---")

# --- Navigation ---
menu = st.sidebar.radio("Main Menu", ["📝 Nayi Entry", "📊 Dashboard", "📅 Yearly Archive", "⚙️ Manage Records"])

now = datetime.now()

# --- 1. NEW ENTRY ---
if menu == "📝 Nayi Entry":
    st.header("📝 Nayi Entry Karein")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Tareekh", now)
            cat = st.selectbox("Category", ["Accessories", "Repairing"])
            item = st.text_input("Item Name / Kaam")
        with col2:
            cost = st.number_input("Khareed (Cost)", min_value=0.0)
            sale = st.number_input("Becha (Sale)", min_value=0.0)
            pay = st.selectbox("Payment", ["Cash", "EasyPaisa", "JazzCash"])
        
        if st.form_submit_button("💾 Save to Google Account"):
            if item and sale > 0:
                profit = sale - cost
                new_row = pd.DataFrame([[date.strftime('%Y-%m-%d'), cat, item, cost, sale, profit, pay]], columns=df.columns)
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(data=updated_df) # Google Sheet par save kar dega
                st.success("✅ Data Google Sheet par save ho gaya!")
                st.rerun()

# --- 2. DASHBOARD (Daily & Monthly) ---
elif menu == "📊 Dashboard":
    if not df.empty:
        # Time Calculations
        today_str = now.strftime('%Y-%m-%d')
        df_today = df[df['Date'].dt.strftime('%Y-%m-%d') == today_str]
        df_month = df[(df['Date'].dt.month == now.month) & (df['Date'].dt.year == now.year)]
        
        # Target Section (Rs. 60,000)
        target_profit = 60000
        month_profit = df_month['Profit'].sum()
        progress = min(month_profit / target_profit, 1.0)
        
        st.markdown(f"""
            <div class="target-card">
                <h3 style='margin:0;'>🎯 Monthly Profit Target ({now.strftime('%B')})</h3>
                <h1 style='margin:10px 0;'>Rs. {month_profit:,.0f} / {target_profit:,}</h1>
                <p>Progress: {progress*100:.1f}% | Remaining: Rs. {max(target_profit-month_profit, 0):,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        st.progress(progress)

        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown(f"""<div class="today-card">
                <h4>Aaj Ki Performance (Today)</h4>
                <h2>Sale: Rs. {df_today['Sale'].sum():,.0f}</h2>
                <h3>Profit: Rs. {df_today['Profit'].sum():,.0f}</h3>
            </div>""", unsafe_allow_html=True)
        
        with col_t2:
            st.markdown(f"""<div class="today-card" style="border-left: 5px solid #3498db;">
                <h4>Is Mahine Ki Total (Monthly)</h4>
                <h2>Sale: Rs. {df_month['Sale'].sum():,.0f}</h2>
                <h3>Entries: {len(df_month)}</h3>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        
        # Trend Graph
        st.subheader("📈 Monthly Sales Trend")
        fig = px.bar(df_month.groupby('Date')['Sale'].sum().reset_index(), x='Date', y='Sale', color='Sale')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data found.")

# --- 3. YEARLY ARCHIVE ---
elif menu == "📅 Yearly Archive":
    st.header("📅 Purana Record")
    if not df.empty:
        df['Month_Year'] = df['Date'].dt.strftime('%B %Y')
        archive = df.groupby('Month_Year').agg({'Sale':'sum', 'Profit':'sum', 'Item':'count'}).reset_index()
        st.table(archive.sort_values(by='Month_Year', ascending=False))
        
        selected = st.selectbox("Select Month to See Details:", df['Month_Year'].unique())
        st.dataframe(df[df['Month_Year'] == selected], use_container_width=True)

# --- 4. MANAGE RECORDS ---
elif menu == "⚙️ Manage Records":
    st.header("⚙️ Edit/Delete Records")
    st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)
    
    del_idx = st.number_input("Enter Row Index to Delete:", min_value=0, max_value=len(df)-1, step=1)
    if st.button("❌ Delete Permanently"):
        df = df.drop(df.index[del_idx])
        conn.update(data=df)
        st.warning("Entry deleted from Google Sheet!")
        st.rerun()
