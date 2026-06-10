import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Order Intelligence Assistant",
    page_icon="📦",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
}

.title-text {
    font-size: 32px;
    font-weight: 700;
}

.small-text {
    color: gray;
    font-size: 14px;
}

.chat-box {
    background: white;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    border-left: 5px solid #4f46e5;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SAMPLE DATA
# ---------------------------------------------------
data = {
    "Order ID": [1001, 1002, 1003, 1004, 1005, 1006, 1007],
    "Client": ["Amazon", "Walmart", "Target", "Best Buy", "Amazon", "Target", "Walmart"],
    "Status": [
        "Order Entered",
        "QA Pending",
        "Shipped",
        "In Progress",
        "Pending Approval",
        "Shipped",
        "In Progress"
    ],
    "Assigned To": [
        "Rahul",
        "Priya",
        "Amit",
        "Neha",
        "Rahul",
        "Amit",
        "Priya"
    ],
    "Created Date": [
        "2026-06-01",
        "2026-06-02",
        "2026-06-03",
        "2026-06-04",
        "2026-06-05",
        "2026-06-06",
        "2026-06-07"
    ],
    "Shipment Date": [
        "2026-06-12",
        "2026-06-13",
        "2026-06-08",
        "2026-06-15",
        "2026-06-16",
        "2026-06-09",
        "2026-06-17"
    ]
}

df = pd.DataFrame(data)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("📦 Order Intelligence Assistant")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Orders",
        "Analytics",
        "AI Assistant"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info("""
### Quick Actions
- Create Order
- Upload Orders
- Export Reports
""")

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.markdown("""
<div class='title-text'>
Dashboard
</div>

<div class='small-text'>
Overview of all orders and operations
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------
total_orders = len(df)
shipped_orders = len(df[df["Status"] == "Shipped"])
pending_orders = len(df[df["Status"] != "Shipped"])
in_progress = len(df[df["Status"] == "In Progress"])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Total Orders</h4>
        <h2>{total_orders}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Shipped</h4>
        <h2>{shipped_orders}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Pending</h4>
        <h2>{pending_orders}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>In Progress</h4>
        <h2>{in_progress}</h2>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# ---------------------------------------------------
# CHARTS
# ---------------------------------------------------
col1, col2 = st.columns(2)

with col1:

    status_count = df["Status"].value_counts()

    fig = px.pie(
        names=status_count.index,
        values=status_count.values,
        title="Orders By Status"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    assigned_count = df["Assigned To"].value_counts()

    fig2 = px.bar(
        x=assigned_count.index,
        y=assigned_count.values,
        title="Orders By Employee"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# ORDER TABLE
# ---------------------------------------------------
st.subheader("📋 Recent Orders")

st.dataframe(
    df,
    use_container_width=True
)

# ---------------------------------------------------
# SEARCH SECTION
# ---------------------------------------------------
st.write("")
st.subheader("🔍 Search Order")

search_order = st.text_input("Enter Order ID")

if search_order:

    try:
        search_order = int(search_order)

        result = df[df["Order ID"] == search_order]

        if not result.empty:

            st.success("Order Found")

            st.dataframe(result, use_container_width=True)

        else:
            st.error("Order not found")

    except:
        st.error("Please enter valid Order ID")

# ---------------------------------------------------
# AI ASSISTANT SECTION
# ---------------------------------------------------
st.write("")
st.subheader("🤖 AI Assistant")

user_query = st.text_input(
    "Ask something about orders"
)

if user_query:

    query = user_query.lower()

    # -------------------------------
    # SIMPLE AI LOGIC
    # -------------------------------

    if "pending" in query:

        pending_df = df[df["Status"] != "Shipped"]

        st.markdown("""
        <div class='chat-box'>
        Here are all pending orders.
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(pending_df)

    elif "shipped" in query:

        shipped_df = df[df["Status"] == "Shipped"]

        st.markdown("""
        <div class='chat-box'>
        Here are shipped orders.
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(shipped_df)

    elif "who is working" in query:

        active_df = df[df["Status"] == "In Progress"]

        st.markdown("""
        <div class='chat-box'>
        These employees are currently handling active orders.
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(active_df[[
            "Order ID",
            "Assigned To",
            "Status"
        ]])

    elif "summary" in query:

        st.markdown(f"""
        <div class='chat-box'>
        Total Orders: {total_orders}<br>
        Pending Orders: {pending_orders}<br>
        Shipped Orders: {shipped_orders}<br>
        In Progress: {in_progress}
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class='chat-box'>
        Sorry, I could not understand your query.
        Try:
        - Show pending orders
        - Show shipped orders
        - Who is working on orders?
        - Give summary
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.write("")
st.write("")

st.caption("© 2026 Order Intelligence Assistant")