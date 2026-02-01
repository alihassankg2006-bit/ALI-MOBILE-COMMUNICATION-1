import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import os

# --- Page Configuration ---
st.set_page_config(page_title="Ali Mobiles & Communication", page_icon="📱", layout="wide")

# --- Custom Styling (Purana Look) ---
st.markdown("""
    <style>
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #4e5d6c; }
    .target-card { background-color: #1e2130; padding: 20px; border-radius: 15px; text-align: center; border: 2px solid #00cc66; margin-bottom: 20px; }
    .today-card { background-color: #262730; padding: 15px; border-radius: 10px; border-left: 5px solid #00cc66; margin-bottom: 10px; }
    h1, h2, h3 { color: #00cc66 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- Google Sheets Connection ---
# Yeh line aapka data hamesha ke liye Google Account se jorh degi
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        df = conn.read(ttl="0")
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except:
        cols = ['Date', 'Category', 'Item', 'Cost', 'Sale', 'Profit', 'Payment']
        return pd.DataFrame(columns=cols)

df = load_data()
now = datetime.now()

# --- Header & Logo Section ---
col_head1, col_head2, col_head3 = st.columns([1, 2, 1])
with col_head2:
    # Yahan logo file ka naam likha hai. 
    # Aap apne folder mein 'logo.png' ya 'logo.jpg' ke naam se image rakhein
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    elif os.path.exists("logo.jpg"):
        st.image("logo.jpg", use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center;'>Ali Mobiles & Communication</h1>", unsafe_allow_html=True)

st.markdown("---")

# --- Navigation ---
menu = st.sidebar.radio("Main Menu", ["📝 Nayi Entry", "📊 Dashboard (Daily/Monthly)", "📅 Yearly Archive", "⚙️ Manage Records"])

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
                conn.update(data=updated_df)
                st.success("✅ Record saved to your Google Account!")
                st.rerun()

# --- 2. DASHBOARD ---
elif menu == "📊 Dashboard (Daily/Monthly)":
    if not df.empty:
        # Time Filters
        today_str = now.strftime('%Y-%m-%d')
        df_today = df[df['Date'].dt.strftime('%Y-%m-%d') == today_str]
        df_month = df[(df['Date'].dt.month == now.month) & (df['Date'].dt.year == now.year)]
        
        # Monthly Target (60,000)
        target_profit = 60000
        month_profit = df_month['Profit'].sum()
        progress = min(month_profit / target_profit, 1.0)
        
        st.markdown(f"""
            <div class="target-card">
                <h3 style='margin:0;'>🎯 Monthly Profit Target ({now.strftime('%B %Y')})</h3>
                <h1 style='margin:10px 0;'>Rs. {month_profit:,.0f} / {target_profit:,}</h1>
                <p>Progress: {progress*100:.1f}% | Remaining: Rs. {max(target_profit-month_profit, 0):,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        st.progress(progress)

        # Today vs Monthly Stats
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""<div class="today-card">
                <h4 style='margin:0;'>Aaj Ki Performance (Today)</h4>
                <h2 style='color:#00cc66;'>Sale: Rs. {df_today['Sale'].sum():,.0f}</h2>
                <h3 style='color:#fff;'>Profit: Rs. {df_today['Profit'].sum():,.0f}</h3>
            </div>""", unsafe_allow_html=True)
        
        with c2:
            st.markdown(f"""<div class="today-card" style="border-left: 5px solid #3498db;">
                <h4 style='margin:0;'>Is Mahine Ki Total (Monthly)</h4>
                <h2 style='color:#3498db;'>Sale: Rs. {df_month['Sale'].sum():,.0f}</h2>
                <h3 style='color:#fff;'>Entries: {len(df_month)}</h3>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        
        # Trend Chart
        st.subheader("📈 Monthly Sales Trend")
        fig = px.bar(df_month.groupby('Date')['Sale'].sum().reset_index(), x='Date', y='Sale', color_discrete_sequence=['#00cc66'])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Abhi tak koi entry nahi mili.")

# --- 3. YEARLY ARCHIVE ---
elif menu == "📅 Yearly Archive":
    st.header("📅 Purana Monthly Record")
    if not df.empty:
        df['Month_Year'] = df['Date'].dt.strftime('%B %Y')
        archive = df.groupby('Month_Year').agg({'Sale':'sum', 'Profit':'sum', 'Item':'count'}).reset_index()
        st.table(archive.sort_values(by='Month_Year', ascending=False))

# --- 4. MANAGE RECORDS ---
elif menu == "⚙️ Manage Records":
    st.header("⚙️ Data Management")
    st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)
    del_idx = st.number_input("Index no. likhein jo delete karna hai:", min_value=0, max_value=len(df)-1, step=1)
    if st.button("❌ Delete Permanently"):
        df = df.drop(df.index[del_idx])
        conn.update(data=df)
        st.warning("Entry deleted successfully!")
        st.rerun()
                
