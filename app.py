import streamlit as st
import pandas as pd
import plotly.express as px
from github import Github
import io
from datetime import datetime
import pytz

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
    .expense-card { 
        background-color: #1e2130; 
        padding: 25px; 
        border-radius: 15px; 
        text-align: center; 
        border: 2px solid #ff4b4b; 
        margin-bottom: 20px; 
    }
    h1, h2, h3 { color: #00cc66 !important; }
    .status-text { font-size: 24px; font-weight: bold; margin-top: 10px; }
    div[data-testid="stExpander"] { border: 1px solid #4e5d6c; border-radius: 10px; margin-bottom: 10px; }
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
    save_df = df.copy()
    save_df['Date'] = pd.to_datetime(save_df['Date']).dt.strftime('%Y-%m-%d')
    save_df.to_csv(csv_buffer, index=False)
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
pk_tz = pytz.timezone('Asia/Karachi')
now = datetime.now(pk_tz)

df = load_data()
logo_url = get_logo()

# Header
col_h1, col_h2, col_h3 = st.columns([1, 2, 1])
with col_h2:
    if logo_url: 
        st.image(logo_url, use_container_width=True)
    else: 
        st.markdown("<h1 style='text-align: center;'>Ali Mobiles & Communication</h1>", unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center;'><b>آج کی تاریخ:</b> {now.strftime('%d %B, %Y')}</p>", unsafe_allow_html=True)
st.markdown("---")

menu = st.sidebar.radio("Main Menu", ["📝 Nayi Entry", "📊 Dashboard", "📂 Archive", "⚙️ Manage Records"])

# --- SECTION 1: ENTRY ---
if menu == "📝 Nayi Entry":
    st.header("📝 Nayi Entry Karein")
    with st.form("entry_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            date_input = st.date_input("Tareekh", now.date())
            cat = st.selectbox("Category", ["Accessories", "Repairing", "Ghar ka Kharcha"])
            item = st.text_input("Item Name / Kaam / Detail")
        with c2:
            cost = st.number_input("Cost (Khareed / Kharcha)", 0.0)
            sale = st.number_input("Sale (Becha)", 0.0)
            pay = st.selectbox("Payment", ["Cash", "EasyPaisa", "JazzCash"])
        
        if st.form_submit_button("💾 Save Entry"):
            if item:
                profit = (sale - cost) if cat != "Ghar ka Kharcha" else 0
                new_row = pd.DataFrame([[pd.to_datetime(date_input), cat, item, cost, sale, profit, pay]], columns=COLS)
                df = pd.concat([df, new_row], ignore_index=True)
                if save_data(df, f"Added: {item} ({cat})"):
                    st.success(f"✅ {item} محفوظ کر لیا گیا!")
                    st.rerun()

# --- SECTION 2: DASHBOARD ---
elif menu == "📊 Dashboard":
    st.header(f"📊 {now.strftime('%B %Y')} Reports")
    if not df.empty:
        df_month = df[(df['Date'].dt.month == now.month) & (df['Date'].dt.year == now.year)]
        df_today = df[df['Date'].dt.date == now.date()]

        m_shop_profit = df_month[df_month['Category'] != "Ghar ka Kharcha"]['Profit'].sum()
        m_home_expense = df_month[df_month['Category'] == "Ghar ka Kharcha"]['Cost'].sum()
        net_savings = m_shop_profit - m_home_expense

        # Target Updated to 90,000
        target = 90000 
        completion_pct = (m_shop_profit / target) * 100 if target > 0 else 0
        
        row_cards = st.columns(2)
        with row_cards[0]:
            st.markdown(f"""
                <div class="target-card">
                    <h3 style="color:white !important;">🎯 Monthly Shop Profit Target</h3>
                    <h1 style="color:white !important;">Rs. {m_shop_profit:,.0f} / {target:,}</h1>
                    <div class="status-text">{completion_pct:.1f}% مکمل</div>
                </div>
                """, unsafe_allow_html=True)
        
        with row_cards[1]:
            st.markdown(f"""
                <div class="expense-card">
                    <h3 style="color:white !important;">🏠 Ghar ka Kharcha</h3>
                    <h1 style="color:white !important;">Rs. {m_home_expense:,.0f}</h1>
                    <div class="status-text" style="color:#ff4b4b !important;">Net Savings: Rs. {net_savings:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)

        st.progress(min(max(m_shop_profit,0)/target, 1.0) if target > 0 else 0)

        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("Shop Total Sale", f"Rs. {df_month[df_month['Category'] != 'Ghar ka Kharcha']['Sale'].sum():,.0f}")
        col2.metric("Today's Profit", f"Rs. {df_today[df_today['Category'] != 'Ghar ka Kharcha']['Profit'].sum():,.0f}")
        col3.metric("Today's Home Expense", f"Rs. {df_today[df_today['Category'] == 'Ghar ka Kharcha']['Cost'].sum():,.0f}")

        st.markdown("### 📋 Aaj Ka Record (Detailed)")
        if not df_today.empty:
            st.table(df_today[['Item', 'Category', 'Cost', 'Sale', 'Profit', 'Payment']])
        else:
            st.info("آج ابھی تک کوئی اینٹری نہیں کی گئی۔")
            
    else: st.info("ریکارڈ خالی ہے۔")

# --- SECTION 3: ARCHIVE ---
elif menu == "📂 Archive":
    st.header("📂 Purana Monthly Record")
    if not df.empty:
        df['Month_Year'] = df['Date'].dt.strftime('%B %Y')
        
        summary = df.groupby('Month_Year').apply(lambda x: pd.Series({
            'Total Sale': x[x['Category'] != 'Ghar ka Kharcha']['Sale'].sum(),
            'Shop Profit': x[x['Category'] != 'Ghar ka Kharcha']['Profit'].sum(),
            'Home Expense': x[x['Category'] == 'Ghar ka Kharcha']['Cost'].sum(),
            'Net Savings': x[x['Category'] != 'Ghar ka Kharcha']['Profit'].sum() - x[x['Category'] == 'Ghar ka Kharcha']['Cost'].sum()
        })).reset_index().sort_values(by='Month_Year', ascending=False)
        
        st.table(summary.style.format({
            'Total Sale': 'Rs. {:,.0f}',
            'Shop Profit': 'Rs. {:,.0f}',
            'Home Expense': 'Rs. {:,.0f}',
            'Net Savings': 'Rs. {:,.0f}'
        }))
        
        st.markdown("---")
        sel_m = st.selectbox("Select Month for Detail:", summary['Month_Year'].unique())
        detail_df = df[df['Month_Year'] == sel_m].sort_values(by='Date', ascending=False)
        st.dataframe(detail_df[COLS], use_container_width=True)

# --- SECTION 4: MANAGE ---
elif menu == "⚙️ Manage Records":
    st.header("⚙️ Records Edit ya Delete Karein")
    if not df.empty:
        st.subheader("Recent Entries")
        temp_df = df.sort_index(ascending=False).head(20)
        st.dataframe(temp_df[COLS], use_container_width=True)
        
        st.markdown("---")
        action_idx = st.number_input("Enter Index to Edit/Delete:", 0, len(df)-1, value=len(df)-1)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🖊️ Edit This Entry"):
                st.session_state.edit_mode = True
                st.session_state.edit_idx = action_idx
        with col_btn2:
            if st.button("❌ Delete Permanently"):
                item_name = df.iloc[action_idx]['Item']
                df = df.drop(df.index[action_idx])
                if save_data(df, f"Deleted: {item_name}"):
                    st.warning(f"Record '{item_name}' removed!")
                    st.rerun()

        if st.session_state.get("edit_mode", False):
            st.markdown("### 📝 Edit Entry Details")
            row = df.iloc[st.session_state.edit_idx]
            with st.form("edit_form"):
                e_date = st.date_input("Date", row['Date'])
                cat_list = ["Accessories", "Repairing", "Ghar ka Kharcha"]
                e_cat = st.selectbox("Category", cat_list, index=cat_list.index(row['Category']) if row['Category'] in cat_list else 0)
                e_item = st.text_input("Item Name", row['Item'])
                e_cost = st.number_input("Cost", float(row['Cost']))
                e_sale = st.number_input("Sale", float(row['Sale']))
                e_pay = st.selectbox("Payment", ["Cash", "EasyPaisa", "JazzCash"], index=["Cash", "EasyPaisa", "JazzCash"].index(row['Payment']))
                
                if st.form_submit_button("✅ Update & Save"):
                    df.at[st.session_state.edit_idx, 'Date'] = pd.to_datetime(e_date)
                    df.at[st.session_state.edit_idx, 'Category'] = e_cat
                    df.at[st.session_state.edit_idx, 'Item'] = e_item
                    df.at[st.session_state.edit_idx, 'Cost'] = e_cost
                    df.at[st.session_state.edit_idx, 'Sale'] = e_sale
                    df.at[st.session_state.edit_idx, 'Profit'] = (e_sale - e_cost) if e_cat != "Ghar ka Kharcha" else 0
                    df.at[st.session_state.edit_idx, 'Payment'] = e_pay
                    
                    if save_data(df, f"Updated: {e_item}"):
                        st.session_state.edit_mode = False
                        st.success("Record Updated!")
                        st.rerun()
    else: st.info("No data to manage.")
        
