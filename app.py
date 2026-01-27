import streamlit as st
import pandas as pd
from datetime import datetime
import os

# =============================
# APP CONFIG
# =============================
st.set_page_config(page_title="Ali Mobiles & Communication", layout="wide")

# =============================
# CSS
# =============================
st.markdown("""
<style>
.block-container { padding: 0.5rem; }

.big-tile {
    height: 140px;
    border-radius: 18px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: white;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0px 6px 12px rgba(0,0,0,0.25);
    transition: 0.2s;
}
.big-tile:hover {
    transform: translateY(-5px);
}

.bg-purple { background: linear-gradient(135deg,#4a148c,#7b1fa2); }
.bg-green { background: linear-gradient(135deg,#1b5e20,#2e7d32); }
.bg-blue { background: linear-gradient(135deg,#0d47a1,#1e88e5); }
.bg-red { background: linear-gradient(135deg,#b71c1c,#d32f2f); }
.bg-orange { background: linear-gradient(135deg,#e65100,#fb8c00); }
.bg-teal { background: linear-gradient(135deg,#006064,#00838f); }
.bg-pink { background: linear-gradient(135deg,#ad1457,#d81b60); }
.bg-slate { background: linear-gradient(135deg,#263238,#37474f); }

.tile-title { font-size: 15px; }
.tile-number { font-size: 34px; }
</style>
""", unsafe_allow_html=True)

# =============================
# DATA
# =============================
FILE = "ali_shop.csv"

def load_data():
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        df["تاریخ"] = pd.to_datetime(df["تاریخ"])
        return df
    return pd.DataFrame(columns=["تاریخ","کیٹیگری","تفصیل","خریداری","فروخت","منافع","اسٹیٹس"])

df = load_data()

if "page" not in st.session_state:
    st.session_state.page = "home"

today = datetime.now().date()
today_df = df[df["تاریخ"].dt.date == today]

profit = int(today_df[(today_df["اسٹیٹس"]=="نقد") & (today_df["کیٹیگری"]!="Home Expense")]["منافع"].sum())
repair = int(today_df[today_df["کیٹیگری"]=="Repairing"]["منافع"].sum())
expense = int(today_df[today_df["کیٹیگری"]=="Home Expense"]["فروخت"].sum())
bank = int(today_df[today_df["کیٹیگری"]=="Banking"]["فروخت"].sum())

# =============================
# TILE FUNCTION
# =============================
def tile(col, color, title, value, page):
    with col:
        if st.button(" ", key=page):
            st.session_state.page = page
            st.rerun()

        st.markdown(f"""
        <div class="big-tile {color}">
            <div class="tile-title">{title}</div>
            <div class="tile-number">{value}</div>
        </div>
        """, unsafe_allow_html=True)

# =============================
# DASHBOARD
# =============================
st.title("📱 Ali Mobiles & Communication")

c1,c2 = st.columns(2)
tile(c1,"bg-purple","نئی انٹری","➕","new")
tile(c2,"bg-green","کل نقد پرافٹ",profit,"profit")

c3,c4 = st.columns(2)
tile(c3,"bg-blue","ریپیرنگ پرافٹ",repair,"repair")
tile(c4,"bg-teal","ادھار لسٹ","📒","credit")

c5,c6 = st.columns(2)
tile(c5,"bg-orange","ایزی پیسہ سیل",bank,"bank")
tile(c6,"bg-pink","مکمل ہسٹری","📅","history")

c7,c8 = st.columns(2)
tile(c7,"bg-red","گھر کا خرچ",expense,"expense")
tile(c8,"bg-slate","ہوم پیج","🏠","home")

# =============================
# PAGES
# =============================
if st.session_state.page == "home":
    st.subheader("آج کا ریکارڈ")
    st.dataframe(today_df)

elif st.session_state.page == "new":
    st.subheader("نئی انٹری")
    with st.form("form"):
        cat = st.selectbox("کیٹیگری",["Accessories","Repairing","Banking","Home Expense"])
        det = st.text_input("تفصیل")
        cost = st.number_input("لاگت",0)
        sale = st.number_input("وصولی",0)
        status = st.radio("ادائیگی",["نقد","ادھار"])
        if st.form_submit_button("محفوظ کریں"):
            profit = 0 if cat=="Home Expense" else sale-cost
            df.loc[len(df)] = [datetime.now(),cat,det,cost,sale,profit,status]
            df.to_csv(FILE,index=False)
            st.success("محفوظ ہوگیا ✅")
            st.session_state.page="home"
            st.rerun()

elif st.session_state.page == "history":
    st.subheader("مکمل ہسٹری")
    st.dataframe(df)

elif st.session_state.page == "profit":
    st.subheader("کل نقد پرافٹ")
    st.dataframe(today_df)

elif st.session_state.page == "repair":
    st.subheader("ریپیرنگ پرافٹ")
    st.dataframe(today_df[today_df["کیٹیگری"]=="Repairing"])

elif st.session_state.page == "bank":
    st.subheader("ایزی پیسہ سیلز")
    st.dataframe(today_df[today_df["کیٹیگری"]=="Banking"])

elif st.session_state.page == "expense":
    st.subheader("گھر کا خرچ")
    st.dataframe(today_df[today_df["کیٹیگری"]=="Home Expense"])

elif st.session_state.page == "credit":
    st.subheader("ادھار لسٹ")
    st.dataframe(df[df["اسٹیٹس"]=="ادھار"])
