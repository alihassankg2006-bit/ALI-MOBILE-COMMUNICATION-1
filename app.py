import streamlit as st
import pandas as pd
import plotly.express as px
from github import Github
import io
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Ali Mobiles & Communication", page_icon="📱", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #4e5d6c; }
    .target-card { background-color: #1e2130; padding: 20px; border-radius: 15px; text-align: center; border: 2px solid #00cc66; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- GitHub Auth ---
try:
    token = st.secrets["GITHUB_TOKEN"]
    repo_name = st.secrets["REPO_NAME"]
    g = Github(token)
    repo = g.get_repo(repo_name)
except Exception:
    st.error("Secrets Missing! Check GITHUB_TOKEN and REPO_NAME.")
    st.stop()

# --- Load Logo ---
def get_logo():
    try:
        file_content = repo.get_contents("IMG-20260127-WA0094.jpg")
        return file_content.download_url
    except:
        return None

logo_url = get_logo()

# --- Data Logic ---
CSV_FILE = "sales_record.csv"

def load_data():
    try:
        contents = repo.get_contents(CSV_FILE)
        data = contents.decoded_content.decode('utf-8')
        df = pd.read_csv(io.StringIO(data))
        df['Date'] = pd.to_datetime(df['Date'])
        return df, contents.sha
    except:
        cols = ['Date', 'Category', 'Item', 'Cost', 'Sale', 'Profit', 'Payment']
        return pd.DataFrame(columns=cols), None

def save_data(df, sha, message="Update"):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    if sha:
        repo.update_file(CSV_FILE, message, csv_buffer.getvalue(), sha)
    else:
        repo.create_file(CSV_FILE, "Initial Record", csv_buffer.getvalue())

df, current_sha = load_data()

# --- Time Context ---
now = datetime.now()
today_date = now.strftime('%Y-%m-%d')
this_month = now.month
this_year = now.year

# --- Header ---
col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
with col_l2:
    if logo_url:
        st.image(logo_url, use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #00cc66;'>Ali Mobiles & Communication</h1>", unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center;'><b>Today:</b> {now.strftime('%d %B, %Y')}</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Navigation ---
menu = st.sidebar.radio("Main Menu", ["Nayi Entry", "Dashboard (Monthly)", "Yearly Archive", "History & Delete"])

# --- 1. NEW ENTRY ---
if menu == "Nayi Entry":
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
        
        if st.form_submit_button("💾 Save to Cloud"):
            if item and sale > 0:
                profit = sale - cost
                # Nayi entry add karna
                new_row = pd.DataFrame([[date.strftime('%Y-%m-%d'), cat, item, cost, sale, profit, pay]], columns=df.columns)
                updated_df = pd.concat([df, new_row], ignore_index=True)
                # Date format fix for CSV
                updated_df['Date'] = pd.to_datetime(updated_df['Date']).dt.strftime('%Y-%m-%d')
                save_data(updated_df, current_sha, f"Added: {item}")
                st.success("✅ Saved!")
                st.rerun()

# --- 2. DASHBOARD (Monthly Focus) ---
elif menu == "Dashboard (Monthly)":
    st.header(f"📊 {now.strftime('%B %Y')} Reports")
    if not df.empty:
        # Filtering
        df['Date'] = pd.to_datetime(df['Date'])
        df_today = df[df['Date'].dt.strftime('%Y-%m-%d') == today_date]
        df_month = df[(df['Date'].dt.month == this_month) & (df['Date'].dt.year == this_year)]

        # Target Tracker
        target_profit = 60000
        current_month_profit = df_month['Profit'].sum()
        progress = min(current_month_profit / target_profit, 1.0)
        
        st.markdown(f"""
            <div class="target-card">
                <h3 style='margin:0; color:#00cc66;'>🎯 Monthly Profit Target ({now.strftime('%B')})</h3>
                <h1 style='margin:10px 0;'>Rs. {current_month_profit:,.0f} / {target_profit:,}</h1>
                <p style='color:#aaa;'>Progress: {progress*100:.1f}% | Remaining: Rs. {max(target_profit-current_month_profit, 0):,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        st.progress(progress)

        # Metrics Breakdown
        st.subheader("📍 Stats Breakdown")
        m1, m2, m3 = st.columns(3)
        m1.metric("Today's Profit", f"Rs. {df_today['Profit'].sum():,.0f}")
        m2.metric("Monthly Profit", f"Rs. {current_month_profit:,.0f}")
        m3.metric("Total Entries (Month)", len(df_month))

        st.markdown("---")
        
        # Monthly Chart
        st.subheader("📈 Monthly Sales Trend")
        if not df_month.empty:
            plot_df = df_month.groupby('Date')['Sale'].sum().reset_index()
            fig = px.bar(plot_df, x='Date', y='Sale', color='Sale', color_continuous_scale='Greens')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sales yet this month.")

    else:
        st.info("No records found.")

# --- 3. YEARLY ARCHIVE ---
elif menu == "Yearly Archive":
    st.header("📂 Business Archive")
    if not df.empty:
        df['Month_Year'] = df['Date'].dt.strftime('%B %Y')
        archive = df.groupby('Month_Year').agg({
            'Sale': 'sum',
            'Profit': 'sum',
            'Item': 'count'
        }).reset_index().sort_values(by='Month_Year', ascending=False)
        
        st.write("Summary by Month:")
        st.table(archive)
        
        selected_m = st.selectbox("Select Month for Details:", archive['Month_Year'].unique())
        st.dataframe(df[df['Month_Year'] == selected_m].drop(columns=['Month_Year']), use_container_width=True)
    else:
        st.info("Archive is empty.")

# --- 4. HISTORY ---
elif menu == "History & Delete":
    st.header("📋 All Records")
    if not df.empty:
        st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)
        delete_idx = st.number_input("Delete Index:", min_value=0, max_value=len(df)-1, step=1)
        if st.button("❌ Permanent Delete"):
            updated_df = df.drop(df.index[delete_idx])
            updated_df['Date'] = updated_df['Date'].dt.strftime('%Y-%m-%d')
            save_data(updated_df, current_sha, "Deleted")
            st.warning("Entry removed!")
            st.rerun()
