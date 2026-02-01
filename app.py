import streamlit as st
import pandas as pd
import plotly.express as px
from github import Github
import io
from datetime import datetime

# --- 1. Page Configuration ---
st.set_page_config(page_title="Ali Mobiles & Communication", page_icon="📱", layout="wide")

# Custom Styling (Professional Look)
st.markdown("""
    <style>
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #4e5d6c; }
    .target-card { background-color: #1e2130; padding: 20px; border-radius: 15px; text-align: center; border: 2px solid #00cc66; margin-bottom: 20px; }
    h1, h2, h3 { color: #00cc66 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GitHub Authentication ---
try:
    token = st.secrets["GITHUB_TOKEN"]
    repo_name = st.secrets["REPO_NAME"]
    g = Github(token)
    repo = g.get_repo(repo_name)
except Exception as e:
    st.error(f"Secrets Missing! Check Settings. Error: {e}")
    st.stop()

# --- 3. Functions ---

# Logo Search Function
def get_logo():
    for name in ["logo.png", "Logo.png", "logo.jpg", "Logo.jpg"]:
        try:
            return repo.get_contents(name).download_url
        except: continue
    return None

CSV_FILE = "data.csv"
COLS = ['Date', 'Category', 'Item', 'Cost', 'Sale', 'Profit', 'Payment']

# Data Loading Function
def load_data():
    try:
        contents = repo.get_contents(CSV_FILE)
        raw_df = pd.read_csv(io.StringIO(contents.decoded_content.decode('utf-8')))
        # Index column check and cleaning
        if raw_df.columns[0].startswith('Unnamed') or raw_df.columns[0] == "":
            raw_df = raw_df.iloc[:, 1:]
        raw_df.columns = COLS
        raw_df['Date'] = pd.to_datetime(raw_df['Date'])
        return raw_df
    except Exception:
        return pd.DataFrame(columns=COLS)

# Data Saving Function (Fixed for GithubException)
def save_data(df, message="Update"):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    try:
        # Always get the latest SHA before saving to avoid errors
        contents = repo.get_contents(CSV_FILE)
        repo.update_file(CSV_FILE, message, csv_buffer.getvalue(), contents.sha)
    except Exception:
        # If file doesn't exist, create it
        repo.create_file(CSV_FILE, "Initial Record", csv_buffer.getvalue())
    return True

# --- 4. App Logic ---

df = load_data()
logo_url = get_logo()
now = datetime.now()

# Header Section
col_h1, col_h2, col_h3 = st.columns([1, 2, 1])
with col_h2:
    if logo_url: st.image(logo_url, use_container_width=True)
    else: st.markdown("<h1 style='text-align: center;'>Ali Mobiles & Communication</h1>", unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center;'><b>آج کی تاریخ:</b> {now.strftime('%d %B, %Y')}</p>", unsafe_allow_html=True)
st.markdown("---")

# Navigation Sidebar
menu = st.sidebar.radio("Main Menu", ["📝 Nayi Entry", "📊 Dashboard", "📂 Archive", "⚙️ Manage Records"])

# --- SECTION 1: NEW ENTRY ---
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
            if item and sale >= 0:
                profit = sale - cost
                new_row = pd.DataFrame([[date.strftime('%Y-%m-%d'), cat, item, cost, sale, profit, pay]], columns=COLS)
                updated_df = pd.concat([df, new_row], ignore_index=True)
                # Date fix for CSV consistency
                updated_df['Date'] = pd.to_datetime(updated_df['Date']).dt.strftime('%Y-%m-%d')
                if save_data(updated_df, f"Added: {item}"):
                    st.success(f"✅ Record saved: {item}")
                    st.rerun()

# --- SECTION 2: DASHBOARD (Current Month Focus) ---
elif menu == "📊 Dashboard":
    st.header(f"📊 {now.strftime('%B %Y')} کی کارکردگی")
    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'])
        # Current month filtering
        df_month = df[(df['Date'].dt.month == now.month) & (df['Date'].dt.year == now.year)]
        df_today = df[df['Date'].dt.date == now.date()]

        # Target Tracker (60,000 PKR)
        target = 60000
        m_profit = df_month['Profit'].sum()
        progress = min(m_profit / target, 1.0) if target > 0 else 0
        
        st.markdown(f"""
            <div class="target-card">
                <h3 style='margin:0;'>🎯 ماہانہ ہدف ({now.strftime('%B')})</h3>
                <h1 style='margin:10px 0;'>Rs. {m_profit:,.0f} / {target:,}</h1>
                <p>Progress: {progress*100:.1f}% | Remaining: Rs. {max(target-m_profit, 0):,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        st.progress(progress)

        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("آج کا منافع", f"Rs. {df_today['Profit'].sum():,.0f}")
        col_m2.metric("اس ماہ کا منافع", f"Rs. {m_profit:,.0f}")
        col_m3.metric("ماہانہ کل سیل", f"Rs. {df_month['Sale'].sum():,.0f}")

        st.markdown("---")
        st.subheader("📈 سیل کا گراف (موجودہ مہینہ)")
        if not df_month.empty:
            chart_data = df_month.groupby('Date')['Sale'].sum().reset_index()
            fig = px.bar(chart_data, x='Date', y='Sale', color_discrete_sequence=['#00cc66'], labels={'Sale':'فروخت', 'Date':'تاریخ'})
            st.plotly_chart(fig, use_container_width=True)
    else: st.info("ابھی اس مہینے کا کوئی ریکارڈ نہیں ملا۔")

# --- SECTION 3: ARCHIVE ---
elif menu == "📂 Archive":
    st.header("📂 پرانا ماہانہ ریکارڈ (Archive)")
    if not df.empty:
        df['Month_Year'] = df['Date'].dt.strftime('%B %Y')
        archive_summary = df.groupby('Month_Year').agg({'Sale':'sum', 'Profit':'sum', 'Item':'count'}).reset_index().sort_values(by='Month_Year', ascending=False)
        st.table(archive_summary)
        
        selected_month = st.selectbox("تفصیل دیکھنے کے لیے مہینہ منتخب کریں:", archive_summary['Month_Year'].unique())
        st.dataframe(df[df['Month_Year'] == selected_month].drop(columns=['Month_Year']), use_container_width=True)

# --- SECTION 4: MANAGE RECORDS ---
elif menu == "⚙️ Manage Records":
    st.header("⚙️ ریکارڈ کی کانٹ چھانٹ")
    st.write("یہاں سے آپ پرانی انٹریز دیکھ سکتے ہیں یا انہیں ڈیلیٹ کر سکتے ہیں۔")
    st.dataframe(df.sort_values(by='Date', ascending=False), use_container_width=True)
    
    idx_to_del = st.number_input("ڈیلیٹ کرنے کے لیے انڈیکس نمبر لکھیں:", min_value=0, max_value=len(df)-1 if len(df)>0 else 0, step=1)
    if st.button("❌ مستقل طور پر ڈیلیٹ کریں"):
        updated_df = df.drop(df.index[idx_to_del])
        updated_df['Date'] = pd.to_datetime(updated_df['Date']).dt.strftime('%Y-%m-%d')
        if save_data(updated_df, "Deleted Entry"):
            st.warning("ریکارڈ ڈیلیٹ کر دیا گیا ہے!")
            st.rerun()
