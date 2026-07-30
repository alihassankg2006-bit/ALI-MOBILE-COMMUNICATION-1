# -*- coding: utf-8 -*-
"""
Ali Mobiles & Communication - Super POS System with GitHub Persistence & Animations
Run: streamlit run app.py
"""

from datetime import datetime
import io
import urllib.parse
from github import Github
import pandas as pd
import pytz
import streamlit as st

# ============================================================
# PAGE CONFIG & THEME
# ============================================================
st.set_page_config(
    page_title="Ali Mobiles & Communication",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PROFESSIONAL CSS & ANIMATIONS
# ============================================================
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

    body, .stTextInput, .stNumberInput, .stSelectbox, .stDateInput, .stTextArea, div[data-testid="stMetricValue"] {
        font-family: 'Roboto', sans-serif;
    }

    @keyframes screenTransition {
        0% { background-color: #000000; }
        50% { background-color: #111111; }
        100% { background-color: #f8f9fa; }
    }

    .stApp {
        animation: screenTransition 2.5s ease-in-out;
    }

    @keyframes floatMobiles {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(8deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }

    .floating-bg-img {
        position: fixed;
        width: 100px;
        opacity: 0.08;
        animation: floatMobiles 5s infinite ease-in-out;
        z-index: 1;
        pointer-events: none;
    }

    section[data-testid="stSidebar"] > div {
        background-color: #1e2a38;
        color: white;
        padding-top: 20px;
    }
    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background-color: transparent;
        color: #b0bec5;
        border: none;
        text-align: left;
        font-weight: 500;
        padding: 10px 20px;
        margin-bottom: 5px;
        border-radius: 4px;
        transition: all 0.3s;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #37474f;
        color: white;
    }
    .sidebar-header {
        padding: 0 20px 20px 20px;
        border-bottom: 1px solid #37474f;
        margin-bottom: 20px;
        text-align: center;
    }
    .sidebar-header h3 { color: white; margin: 0; }
    .sidebar-header p { color: #b0bec5; margin: 5px 0 0 0; font-size: 0.9em; }

    h1, h2, h3 { color: #37474f; }
    .main-header {
        background: linear-gradient(135deg, #0a1a3a 0%, #1e3a6e 55%, #3a1e6e 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        border: 2px solid #f5d67e;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-header h1 { color: #f5d67e; margin: 0; font-size: 36px; }
    .main-header p { color: #ffffff; margin: 5px 0 0 0; }

    div[data-testid="stMetricValue"] {
        color: #1e3a6e;
        font-weight: 800 !important;
    }
</style>

<img src="https://img.icons8.com/ios-filled/500/iphone.png" class="floating-bg-img" style="top: 15%; left: 3%;">
<img src="https://img.icons8.com/ios-filled/500/smartphone.png" class="floating-bg-img" style="top: 60%; right: 5%;">
<img src="https://img.icons8.com/ios-filled/500/phone.png" class="floating-bg-img" style="top: 35%; right: 8%;">
""",
    unsafe_allow_html=True,
)

# ============================================================
# GITHUB AUTH & STORAGE LAYER
# ============================================================
try:
  token = st.secrets["GITHUB_TOKEN"]
  repo_name = st.secrets["REPO_NAME"]
  g = Github(token)
  repo = g.get_repo(repo_name)
except Exception as e:
  st.error(f"GitHub Secrets Missing! Error: {e}")
  st.stop()


def get_logo():
  for name in ["logo.png", "Logo.png", "logo.jpg", "Logo.jpg"]:
    try:
      return repo.get_contents(name).download_url
    except:
      continue
  return None


# Master Data Schema for GitHub CSV Storage (Total 14 Columns)
DB_FILE = "ali_mobiles_master_data.csv"
COLUMNS = [
    "id",
    "module",
    "col1",
    "col2",
    "col3",
    "col4",
    "col5",
    "col6",
    "col7",
    "col8",
    "col9",
    "col10",
    "col11",
    "timestamp",
]

INITIAL_MOBILES = [
    [
        1,
        "Mobile",
        "زبیر مردان",
        "N/A",
        "N/A",
        "Google Pixel 7 Pro",
        "بلیک، 12GB/128GB",
        "Available",
        "N/A",
        "N/A",
        "Used",
        "48000",
        "48000",
        "2026-06-01 12:00",
    ],
    [
        2,
        "Mobile",
        "زبیر مردان",
        "N/A",
        "N/A",
        "Google Pixel 7 Pro",
        "وائٹ، Non-PTA، CPID Approved",
        "Available",
        "N/A",
        "N/A",
        "Used",
        "42000",
        "42000",
        "2026-06-01 12:00",
    ],
    [
        3,
        "Mobile",
        "زبیر مردان",
        "N/A",
        "N/A",
        "iPhone 8 Plus",
        "گولڈ، 256GB",
        "Available",
        "N/A",
        "N/A",
        "Used",
        "20000",
        "20000",
        "2026-06-01 12:00",
    ],
    [
        4,
        "Mobile",
        "زبیر مردان",
        "N/A",
        "N/A",
        "iPhone 8 Plus",
        "گولڈ، 64GB",
        "Available",
        "N/A",
        "N/A",
        "Used",
        "7000",
        "7000",
        "2026-06-01 12:00",
    ],
    [
        5,
        "Mobile",
        "زبیر مردان",
        "N/A",
        "N/A",
        "iPhone XR",
        "Converted to iPhone 17",
        "Available",
        "N/A",
        "N/A",
        "Used",
        "25000",
        "25000",
        "2026-06-01 12:00",
    ],
    [
        6,
        "Mobile",
        "زبیر مردان",
        "N/A",
        "N/A",
        "iPhone 7 Plus",
        "—",
        "Available",
        "N/A",
        "N/A",
        "Used",
        "13500",
        "13500",
        "2026-06-01 12:00",
    ],
    [
        7,
        "Mobile",
        "زبیر مردان",
        "N/A",
        "N/A",
        "iPhone XR",
        "بلیک، 256GB",
        "Available",
        "N/A",
        "N/A",
        "Used",
        "22000",
        "22000",
        "2026-06-01 12:00",
    ],
    [
        8,
        "Mobile",
        "زبیر مردان",
        "N/A",
        "N/A",
        "Vivo V20",
        "صاف کنڈیشن",
        "Available",
        "N/A",
        "N/A",
        "Used",
        "10000",
        "10000",
        "2026-06-01 12:00",
    ],
    [
        9,
        "Mobile",
        "زبیر مردان",
        "N/A",
        "N/A",
        "Tecno Spark Go",
        "2024",
        "Available",
        "N/A",
        "N/A",
        "New",
        "13500",
        "13500",
        "2026-06-01 12:00",
    ],
    [
        10,
        "Mobile",
        "زبیر مردان",
        "N/A",
        "N/A",
        "Realme C21",
        "—",
        "Available",
        "N/A",
        "N/A",
        "Used",
        "13500",
        "13500",
        "2026-06-01 12:00",
    ],
    [
        11,
        "Mobile",
        "زبیر مردان",
        "N/A",
        "N/A",
        "Vivo V12",
        "—",
        "Available",
        "N/A",
        "N/A",
        "Used",
        "5000",
        "5000",
        "2026-06-01 12:00",
    ],
]


def load_db():
  try:
    contents = repo.get_contents(DB_FILE)
    df = pd.read_csv(io.StringIO(contents.decoded_content.decode("utf-8")))
    if df.empty or len(df.columns) != len(COLUMNS):
      df = pd.DataFrame(INITIAL_MOBILES, columns=COLUMNS)
      save_db(df, "Initialized with default mobiles")
    return df
  except Exception:
    df = pd.DataFrame(INITIAL_MOBILES, columns=COLUMNS)
    save_db(df, "Initial POS Data with default mobiles")
    return df


def save_db(df, message="Update POS Data"):
  csv_buffer = io.StringIO()
  df.to_csv(csv_buffer, index=False)
  try:
    contents = repo.get_contents(DB_FILE)
    repo.update_file(DB_FILE, message, csv_buffer.getvalue(), contents.sha)
    return True
  except Exception:
    try:
      repo.create_file(DB_FILE, "Initial POS Data", csv_buffer.getvalue())
      return True
    except:
      return False


pk_tz = pytz.timezone("Asia/Karachi")


def get_formatted_date():
  return datetime.now(pk_tz).strftime("%Y-%m-%d %H:%M")


def get_current_date():
  return datetime.now(pk_tz).strftime("%Y-%m-%d")


def get_current_year_month():
  return datetime.now(pk_tz).strftime("%Y-%m")


def send_whatsapp_link(phone, message):
  if not phone:
    return
  clean_phone = "".join(filter(str.isdigit, phone))
  if clean_phone.startswith("0"):
    clean_phone = "92" + clean_phone[1:]
  encoded_msg = urllib.parse.quote(message)
  wa_url = f"https://wa.me/{clean_phone}?text={encoded_msg}"
  st.markdown(
      f"""
        <a href="{wa_url}" target="_blank">
            <button style="background-color: #25D366; color: white; padding: 10px 20px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 10px;">
                📱 Send Receipt on WhatsApp
            </button>
        </a>
    """,
      unsafe_allow_html=True,
  )


if "df_master" not in st.session_state:
  st.session_state.df_master = load_db()

df_master = st.session_state.df_master
logo_url = get_logo()

# ============================================================
# SIDEBAR NAVIGATION & LOGO
# ============================================================
with st.sidebar:
  if logo_url:
    st.image(logo_url, use_container_width=True)
  else:
    st.markdown(
        """
        <div class="sidebar-header">
            <h3>Ali Hassan</h3>
            <p>Shamsabad, Rawalpindi<br>📞 0302-9401314</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if "current_page" not in st.session_state:
  st.session_state.current_page = "Dashboard"

nav_options = {
    "Dashboard": "📊 Dashboard & Profits",
    "CashDrawer": "💵 Cash Drawer (Open/Close)",
    "Udhar": "📒 Udhar Khata (ادھار کھاتا)",
    "Mobile Sales": "📱 Mobile Buy & Sell",
    "Accessories": "🎧 Accessories",
    "Repair": "🛠️ Repair Khata",
    "EasyPaisa": "💰 EasyPaisa / JazzCash",
    "Expenses": "💸 Expenses & Home",
    "History": "📜 Unified Activity History",
    "Reports": "📈 Monthly & Yearly Reports",
    "Inventory": "📦 Inventory",
}

for page_key, page_label in nav_options.items():
  if st.sidebar.button(page_label):
    st.session_state.current_page = page_key

page = st.session_state.current_page

st.markdown(
    """
<div class="main-header">
    <h1>📱 ALI MOBILES & COMMUNICATION</h1>
    <p>Professional Mobile Shop & EasyPaisa Management System (Cloud Protected)</p>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# 1. DASHBOARD PAGE
# ============================================================
if page == "Dashboard":
  st.subheader("📊 Business Performance & Profit Summary")

  curr_date = get_current_date()
  curr_ym = get_current_year_month()


  def get_module_df(mod_name):
    if df_master.empty:
      return pd.DataFrame()
    return df_master[df_master["module"] == mod_name]


  mob_df = get_module_df("Mobile")
  tod_mob, m_mob = 0, 0
  if not mob_df.empty:
    sold_mob = mob_df[mob_df["col7"] == "Sold"]
    for _, r in sold_mob.iterrows():
      prof = float(r["col11"] or 0) - float(r["col10"] or 0)
      s_date = str(r["timestamp"])
      if curr_date in s_date:
        tod_mob += prof
      if curr_ym in s_date:
        m_mob += prof

  rep_df = get_module_df("Repair")
  tod_rep, m_rep = 0, 0
  if not rep_df.empty:
    for _, r in rep_df.iterrows():
      prof = float(r["col8"] or 0)
      c_date = str(r["timestamp"])
      if curr_date in c_date:
        tod_rep += prof
      if curr_ym in c_date:
        m_rep += prof

  acc_df = get_module_df("AccessorySale")
  tod_acc, m_acc = 0, 0
  if not acc_df.empty:
    for _, r in acc_df.iterrows():
      prof = float(r["col6"] or 0)
      s_date = str(r["timestamp"])
      if curr_date in s_date:
        tod_acc += prof
      if curr_ym in s_date:
        m_acc += prof

  txn_df = get_module_df("Transaction")
  tod_ep, m_ep = 0, 0
  tod_shop_exp, m_shop_exp = 0, 0
  if not txn_df.empty:
    for _, r in txn_df.iterrows():
      ttype = str(r["col2"])
      prof = float(r["col4"] or 0)
      amt = float(r["col3"] or 0)
      e_date = str(r["timestamp"])
      if "EasyPaisa" in ttype or "JazzCash" in ttype:
        if curr_date in e_date:
          tod_ep += prof
        if curr_ym in e_date:
          m_ep += prof
      elif ttype == "ShopExpense":
        if curr_date in e_date:
          tod_shop_exp += amt
        if curr_ym in e_date:
          m_shop_exp += amt

  todays_total_profit = (tod_mob + tod_rep + tod_acc + tod_ep) - tod_shop_exp
  monthly_total_profit = (m_mob + m_rep + m_acc + m_ep) - m_shop_exp

  st.markdown("### 🌟 Total Profits Overview")
  t_col1, t_col2 = st.columns(2)
  t_col1.metric(
      "📅 Today's Total Profit (آج کا کل پرافٹ)",
      f"PKR {todays_total_profit:,.0f}",
  )
  t_col2.metric(
      "🗓️ This Month's Total Profit (اس ماہ کا کل پرافٹ)",
      f"PKR {monthly_total_profit:,.0f}",
  )

  st.markdown("---")
  filter_mode = st.radio(
      "Select Breakdown View Mode:",
      ["Current Month", "All Time Records"],
      horizontal=True,
  )

  if "Current Month" in filter_mode:
    mobile_profit, repair_profit, acc_profit, ep_profit = m_mob, m_rep, m_acc, m_ep
    shop_expenses = m_shop_exp
    home_expenses = 0
    if not txn_df.empty:
      home_expenses = (
          txn_df[
              (txn_df["col2"] == "HomeExpense")
              & (txn_df["timestamp"].str.contains(curr_ym, na=False))
          ]["col3"]
          .astype(float)
          .sum()
      )
  else:
    mobile_profit = 0
    if not mob_df.empty:
      sold_all = mob_df[mob_df["col7"] == "Sold"]
      for _, r in sold_all.iterrows():
        mobile_profit += float(r["col11"] or 0) - float(r["col10"] or 0)
    repair_profit = (
        rep_df["col8"].astype(float).sum() if not rep_df.empty else 0
    )
    acc_profit = acc_df["col6"].astype(float).sum() if not acc_df.empty else 0
    ep_profit = 0
    if not txn_df.empty:
      ep_profit = (
          txn_df[
              txn_df["col2"].isin([
                  "EasyPaisaSend",
                  "EasyPaisaReceive",
                  "JazzCashSend",
                  "JazzCashReceive",
              ])
          ]["col4"]
          .astype(float)
          .sum()
      )
      shop_expenses = (
          txn_df[txn_df["col2"] == "ShopExpense"]["col3"].astype(float).sum()
      )
      home_expenses = (
          txn_df[txn_df["col2"] == "HomeExpense"]["col3"].astype(float).sum()
      )
    else:
      shop_expenses, home_expenses = 0, 0

  net_profit = (
      mobile_profit + repair_profit + acc_profit + ep_profit
  ) - shop_expenses

  st.markdown("##### Category-wise Breakdown")
  col1, col2, col3, col4 = st.columns(4)
  col1.metric("Mobile Sales Profit", f"PKR {mobile_profit:,.0f}")
  col2.metric("Repair Profit", f"PKR {repair_profit:,.0f}")
  col3.metric("Accessories Profit", f"PKR {acc_profit:,.0f}")
  col4.metric("EasyPaisa Commission", f"PKR {ep_profit:,.0f}")

  st.markdown("---")
  col5, col6, col7, col8 = st.columns(4)
  col5.metric("Net Profit", f"PKR {net_profit:,.0f}")
  col6.metric("Shop Expenses", f"PKR {shop_expenses:,.0f}")
  col7.metric("Home Expenses", f"PKR {home_expenses:,.0f}")

  stock_val = 0
  if not mob_df.empty:
    avail_mobs = mob_df[mob_df["col7"] == "Available"]
    stock_val = (
        avail_mobs["col10"]
        .apply(
            lambda x: float(x)
            if pd.notna(x) and str(x).replace(".", "", 1).isdigit()
            else 0.0
        )
        .sum()
    )
  col8.metric("Available Stock Value", f"PKR {stock_val:,.0f}")

# ============================================================
# CASH DRAWER PAGE
# ============================================================
elif page == "CashDrawer":
  st.subheader("💵 Daily Cash Drawer (Morning & Night Calculation)")
  today_date = get_current_date()
  drawer_df = (
      df_master[
          (df_master["module"] == "CashDrawer")
          & (df_master["col1"] == today_date)
      ]
      if not df_master.empty
      else pd.DataFrame()
  )

  with st.form("cash_drawer_form"):
    st.write(f"### Date: {today_date}")
    default_open = (
        float(drawer_df.iloc[0]["col2"]) if not drawer_df.empty else 0.0
    )
    default_close = (
        float(drawer_df.iloc[0]["col3"]) if not drawer_df.empty else 0.0
    )

    c1, c2 = st.columns(2)
    opening_cash = c1.number_input(
        "Morning Opening Cash (صبح کا کیش)",
        min_value=0.0,
        step=100.0,
        value=default_open,
    )
    closing_cash = c2.number_input(
        "Night Closing Cash (رات کا کیش)",
        min_value=0.0,
        step=100.0,
        value=default_close,
    )

    if st.form_submit_button(
        "Save Cash Drawer Record", use_container_width=True
    ):
      if not drawer_df.empty:
        idx = drawer_df.index[0]
        st.session_state.df_master.loc[
            idx, ["col2", "col3", "timestamp"]
        ] = [str(opening_cash), str(closing_cash), get_formatted_date()]
      else:
        new_id = (
            int(st.session_state.df_master["id"].max() + 1)
            if not st.session_state.df_master.empty
            else 1
        )
        new_row = pd.DataFrame(
            [[
                new_id,
                "CashDrawer",
                today_date,
                str(opening_cash),
                str(closing_cash),
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                get_formatted_date(),
            ]],
            columns=COLUMNS,
        )
        st.session_state.df_master = pd.concat(
            [st.session_state.df_master, new_row], ignore_index=True
        )

      if save_db(st.session_state.df_master, "Updated Cash Drawer"):
        st.success("Cash Drawer record saved successfully to GitHub!")
        st.rerun()

# ============================================================
# UDHAR KHATA PAGE
# ============================================================
elif page == "Udhar":
  st.subheader("📒 Udhar Khata (کسٹمرز کا ادھار کھاتا)")
  with st.form("udhar_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    u_name = c1.text_input("Customer Name (کسٹمر کا نام) *")
    u_phone = c2.text_input("Customer Mobile Number (موبایل نمبر) *")

    c3, c4, c5 = st.columns(3)
    u_item = c3.text_input("Item / Cash Details *")
    u_amount = c4.number_input(
        "Total Amount (کل رقم - PKR) *", min_value=0.0, step=50.0
    )
    u_ret_date = c5.date_input("Promised Return Date")

    if st.form_submit_button(
        "Save Udhar & Generate WhatsApp Receipt", use_container_width=True
    ):
      if not u_name or not u_phone or not u_item or u_amount <= 0:
        st.error("برائے مہربانی تمام لازمی خانے پر کریں اور رقم درج کریں۔")
      else:
        new_id = (
            int(st.session_state.df_master["id"].max() + 1)
            if not st.session_state.df_master.empty
            else 1
        )
        new_row = pd.DataFrame(
            [[
                new_id,
                "Udhar",
                u_name,
                u_phone,
                u_item,
                str(u_amount),
                str(u_ret_date),
                "Pending",
                "",
                "",
                "",
                "",
                "",
                get_formatted_date(),
            ]],
            columns=COLUMNS,
        )
        st.session_state.df_master = pd.concat(
            [st.session_state.df_master, new_row], ignore_index=True
        )
        if save_db(st.session_state.df_master, f"Added Udhar: {u_name}"):
          st.success("ادھار کامیابی سے محفوظ ہو گیا ہے!")
          whatsapp_msg = (
              f"*ALI MOBILES & COMMUNICATION - UDHAR RECEIPT*\n\n"
              f"محترم کسٹمر: {u_name}\nآپ نے ادھار لیا ہے:\n🔹 تفصیل:"
              f" {u_item}\n🔹 کل رقم: PKR {u_amount:,.0f}\n🔹 واپسی کی تاریخ:"
              f" {u_ret_date}\n\nشکریہ!"
          )
          send_whatsapp_link(u_phone, whatsapp_msg)

  st.markdown("---")
  st.markdown("##### 📌 Pending Udhar Records (بقایا ادھار لسٹ)")
  udhar_df = (
      st.session_state.df_master[
          (st.session_state.df_master["module"] == "Udhar")
          & (st.session_state.df_master["col8"] == "Pending")
      ]
      if not st.session_state.df_master.empty
      else pd.DataFrame()
  )
  if not udhar_df.empty:
    for idx, u_row in udhar_df.iterrows():
      with st.container(border=True):
        col_u1, col_u2, col_u3 = st.columns([2.5, 2, 1.5])
        col_u1.markdown(
            f"**{u_row['col1']}** ({u_row['col2']})<br>Item: {u_row['col3']}",
            unsafe_allow_html=True,
        )
        col_u2.markdown(
            f"Amount: **PKR {float(u_row['col4']):,.0f}**<br>Return Date:"
            f" {u_row['col5']}",
            unsafe_allow_html=True,
        )
        with col_u3:
          if st.button("Mark Paid ✅", key=f"paid_udhar_{u_row['id']}"):
            st.session_state.df_master.loc[idx, "col8"] = "Paid"
            save_db(st.session_state.df_master, "Marked Udhar Paid")
            st.success("ادھار کلیئر ہو گیا!")
            st.rerun()
          if st.button("Delete ❌", key=f"del_udhar_{u_row['id']}"):
            st.session_state.df_master = st.session_state.df_master.drop(idx)
            save_db(st.session_state.df_master, "Deleted Udhar")
            st.rerun()
  else:
    st.info("کوئی بقایا ادھار موجود نہیں۔")

# ============================================================
# MOBILE SALES PAGE
# ============================================================
elif page == "Mobile Sales":
  st.subheader("📱 Mobile Purchase & Sale Management")
  mob_df = (
      st.session_state.df_master[
          st.session_state.df_master["module"] == "Mobile"
      ]
      if not st.session_state.df_master.empty
      else pd.DataFrame()
  )

  tab1, tab2, tab3 = st.tabs([
      "➕ Buy New Mobile",
      "💵 Sell Available Mobile",
      "⚙️ Edit / Delete Entries",
  ])

  with tab1:
    with st.form("purchase_mob_form", clear_on_submit=True):
      c1, c2, c3 = st.columns(3)
      c_name = c1.text_input("Customer / Seller Name (مالک کا نام)")
      c_phone = c2.text_input("Mobile Number")
      c_cnic = c3.text_input("Seller CNIC (آئی ڈی کارڈ نمبر)")

      c4, c5, c6 = st.columns(3)
      brand = c4.text_input("Brand *")
      model = c5.text_input("Color / Variant (کلر / ویریئنٹ) *")
      imei = c6.text_input("IMEI Number")

      c7, c8, c9 = st.columns(3)
      condition = c7.selectbox("Condition", ["Used", "New"])
      p_price = c8.number_input("Purchase Price (خرید قیمت) *", min_value=0.0, step=100.0)

      if st.form_submit_button("Save to Stock", use_container_width=True):
        if not brand or not model or p_price <= 0:
          st.error("برائے مہربانی برانڈ، ماڈل اور قیمت درج کریں۔")
        else:
          new_id = (
              int(st.session_state.df_master["id"].max() + 1)
              if not st.session_state.df_master.empty
              else 1
          )
          new_row = pd.DataFrame(
              [[
                  new_id,
                  "Mobile",
                  c_name,
                  c_phone,
                  c_cnic,
                  brand,
                  model,
                  "Available",
                  "N/A",
                  "N/A",
                  condition,
                  str(p_price),
                  str(p_price),
                  get_formatted_date(),
              ]],
              columns=COLUMNS,
          )
          st.session_state.df_master = pd.concat(
              [st.session_state.df_master, new_row], ignore_index=True
          )
          if save_db(
              st.session_state.df_master, f"Bought Mobile: {brand} {model}"
          ):
            st.success("موبائل کامیابی سے اسٹاک میں محفوظ ہو گیا ہے!")

  with tab2:
    if not mob_df.empty:
      avail_mobs = mob_df[mob_df["col7"] == "Available"]
    else:
      avail_mobs = pd.DataFrame()

    if avail_mobs.empty:
      st.info("فروخت کے لیے کوئی موبائل دستیاب نہیں ہے۔")
    else:
      mob_options = {}
      for _, row in avail_mobs.iterrows():
        b_name = row["col5"] if pd.notna(row["col5"]) else ""
        m_name = row["col6"] if pd.notna(row["col6"]) else ""
        cost_val = row["col10"] if pd.notna(row["col10"]) else "0"
        label = f"{b_name} ({m_name}) — خرید قیمت: PKR {cost_val}"
        mob_options[label] = row["id"]

      selected_choice = st.selectbox(
          "Select Available Mobile", list(mob_options.keys())
      )
      selected_id = mob_options[selected_choice]
      sel_row = avail_mobs[avail_mobs["id"] == selected_id].iloc[0]

      raw_cost = sel_row["col10"]
      if pd.notna(raw_cost) and str(raw_cost).replace('.', '', 1).isdigit():
        display_cost = float(raw_cost)
      else:
        display_cost = 0.0

      st.markdown("---")
      st.markdown("### 📋 منتخب کردہ موبائل کی مکمل تفصیلات:")
      d_col1, d_col2, d_col3 = st.columns(3)
      d_col1.markdown(f"**مالک کا نام:** {sel_row['col1']}")
      d_col1.markdown(f"**موبائل نمبر:** {sel_row['col2']}")
      d_col2.markdown(f"**آئی ڈی کارڈ نمبر:** {sel_row['col3']}")
      d_col2.markdown(f"**IMEI نمبر:** {sel_row['col4']}")
      d_col3.markdown(f"**خرید قیمت:** PKR {display_cost:,.0f}")
      d_col3.markdown(f"**خرید کی تاریخ:** {sel_row['timestamp']}")
      st.markdown("---")

      with st.form("sell_mob_form"):
        act_price = st.number_input(
            "Actual Selling Price (فروخت قیمت) *",
            min_value=0.0,
            step=100.0,
            value=display_cost,
        )
        c_b1, c_b2, c_b3 = st.columns(3)
        b_name = c_b1.text_input("Buyer Name (خریدار کا نام) *")
        b_phone = c_b2.text_input("Buyer Phone *")
        b_cnic = c_b3.text_input("Buyer CNIC *")

        if st.form_submit_button(
            "Complete Sale & Calculate Profit", use_container_width=True
        ):
          if not b_name or act_price <= 0:
            st.error("برائے مہربانی خریدار کا نام اور قیمت درج کریں۔")
          else:
            idx = sel_row.name
            st.session_state.df_master.loc[idx, "col7"] = "Sold"
            st.session_state.df_master.loc[idx, "col11"] = str(act_price)
            st.session_state.df_master.loc[idx, "timestamp"] = (
                get_formatted_date()
            )
            if save_db(st.session_state.df_master, "Completed Mobile Sale"):
              profit = act_price - display_cost
              st.success(
                  f"موبائل فروخت ہو گیا! خالص پرافٹ: PKR {profit:,.0f}"
              )
              st.rerun()

  with tab3:
    if not mob_df.empty:
      for idx, r in mob_df.iterrows():
        with st.container(border=True):
          col_m1, col_m2 = st.columns([4, 1])
          b_name = r["col5"] if pd.notna(r["col5"]) else ""
          m_name = r["col6"] if pd.notna(r["col6"]) else ""
          status = r["col7"] if pd.notna(r["col7"]) else ""
          col_m1.markdown(
              f"**{b_name} {m_name}** | Status:"
              f" **{status}**"
          )
          if col_m2.button("Delete ❌", key=f"del_mob_{r['id']}"):
            st.session_state.df_master = st.session_state.df_master.drop(idx)
            save_db(st.session_state.df_master, "Deleted Mobile Entry")
            st.rerun()
    else:
      st.info("کوئی ریکارڈ موجود نہیں۔")

# ============================================================
# ACCESSORIES PAGE
# ============================================================
elif page == "Accessories":
  st.subheader("🎧 Direct Accessories Sale & Profit")
  with st.form("direct_acc_sale_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    name = c1.text_input("Item Name *", placeholder="e.g. Charger, Handsfree")
    category = c2.selectbox(
        "Category",
        ["Chargers", "Handsfree", "Covers", "Glass/Protector", "Cables", "Other"],
    )
    c3, c4, c5 = st.columns(3)
    qty = c3.number_input("Quantity", min_value=1, step=1, value=1)
    p_price = c4.number_input("Unit Purchase Price", min_value=0.0, step=10.0)
    s_price = c5.number_input("Unit Sale Price", min_value=0.0, step=10.0)

    if st.form_submit_button(
        "Sell Accessory & Save Profit", use_container_width=True
    ):
      if not name or qty <= 0:
        st.error("برائے مہربانی آئٹم کا نام درج کریں۔")
      else:
        total_sale = s_price * qty
        total_cost = p_price * qty
        item_profit = total_sale - total_cost

        new_id = (
            int(st.session_state.df_master["id"].max() + 1)
            if not st.session_state.df_master.empty
            else 1
        )
        new_row = pd.DataFrame(
            [[
                new_id,
                "AccessorySale",
                name,
                category,
                str(qty),
                str(p_price),
                str(s_price),
                str(item_profit),
                "",
                "",
                "",
                "",
                "",
                get_formatted_date(),
            ]],
            columns=COLUMNS,
        )
        st.session_state.df_master = pd.concat(
            [st.session_state.df_master, new_row], ignore_index=True
        )
        if save_db(st.session_state.df_master, f"Accessory Sold: {name}"):
          st.success(f"فروخت کامیاب! خالص پرافٹ: PKR {item_profit:,.0f}")

  st.markdown("---")
  acc_df = (
      st.session_state.df_master[
          st.session_state.df_master["module"] == "AccessorySale"
      ]
      if not st.session_state.df_master.empty
      else pd.DataFrame()
  )
  if not acc_df.empty:
    for idx, ac in acc_df.tail(15).iterrows():
      col_a1, col_a2 = st.columns([4, 1])
      col_a1.markdown(
          f"**{ac['col1']}** ({ac['col2']}) - Qty: {ac['col3']} - Profit:"
          f" **PKR {float(ac['col6']):,.0f}**"
      )
      if col_a2.button("Delete ❌", key=f"del_acc_{ac['id']}"):
        st.session_state.df_master = st.session_state.df_master.drop(idx)
        save_db(st.session_state.df_master, "Deleted Accessory Sale")
        st.rerun()

# ============================================================
# REPAIR PAGE
# ============================================================
elif page == "Repair":
  st.subheader("🛠️ Mobile Repair Khata")
  with st.form("repair_form", clear_on_submit=True):
    c1, c2, c3 = st.columns(3)
    r_name = c1.text_input("Customer Name *")
    r_phone = c2.text_input("Mobile Number *")
    r_model = c3.text_input("Device Model *")
    r_fault = st.text_area("Fault Description *")

    c4, c5 = st.columns(2)
    r_cost = c4.number_input("Parts Cost Price - PKR *", min_value=0.0, step=50.0)
    r_sale = c5.number_input(
        "Total Charges / Sale Price - PKR *", min_value=0.0, step=50.0
    )

    if st.form_submit_button(
        "Save Repair & Update Dashboard", use_container_width=True
    ):
      if not r_name or not r_model or r_sale <= 0:
        st.error("برائے مہربانی نام اور درست قیمت درج کریں۔")
      else:
        repair_profit = r_sale - r_cost
        new_id = (
            int(st.session_state.df_master["id"].max() + 1)
            if not st.session_state.df_master.empty
            else 1
        )
        new_row = pd.DataFrame(
            [[
                new_id,
                "Repair",
                r_name,
                r_phone,
                r_model,
                r_fault,
                str(r_cost),
                str(r_sale),
                str(repair_profit),
                "Delivered",
                "",
                "",
                "",
                get_formatted_date(),
            ]],
            columns=COLUMNS,
        )
        st.session_state.df_master = pd.concat(
            [st.session_state.df_master, new_row], ignore_index=True
        )
        if save_db(st.session_state.df_master, f"Repair Done: {r_model}"):
          st.success(
              f"ریپیئرنگ محفوظ ہو گئی! خالص پرافٹ: PKR {repair_profit:,.0f}"
          )

  st.markdown("---")
  rep_df = (
      st.session_state.df_master[
          st.session_state.df_master["module"] == "Repair"
      ]
      if not st.session_state.df_master.empty
      else pd.DataFrame()
  )
  if not rep_df.empty:
    for idx, r in rep_df.tail(15).iterrows():
      with st.container(border=True):
        colA, colB = st.columns([4, 1])
        colA.markdown(
            f"**{r['col1']}** - {r['col3']} | Profit: **PKR"
            f" {float(r['col8']):,.0f}**"
        )
        if colB.button("Delete ❌", key=f"del_rep_{r['id']}"):
          st.session_state.df_master = st.session_state.df_master.drop(idx)
          save_db(st.session_state.df_master, "Deleted Repair")
          st.rerun()

# ============================================================
# EASYPAISA / JAZZCASH PAGE
# ============================================================
elif page == "EasyPaisa":
  st.subheader("💰 EasyPaisa / JazzCash Automatic Commission Calculator")
  with st.form("ep_auto_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    service_type = c1.selectbox(
        "Transaction Type",
        [
            ("EasyPaisaSend", "EasyPaisa Sending (PKR 10/1k)"),
            ("EasyPaisaReceive", "EasyPaisa Cash-In (PKR 20/1k)"),
            ("JazzCashSend", "JazzCash Sending (PKR 10/1k)"),
            ("JazzCashReceive", "JazzCash Cash-In (PKR 20/1k)"),
        ],
        format_func=lambda x: x[1],
    )[0]
    trans_amount = c2.number_input("Transaction Amount", min_value=0.0, step=500.0)

    auto_profit = (
        (trans_amount / 1000.0) * 10
        if "Send" in service_type
        else (trans_amount / 1000.0) * 20
    )
    st.info(f"👉 Automatic Commission: **PKR {auto_profit:,.2f}**")

    if st.form_submit_button(
        "Save Transaction & Add Profit", use_container_width=True
    ):
      if trans_amount <= 0:
        st.error("رقم درج کریں۔")
      else:
        new_id = (
            int(st.session_state.df_master["id"].max() + 1)
            if not st.session_state.df_master.empty
            else 1
        )
        new_row = pd.DataFrame(
            [[
                new_id,
                "Transaction",
                service_type,
                str(trans_amount),
                str(auto_profit),
                "Auto Commission",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                get_formatted_date(),
            ]],
            columns=COLUMNS,
        )
        st.session_state.df_master = pd.concat(
            [st.session_state.df_master, new_row], ignore_index=True
        )
        if save_db(st.session_state.df_master, f"EP/JC Transaction"):
          st.success("سندی محفوظ ہو گئی!")

# ============================================================
# EXPENSES PAGE
# ============================================================
elif page == "Expenses":
  st.subheader("💸 Shop Expenses & Home Khata")
  with st.form("expense_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    e_type = c1.selectbox(
        "Expense Type",
        [
            ("ShopExpense", "Shop Daily Expense"),
            ("HomeExpense", "Home Expense"),
        ],
        format_func=lambda x: x[1],
    )[0]
    amount = c2.number_input("Amount", min_value=0.0, step=50.0)
    desc = st.text_input("Description / Remarks *")

    if st.form_submit_button("Save Expense", use_container_width=True):
      if amount <= 0 or not desc:
        st.error("رقم اور تفصیل لازمی ہے۔")
      else:
        new_id = (
            int(st.session_state.df_master["id"].max() + 1)
            if not st.session_state.df_master.empty
            else 1
        )
        new_row = pd.DataFrame(
            [[
                new_id,
                "Transaction",
                e_type,
                str(amount),
                "0",
                desc,
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                get_formatted_date(),
            ]],
            columns=COLUMNS,
        )
        st.session_state.df_master = pd.concat(
            [st.session_state.df_master, new_row], ignore_index=True
        )
        if save_db(st.session_state.df_master, f"Expense Saved"):
          st.success("خرچہ محفوظ ہو گیا!")

# ============================================================
# UNIFIED ACTIVITY HISTORY
# ============================================================
elif page == "History":
  st.subheader("📜 Unified Activity History & Ledger")
  if not st.session_state.df_master.empty:
    for idx, r in st.session_state.df_master.tail(30).iloc[::-1].iterrows():
      with st.container(border=True):
        c1, c2, c3 = st.columns([2, 3, 1])
        c1.markdown(
            f"**[{r['module']}]**<br><small>{r['timestamp']}</small>",
            unsafe_allow_html=True,
        )
        c2.markdown(f"Details: {r['col1']} | {r['col2']}")
        if c3.button("Delete ❌", key=f"del_master_{r['id']}"):
          st.session_state.df_master = st.session_state.df_master.drop(idx)
          save_db(st.session_state.df_master, "Deleted Record")
          st.rerun()
  else:
    st.info("کوئی ریکارڈ موجود نہیں۔")

# ============================================================
# REPORTS & INVENTORY
# ============================================================
elif page == "Reports":
  st.subheader("📈 Detailed Reports")
  if not st.session_state.df_master.empty:
    st.dataframe(st.session_state.df_master, use_container_width=True)
  else:
    st.info("کوئی ڈیٹا موجود نہیں۔")

elif page == "Inventory":
  st.subheader("📦 Available Mobile Stock")
  mob_df = (
      st.session_state.df_master[
          (st.session_state.df_master["module"] == "Mobile")
          & (st.session_state.df_master["col7"] == "Available")
      ]
      if not st.session_state.df_master.empty
      else pd.DataFrame()
  )
  if not mob_df.empty:
    st.dataframe(mob_df, use_container_width=True)
  else:
    st.info("اسٹاک خالی ہے۔")

st.markdown("---")
st.caption(
    "Ali Mobiles & Communication — Super POS System | Cloud Secured via GitHub"
)
