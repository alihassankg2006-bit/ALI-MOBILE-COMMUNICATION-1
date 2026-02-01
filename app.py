import streamlit as st
import pandas as pd
import plotly.express as px
from github import Github
import io
from datetime import datetime

# --- 1. Page Configuration ---
st.set_page_config(page_title="Ali Mobiles & Communication", page_icon="📱", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #4e5d6c; }
    .target-card { 
        background-color: #1e2130; 
        padding: 25px; 
        border-radius: 15px; 
        text-align: center; 
        border: 2px solid #00cc66; 
        margin-bottom: 20px; 
    }
    h1, h2, h3 { color: #00cc66 !important; }
    .status-text { font-size: 24px; font-weight: bold; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GitHub Auth ---
try:
    token = st.secrets["GITHUB_TOKEN"]
    repo_name = st.secrets["REPO_NAME"]
    g = Github(token)
    repo = g.get_repo(repo_name)
except Exception as e:
    st.error(f"Secrets Missing! Settings check karein. Error: {e}")
    st.stop()

# --- 3. Functions ---

def get_logo():
    for name in ["logo.png", "Logo.png", "logo.jpg", "Logo.jpg"]:
        try:
            return repo.get_contents(name).download_url
        except: continue
    return None

CSV_FILE = "data.csv"
COLS = ['Date', 'Category', 'Item', 'Cost', 'Sale', 'Profit', 'Payment']

def load_data():
    try:
        contents = repo.get_contents(CSV_FILE)
        raw_df = pd.read_csv(io.StringIO(contents.decoded_content.decode('utf-8')))
        if raw_df.shape[1] > 7:
            raw_df = raw_df.iloc[:, -7:]
        raw_df.columns = COLS
        raw_df['Date'] = pd.to_datetime(raw_df['Date'], errors='coerce')
        raw_df = raw_df.dropna(subset=['Date'])
        return raw_df
    except Exception:
        return pd.DataFrame(columns=COLS)

def save_data(df, message="Update"):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    try:
        contents = repo.get_contents(CSV_FILE)
        repo.update_file(CSV_FILE, message, csv_buffer.getvalue(), contents.sha)
        return True
    except Exception:
        try:
            repo.create_file(CSV_FILE, "Initial", csv_buffer.getvalue())
            return True
        except: return False

# --- 4. Logic ---
df = load_data()
logo_url = get_logo()
now = datetime.now()

# Header
col_h1, col_h2, col_h3 = st.columns([1, 2, 1])
with col_h2:
    if logo_url: st.image(logo_url, use_container_width=True)
    else: st.markdown("<h1 style='text-align: center;'>Ali Mobiles & Communication</h1>", unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center;'><b>آج:</b> {now.strftime('%d %B, %Y')}</p>", unsafe_allow_html=True)
st.markdown("---")

menu = st.sidebar.radio("Main Menu", ["📝 Nayi Entry", "📊 Dashboard", "📂 Archive", "⚙️ Manage Records"])

# --- SECTION 1: ENTRY ---
if menu == "📝 Nayi Entry":
    st.header("📝 Nayi Entry Karein")
    with st.form("entry_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            date_input = st.date_input("Tareekh", now)
            cat = st.selectbox("Category", ["Accessories", "Repairing"])
            item = st.text_input("Item Name / Kaam")
        with c2:
            cost = st.number_input("Cost (Khareed)", 0.0)
            sale = st.number_input("Sale (Becha)", 0.0)
            pay = st.selectbox("Payment", ["Cash", "EasyPaisa", "JazzCash"])
        
        if st.form_submit_button("💾 Save Entry"):
            if item and sale >= 0:
                profit = sale - cost
                new_row = pd.DataFrame([[pd.to_datetime(date_input), cat, item, cost, sale, profit, pay]], columns=COLS)
                df = pd.concat([df, new_row], ignore_index=True)
                df['Date'] = pd.to_datetime(df['Date'])
                save_df = df.copy()
                save_df['Date'] = save_df['Date'].dt.strftime('%Y-%m-%d')
                if save_data(save_df, f"Added: {item}"):
                    st.success("✅ Entry saved successfully!")
                    st.rerun()

# --- SECTION 2: DASHBOARD ---
elif menu == "📊 Dashboard":
    st.header(f"📊 {now.strftime('%B %Y')} Reports")
    if not df.empty:
        df_month = df[(df['Date'].dt.month == now.month) & (df['Date'].dt.year == now.year)]
        df_today = df[df['Date'].dt.date == now.date()]

        # Totals
        target = 60000
        m_sale = df_month['Sale'].sum()
        m_profit = df_month['Profit'].sum()
        t_profit = df_today['Profit'].sum()
        
        completion_pct = (m_profit / target) * 100 if target > 0 else 0
        remaining = target - m_profit if target > m_profit else 0
        
        if completion_pct < 50: status_color = "#ff4b4b"
        elif completion_pct < 100: status_color = "#ffcc00"
        else: status_color = "#00cc66"

        st.markdown(f"""
            <div class="target-card" style="border-color: {status_color};">
                <h3 style="color: #ffffff !important; margin-bottom: 5px;">🎯 Monthly Profit Target: {now.strftime('%B')}</h3>
                <h1 style="color: #ffffff !important; margin: 0;">Rs. {m_profit:,.0f} / {target:,}</h1>
                <div class="status-text" style="color: {status_color};">
                    {completion_pct:.1f}% Target Completed
                </div>
                {f"<p style='color: #aeb2b7;'>باقی ہدف: Rs. {remaining:,.0f}</p>" if remaining > 0 else "<p style='color: #00cc66; font-weight: bold;'>مبروک! ہدف مکمل ہو گیا 🎉</p>"}
            </div>
            """, unsafe_allow_html=True)
        
        st.progress(min(m_profit/target, 1.0) if target > 0 else 0)

        col1, col2, col3 = st.columns(3)
        col1.metric("Monthly Total Sale", f"Rs. {m_sale:,.0f}")
        col2.metric("Today's Profit", f"Rs. {t_profit:,.0f}")
        col3.metric("Monthly Entries", f"{len(df_month)}")
        
        st.markdown("---")
        if not df_month.empty:
            chart_data = df_month.groupby(df_month['Date'].dt.date)['Sale'].sum().reset_index()
            # Yahan error tha, ab theek kar diya hai:
            st.plotly_chart(px.bar(chart_data, x='Date', y='Sale', title="Daily Sales Graph", color_discrete_sequence=['#00cc66']), use_container_width=True)
    else: st.info("No records for this month.")

# --- SECTION 3: ARCHIVE ---
elif menu == "📂 Archive":
    st.header("📂 Purana Monthly Record")
    if not df.empty:
        df['Month_Year'] = df['Date'].dt.strftime('%B %Y')
        summary = df.groupby('Month_Year').agg({'Sale': 'sum', 'Profit': 'sum', 'Item': 'count'}).reset_index().sort_values(by='Month_Year', ascending=False)
        st.table(summary)
        sel_m = st.selectbox("Select Month for Detail:", summary['Month_Year'].unique())
        detail_df = df[df['Month_Year'] == sel_m].sort_values(by='Date', ascending=False)
        st.dataframe(detail_df[COLS], use_container_width=True)
    else: st.info("Archive is empty.")

# --- SECTION 4: MANAGE ---
elif menu == "⚙️ Manage Records":
    st.header("⚙️ Data Management")
    if not df.empty:
        st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)
        idx = st.number_input("Index to Delete:", 0, len(df)-1, 0)
        if st.button("❌ Delete Permanently"):
            df = df.drop(df.index[idx])
            save_df = df.copy()
            save_df['Date'] = save_df['Date'].dt.strftime('%Y-%m-%d')
            if save_data(save_df, "Deleted"):
                st.warning("Record Removed!")
                st.rerun()
                
