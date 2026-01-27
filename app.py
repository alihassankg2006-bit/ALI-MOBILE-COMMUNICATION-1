import streamlit as st
import pandas as pd
import plotly.express as px
from github import Github
from datetime import datetime
import io

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Ali Mobiles | Pro Manager",
    page_icon="📱",
    layout="wide"
)

# =========================
# CSS DESIGN
# =========================
st.markdown("""
<style>
.big-tile {
    height: 140px;
    border-radius: 18px;
    padding: 15px;
    text-align: center;
    color: white;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 6px 15px rgba(0,0,0,.3);
    transition: 0.2s;
}
.big-tile:hover {
    transform: translateY(-6px);
}

.bg1 {background: linear-gradient(135deg,#4a148c,#7b1fa2);}
.bg2 {background: linear-gradient(135deg,#1b5e20,#2e7d32);}
.bg3 {background: linear-gradient(135deg,#0d47a1,#1e88e5);}
.bg4 {background: linear-gradient(135deg,#b71c1c,#d32f2f);}
.bg5 {background: linear-gradient(135deg,#e65100,#fb8c00);}
.bg6 {background: linear-gradient(135deg,#006064,#00838f);}
.bg7 {background: linear-gradient(135deg,#ad1457,#d81b60);}
.bg8 {background: linear-gradient(135deg,#263238,#37474f);}

.tile-title {font-size:16px;}
.tile-value {font-size:34px;}
</style>
""", unsafe_allow_html=True)

# =========================
# GITHUB CONNECTION
# =========================
token = st.secrets["GITHUB_TOKEN"]
repo_name = st.secrets["REPO_NAME"]

g = Github(token)
repo = g.get_repo(repo_name)
FILE = "shop_data.csv"

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
# SESSION
# =========================
if "page" not in st.session_state:
    st.session_state.page = "home"

# =========================
# TILE FUNCTION
# =========================
def tile(col, color, title, value, page):
    with col:
        if st.button(" ", key=page):
            st.session_state.page = page
            st.rerun()

        st.markdown(f"""
        <div class="big-tile {color}">
            <div class="tile-title">{title}</div>
            <div class="tile-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("<h1 style='text-align:center'>📱 Ali Mobiles & Communication</h1>", unsafe_allow_html=True)

# =========================
# CALCULATIONS
# =========================
today = datetime.now().date()
today_df = df[df["Date"].dt.date == today]

profit = int(today_df[today_df["Category"]!="Home Expense"]["Profit"].sum())
repair = int(today_df[today_df["Category"]=="Repairing"]["Profit"].sum())
bank = int(today_df[today_df["Category"]=="Banking"]["Sale"].sum())
expense = int(today_df[today_df["Category"]=="Home Expense"]["Sale"].sum())

# =========================
# DASHBOARD
# =========================
c1,c2 = st.columns(2)
tile(c1,"bg1","نئی انٹری","➕","new")
tile(c2,"bg2","کل پرافٹ",profit,"profit")

c3,c4 = st.columns(2)
tile(c3,"bg3","ریپیرنگ",repair,"repair")
tile(c4,"bg6","ایزی پیسہ",bank,"bank")

c5,c6 = st.columns(2)
tile(c5,"bg4","گھر خرچ",expense,"expense")
tile(c6,"bg7","مکمل ہسٹری","📊","history")

# =========================
# PAGES
# =========================
if st.session_state.page == "new":
    st.subheader("📝 New Entry")
    with st.form("f"):
        cat = st.selectbox("Category",["Accessories","Repairing","Banking","Home Expense"])
        item = st.text_input("Detail")
        cost = st.number_input("Cost",0)
        sale = st.number_input("Sale",0)
        pay = st.selectbox("Payment",["Cash","EasyPaisa","JazzCash"])

        if st.form_submit_button("Save"):
            profit = 0 if cat=="Home Expense" else sale-cost
            df.loc[len(df)] = [datetime.now(),cat,item,cost,sale,profit,pay]
            save_data(df,sha)
            st.success("Saved!")
            st.session_state.page="home"
            st.rerun()

elif st.session_state.page == "history":
    st.subheader("📜 Full History")
    st.dataframe(df)

elif st.session_state.page == "profit":
    st.subheader("💰 Profit Report")
    st.dataframe(today_df)

elif st.session_state.page == "repair":
    st.subheader("🔧 Repair Profit")
    st.dataframe(today_df[today_df["Category"]=="Repairing"])

elif st.session_state.page == "bank":
    st.subheader("💳 EasyPaisa Sales")
    st.dataframe(today_df[today_df["Category"]=="Banking"])

elif st.session_state.page == "expense":
    st.subheader("🏠 Home Expense")
    st.dataframe(today_df[today_df["Category"]=="Home Expense"])
