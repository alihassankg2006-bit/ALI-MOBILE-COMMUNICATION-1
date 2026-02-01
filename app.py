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
    h1, h2, h3 { color: #00cc66 !important; }
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
    for name in ["logo.png", "Logo.png", "logo.jpg", "Logo.jpg"]:
        try:
            return repo.get_contents(name).download_url
        except: continue
    return None

logo_url = get_logo()

# --- Data Logic (Robust Cleaning) ---
CSV_FILE = "data.csv"
EXPECTED_COLS = ['Date', 'Category', 'Item', 'Cost', 'Sale', 'Profit', 'Payment']

def load_data():
    try:
        contents = repo.get_contents(CSV_FILE)
        df = pd.read_csv(io.StringIO(contents.decoded_content.decode('utf-8')))
        
        # Faltu index column hatana (Unnamed column fix)
        if df.columns[0].startswith('Unnamed') or df.columns[0] == "":
            df = df.iloc[:, 1:]
            
        # Sirf zaruri columns rakhna
        df = df[EXPECTED_COLS]
        df['Date'] = pd.to_datetime(df['Date'])
        return df, contents.sha
    except Exception as e:
        return pd.DataFrame(columns=EXPECTED_COLS), None

def save_data(df, sha, message="Update"):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    if sha: repo.update_file(CSV_FILE, message, csv_buffer.getvalue(), sha)
    else: repo.create_file(CSV_FILE, "Initial Record", csv_buffer.getvalue())

df, current_sha = load_data()
now = datetime.now()

# --- Header ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if logo_url: st.image(logo_url, use_container_width=True)
    else: st.markdown("<h1 style='text-align: center;'>Ali Mobiles & Communication</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'><b>آج:</b> {now.strftime('%d %B, %Y')}</p>", unsafe_allow_html=True)

# --- Navigation ---
menu = st.sidebar.radio("Main Menu", ["📝 Nayi Entry", "📊 Dashboard", "📂 Archive", "⚙️ Delete"])

if menu == "📝 Nayi Entry":
    st.header("📝 Nayi Entry")
    with st.form("entry_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            date = st.date_input("Tareekh", now)
            cat = st.selectbox("Category", ["Accessories", "Repairing"])
            item = st.text_input("Item Name")
        with c2:
            cost = st.number_input("Cost", 0.0)
            sale = st.number_input("Sale", 0.0)
            pay = st.selectbox("Payment", ["Cash", "EasyPaisa", "JazzCash"])
        
        if st.form_submit_button("💾 Save"):
            if item and sale > 0:
                profit = sale - cost
                new_row = pd.DataFrame([[date.strftime('%Y-%m-%d'), cat, item, cost, sale, profit, pay]], columns=EXPECTED_COLS)
                updated_df = pd.concat([df, new_row], ignore_index=True)
                save_data(updated_df, current_sha, f"Added: {item}")
                st.success("✅ Saved!")
                st.rerun()

elif menu == "📊 Dashboard":
    st.header(f"📊 {now.strftime('%B %Y')}")
    if not df.empty:
        df_m = df[(df['Date'].dt.month == now.month) & (df['Date'].dt.year == now.year)]
        t_prof = 60000
        m_prof = df_m['Profit'].sum()
        
        st.markdown(f'<div class="target-card"><h3>🎯 Target: {now.strftime("%B")}</h3><h1>Rs. {m_prof:,.0f} / {t_prof:,}</h1></div>', unsafe_allow_html=True)
        st.progress(min(m_prof/t_prof, 1.0) if t_prof > 0 else 0)

        col1, col2 = st.columns(2)
        col1.metric("Today's Profit", f"Rs. {df[df['Date'].dt.date == now.date()]['Profit'].sum():,.0f}")
        col2.metric("Monthly Entries", len(df_m))
        
        st.plotly_chart(px.bar(df_m.groupby('Date')['Sale'].sum().reset_index(), x='Date', y='Sale', color_discrete_sequence=['#00cc66']))
    else: st.info("No records found.")

elif menu == "📂 Archive":
    st.header("📂 Purana Record")
    if not df.empty:
        df['Month'] = df['Date'].dt.strftime('%B %Y')
        summary = df.groupby('Month').agg({'Sale':'sum', 'Profit':'sum'}).reset_index().sort_values(by='Month', ascending=False)
        st.table(summary)
        sel_m = st.selectbox("Mahina select karein:", summary['Month'].unique())
        st.dataframe(df[df['Month'] == sel_m].drop(columns=['Month']), use_container_width=True)

elif menu == "⚙️ Delete":
    st.header("⚙️ Delete Records")
    st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)
    idx = st.number_input("Index:", 0, len(df)-1 if len(df)>0 else 0, 1)
    if st.button("❌ Delete"):
        df = df.drop(df.index[idx])
        save_data(df, current_sha, "Deleted")
        st.warning("Deleted!")
        st.rerun()
