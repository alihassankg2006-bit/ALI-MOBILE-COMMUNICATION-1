import streamlit as st
import pandas as pd
from datetime import datetime
import os
from github import Github
import io

# =========================
# 1. PAGE CONFIG & UI THEME
# =========================
st.set_page_config(page_title="Ali Mobiles | Pro", layout="wide")

st.markdown("""
<style>
    /* فالتو جگہ ختم */
    .block-container { padding: 0.5rem 0.5rem !important; }
    
    /* بٹنوں کو رنگین ٹائلز بنانا */
    div.stButton > button {
        height: 100px !important;
        width: 100% !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 14px !important;
        border: none !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        margin-bottom: 5px !important;
        white-space: pre-wrap !important;
        line-height: 1.2 !important;
        transition: 0.2s;
    }
    div.stButton > button:hover { transform: translateY(-3px); opacity: 0.9; }

    /* 8 مخصوص گہرے رنگ */
    button[key="new"] { background: linear-gradient(135deg, #4a148c, #7b1fa2) !important; }
    button[key="profit"] { background: linear-gradient(135deg, #1b5e20, #2e7d32) !important; }
    button[key="repair"] { background: linear-gradient(135deg, #0d47a1, #1e88e5) !important; }
    button[key="bank"] { background: linear-gradient(135deg, #006064, #00838f) !important; }
    button[key="expense"] { background: linear-gradient(135deg, #b71c1c, #d32f2f) !important; }
    button[key="credit"] { background: linear-gradient(135deg, #e65100, #fb8c00) !important; }
    button[key="history"] { background: linear-gradient(135deg, #ad1457, #d81b60) !important; }
    button[key="home"] { background: linear-gradient(135deg, #263238, #37474f) !important; }
</style>
""", unsafe_allow_html=True)

# =========================
# 2. GITHUB DATA CONNECTION
# =========================
# نوٹ: یہ ٹوکن اور ریپو نیم آپ کے Streamlit Secrets میں ہونے چاہئیں
token = st.secrets["GITHUB_TOKEN"]
repo_name = st.secrets["REPO_NAME"]
FILE = "shop_data.csv"

g = Github(token)
repo = g.get_repo(repo_name)

def load_data():
    try:
        file = repo.get_contents(FILE)
        df = pd.read_csv(io.StringIO(file.decoded_content.decode()))
        df["Date"] = pd.to_datetime(df["Date"])
        return df, file.sha
    except:
        return pd.DataFrame(columns=["Date","Category","Item","Cost","Sale","Profit","Payment"]), None

def save_data(df, sha):
    csv = io.StringIO()
    df.to_csv(csv, index=False)
    if sha:
        repo.update_file(FILE, "Update Data", csv.getvalue(), sha)
    else:
        repo.create_file(FILE, "Initial Data", csv.getvalue())

df, sha = load_data()

# =========================
# 3. SIDEBAR (REBOOT & SETTINGS)
# =========================
with st.sidebar:
    st.header("⚙️ سسٹم مینیو")
    if st.button("🚨 REBOOT (Clear All Data)"):
        # ڈیٹا ری سیٹ کرنے کے لیے خالی ڈیٹا فریم سیو کریں
        empty_df = pd.DataFrame(columns=["Date","Category","Item","Cost","Sale","Profit","Payment"])
        save_data(empty_df, sha)
        st.warning("سارا ڈیٹا صاف ہو گیا!")
        st.rerun()

# =========================
# 4. CALCULATIONS
# =========================
today = datetime.now().date()
t_df = df[df["Date"].dt.date == today] if not df.empty else df

profit_val = int(t_df[t_df["Category"]!="Home Expense"]["Profit"].sum())
repair_val = int(t_df[t_df["Category"]=="Repairing"]["Profit"].sum())
bank_val = int(t_df[t_df["Category"]=="Banking"]["Sale"].sum())
exp_val = int(t_df[t_df["Category"]=="Home Expense"]["Sale"].sum())

# =========================
# 5. DASHBOARD (4x2 GRID - NO SCROLL)
# =========================
if "page" not in st.session_state: st.session_state.page = "home"
def nav(p):
    st.session_state.page = p
    st.rerun()

# لوگو (اگر موجود ہو)
col_l, col_m, col_r = st.columns([1, 0.5, 1])
with col_m:
    if os.path.exists("logo.png"): st.image("logo.png")
    else: st.markdown("<h3 style='text-align:center'>ALI MOBILES</h3>", unsafe_allow_html=True)

# پہلی لائن (4 ڈبے)
r1c1, r1c2, r1c3, r1c4 = st.columns(4)
with r1c1:
    if st.button(f"➕\nENTRY", key="new"): nav("new")
with r1c2:
    if st.button(f"💰\nپرافٹ\n{profit_val}", key="profit"): nav("profit")
with r1c3:
    if st.button(f"🔧\nریپیرنگ\n{repair_val}", key="repair"): nav("repair")
with r1c4:
    if st.button(f"💳\nبینکنگ\n{bank_val}", key="bank"): nav("bank")

# دوسری لائن (4 ڈبے)
r2c1, r2c2, r2c3, r2c4 = st.columns(4)
with r2c1:
    if st.button(f"🏠\nخرچہ\n{exp_val}", key="expense"): nav("expense")
with r2c2:
    if st.button(f"📓\nادھار", key="credit"): nav("credit")
with r2c3:
    if st.button(f"📊\nہسٹری", key="history"): nav("history")
with r2c4:
    if st.button(f"🏠\nHOME", key="home"): nav("home")

st.markdown("---")

# =========================
# 6. PAGES LOGIC
# =========================
if st.session_state.page == "new":
    st.subheader("📝 نئی انٹری درج کریں")
    with st.form("f", clear_on_submit=True):
        cat = st.selectbox("Category", ["Accessories", "Repairing", "Banking", "Home Expense"])
        item = st.text_input("Detail")
        pay = st.selectbox("Payment", ["Cash", "EasyPaisa", "JazzCash"])
        c1, c2 = st.columns(2)
        cost = c1.number_input("Cost", 0)
        sale = c2.number_input("Sale", 0)
        
        if st.form_submit_button("Save Record"):
            p = 0 if cat == "Home Expense" else (sale - cost)
            new_row = [datetime.now(), cat, item, cost, sale, p, pay]
            df.loc[len(df)] = new_row
            save_data(df, sha)
            st.success("محفوظ ہو گیا!")
            nav("home")

elif st.session_state.page == "history":
    st.subheader("📜 مکمل ریکارڈ")
    st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)

elif st.session_state.page == "credit":
    st.subheader("📓 ادھار لسٹ")
    # فرض کریں EasyPaisa کے علاوہ ادھار کا آپشن بھی ہو سکتا ہے، فی الحال ہسٹری دکھا رہا ہے
    st.info("یہاں آپ اپنا کسٹم ادھار ڈیٹا فلٹر کر سکتے ہیں۔")
    st.dataframe(df, use_container_width=True)

elif st.session_state.page == "home":
    st.subheader("📅 آج کی سیل")
    st.dataframe(t_df, use_container_width=True)

# باقی تمام تفصیلی پیجز (اگر ضرورت ہو)
elif st.session_state.page in ["profit", "repair", "bank", "expense"]:
    st.subheader(f"📊 {st.session_state.page.upper()} رپورٹ")
    st.dataframe(t_df, use_container_width=True)
