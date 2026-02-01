import streamlit as st
import pandas as pd
import plotly.express as px
from github import Github
import io
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Ali Mobiles & Communication", page_icon="📱", layout="wide")

# Custom Styling (Original Professional Look)
st.markdown("""
    <style>
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #4e5d6c; }
    .target-card { background-color: #1e2130; padding: 20px; border-radius: 15px; text-align: center; border: 2px solid #00cc66; margin-bottom: 20px; }
    h1, h2, h3 { color: #00cc66 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- GitHub Auth ---
try:
    token = st.secrets["GITHUB_TOKEN"]
    repo_name = st.secrets["REPO_NAME"]
    g = Github(token)
    repo = g.get_repo(repo_name)
except Exception as e:
    st.error(f"Secrets Missing! Check Streamlit Settings. Error: {e}")
    st.stop()

# --- Flexible Logo Search ---
def get_logo():
    for name in ["logo.png", "Logo.png", "logo.jpg", "Logo.jpg"]:
        try:
            return repo.get_contents(name).download_url
        except: continue
    return None

logo_url = get_logo()

# --- Data Logic (Specific to your data.csv) ---
CSV_FILE = "data.csv"
COLS = ['Date', 'Category', 'Item', 'Cost', 'Sale', 'Profit', 'Payment']

def load_data():
    try:
        contents = repo.get_contents(CSV_FILE)
        raw_df = pd.read_csv(io.StringIO(contents.decoded_content.decode('utf-8')))
        
        # Faltu index columns ko hatana (Cleaning your data.csv structure)
        if raw_df.columns[0].startswith('Unnamed') or raw_df.columns[0] == "":
            raw_df = raw_df.iloc[:, 1:]
        
        # Column names ko set karna
        raw_df.columns = COLS
        raw_df['Date'] = pd.to_datetime(raw_df['Date'])
        return raw_df, contents.sha
    except Exception as e:
        return pd.DataFrame(columns=COLS), None

def save_data(df, sha, msg="Update"):
    csv_buf = io.StringIO()
    df.to_csv(csv_buf, index=False)
    if sha: repo.update_file(CSV_FILE, msg, csv_buf.getvalue(), sha)
    else: repo.create_file(CSV_FILE, "Initial", csv_buf.getvalue())

df, current_sha = load_data()
now = datetime.now()

# --- Header Section ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if logo_url: st.image(logo_url, use_container_width=True)
    else: st.markdown("<h1 style='text-align: center;'>Ali Mobiles & Communication</h1>", unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center;'><b>آج کی تاریخ:</b> {now.strftime('%d %B, %Y')}</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Navigation ---
menu = st.sidebar.radio("Main Menu", ["📝 Nayi Entry", "📊 Dashboard", "📂 Archive", "⚙️ Manage Records"])

# --- 1. NEW ENTRY ---
if menu == "📝 Nayi Entry":
    st.header("📝 Nayi Entry Karein")
    with st.form("entry_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            date = st.date_input("Tareekh", now)
            cat = st.selectbox("Category", ["Accessories", "Repairing"])
            item = st.text_input("Item Name / Kaam")
        with c2:
            cost = st.number_input("Khareed (Cost)", min_value=0.0)
            sale = st.number_input("Becha (Sale)", min_value=0.0)
            pay = st.selectbox("Payment", ["Cash", "EasyPaisa", "JazzCash"])
        
        if st.form_submit_button("💾 Save to Cloud"):
            if item and sale > 0:
                profit = sale - cost
                new_row = pd.DataFrame([[date.strftime('%Y-%m-%d'), cat, item, cost, sale, profit, pay]], columns=COLS)
                df = pd.concat([df, new_row], ignore_index=True)
                # Save without index to keep data.csv clean
                save_data(df, current_sha, f"Added: {item}")
                st.success("✅ Record saved successfully to data.csv!")
                st.rerun()

# --- 2. DASHBOARD ---
elif menu == "📊 Dashboard":
    st.header(f"📊 {now.strftime('%B %Y')} Reports")
    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'])
        # Today's data
        df_today = df[df['Date'].dt.date == now.date()]
        # Current month's data
        df_month = df[(df['Date'].dt.month == now.month) & (df['Date'].dt.year == now.year)]

        target = 60000
        m_profit = df_month['Profit'].sum()
        progress = min(m_profit / target, 1.0) if target > 0 else 0
        
        st.markdown(f"""
            <div class="target-card">
                <h3 style='margin:0;'>🎯 Monthly Profit Target ({now.strftime('%B')})</h3>
                <h1 style='margin:10px 0;'>Rs. {m_profit:,.0f} / {target:,}</h1>
                <p>Progress: {progress*100:.1f}% | Remaining: Rs. {max(target-m_profit, 0):,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        st.progress(progress)

        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Today's Profit", f"Rs. {df_today['Profit'].sum():,.0f}")
        col_m2.metric("Monthly Profit", f"Rs. {m_profit:,.0f}")
        col_m3.metric("Monthly Entries", len(df_month))

        st.markdown("---")
        st.subheader("📈 Monthly Sales Chart")
        if not df_month.empty:
            chart_data = df_month.groupby('Date')['Sale'].sum().reset_index()
            fig = px.bar(chart_data, x='Date', y='Sale', color_discrete_sequence=['#00cc66'])
            st.plotly_chart(fig, use_container_width=True)
    else: st.info("Abhi is mahine ka koi record nahi mila.")

# --- 3. ARCHIVE ---
elif menu == "📂 Archive":
    st.header("📂 Purana Monthly Record")
    if not df.empty:
        df['Month_Year'] = df['Date'].dt.strftime('%B %Y')
        archive = df.groupby('Month_Year').agg({'Sale':'sum', 'Profit':'sum', 'Item':'count'}).reset_index().sort_values(by='Month_Year', ascending=False)
        st.table(archive)
        selected = st.selectbox("Details dekhne ke liye mahina select karein:", archive['Month_Year'].unique())
        st.dataframe(df[df['Month_Year'] == selected].drop(columns=['Month_Year']), use_container_width=True)

# --- 4. MANAGE RECORDS ---
elif menu == "⚙️ Manage Records":
    st.header("⚙️ Data Management")
    st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)
    idx = st.number_input("Delete Index:", min_value=0, max_value=len(df)-1 if len(df)>0 else 0, step=1)
    if st.button("❌ Delete Permanently"):
        df = df.drop(df.index[idx])
        save_data(df, current_sha, "Deleted")
        st.warning("Entry deleted!")
        st.rerun()
