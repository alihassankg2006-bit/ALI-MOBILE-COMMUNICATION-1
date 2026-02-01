import streamlit as st
import pandas as pd
import plotly.express as px
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Ali Mobiles & Communication", page_icon="📱", layout="wide")

# --- Styling ---
st.markdown("""
    <style>
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #4e5d6c; }
    .target-card { background-color: #1e2130; padding: 20px; border-radius: 15px; text-align: center; border: 2px solid #00cc66; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- Data File Logic ---
CSV_FILE = "sales_record.csv"

def load_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    else:
        cols = ['Date', 'Category', 'Item', 'Cost', 'Sale', 'Profit', 'Payment']
        return pd.DataFrame(columns=cols)

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

def send_email_backup(to_email):
    # یہ حصہ ای میل بھیجنے کے لیے ہے
    from_email = st.secrets["MY_EMAIL"]  # اپنی ای میل یہاں سیٹ کریں
    password = st.secrets["EMAIL_PASSWORD"] # ای میل کا ایپ پاس ورڈ
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = f"Ali Mobiles - Sales Record Backup {datetime.now().strftime('%Y-%m-%d')}"
    
    body = "Assalam-o-Alaikum Ali Bhai! Attached is your business record file."
    msg.attach(MIMEText(body, 'plain'))
    
    attachment = open(CSV_FILE, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {CSV_FILE}")
    msg.attach(part)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Email error: {e}")
        return False

df = load_data()
now = datetime.now()

# --- Header ---
st.markdown("<h1 style='text-align: center; color: #00cc66;'>Ali Mobiles & Communication</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- Navigation ---
menu = st.sidebar.radio("Main Menu", ["📝 Nayi Entry", "📊 Dashboard", "📧 Email Backup"])

# --- 1. NEW ENTRY ---
if menu == "📝 Nayi Entry":
    st.header("Nayi Entry")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Tareekh", now)
            cat = st.selectbox("Category", ["Accessories", "Repairing"])
            item = st.text_input("Item Name")
        with col2:
            cost = st.number_input("Cost", min_value=0.0)
            sale = st.number_input("Sale", min_value=0.0)
            pay = st.selectbox("Payment", ["Cash", "EasyPaisa", "JazzCash"])
        
        if st.form_submit_button("💾 Save Locally"):
            if item and sale > 0:
                profit = sale - cost
                new_row = pd.DataFrame([[date.strftime('%Y-%m-%d'), cat, item, cost, sale, profit, pay]], columns=df.columns)
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df)
                st.success("✅ Record Saved!")
                st.rerun()

# --- 2. DASHBOARD ---
elif menu == "📊 Dashboard":
    if not df.empty:
        df_month = df[(df['Date'].dt.month == now.month) & (df['Date'].dt.year == now.year)]
        
        target_profit = 60000
        month_profit = df_month['Profit'].sum()
        progress = min(month_profit / target_profit, 1.0)
        
        st.markdown(f"""
            <div class="target-card">
                <h3 style='margin:0; color:#00cc66;'>🎯 Monthly Profit Target ({now.strftime('%B')})</h3>
                <h1 style='margin:10px 0;'>Rs. {month_profit:,.0f} / {target_profit:,}</h1>
            </div>
            """, unsafe_allow_html=True)
        st.progress(progress)
        
        m1, m2 = st.columns(2)
        m1.metric("Is Mahine Ki Sale", f"Rs. {df_month['Sale'].sum():,.0f}")
        m2.metric("Total Profit", f"Rs. {month_profit:,.0f}")
        
        st.subheader("Records List")
        st.dataframe(df_month.sort_values(by='Date', ascending=False), use_container_width=True)
    else:
        st.info("Abhi tak koi entry nahi hui.")

# --- 3. EMAIL BACKUP ---
elif menu == "📧 Email Backup":
    st.header("📧 Data Backup")
    st.write("Apna sara record file ki surat mein apni Email par mangwaein.")
    
    target_mail = st.text_input("Apni Email Address likhein:")
    if st.button("🚀 Send Record to My Email"):
        if target_mail:
            with st.spinner("Bheja ja raha hai..."):
                if send_email_backup(target_mail):
                    st.success(f"✅ Record successfully sent to {target_mail}!")
                else:
                    st.error("❌ Email nahi bheji ja saki. Secrets check karein.")
        else:
            st.warning("Pehle email address likhein.")

    st.markdown("---")
    # Manual Download Option
    with open(CSV_FILE, "rb") as file:
        st.download_button(
            label="📥 Download CSV File (Manual)",
            data=file,
            file_name="ali_mobiles_record.csv",
            mime="text/csv"
        )
