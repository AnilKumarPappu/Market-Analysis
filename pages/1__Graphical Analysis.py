import pandas as pd
import streamlit as st
import pydeck as pdk
import altair as alt

import plotly.express as px

# import plotly.graph_objs as go

# from session_state import get_session


def get_session():
    # Create a dictionary to store session variables
    if "session" not in st.session_state:
        st.session_state.session = {}
    return st.session_state.session


st.title("Graphical Analysis")
session = get_session()

col1, col2, col3 = st.columns(3)

with col1:
    if "category" in session:
        st.header(session["category"])
with col2:
    # st.header("Dropdown")
    if "manufacturers_list" in session:
        manufacturer = st.selectbox(
            "Choose Manufacturer", session["manufacturers_list"]
        )
with col3:
    if "brand_list" in session:
        brand = st.selectbox("Choose Brand", session["brand_list"])

# need to get the values below according to the selected manufacturer and brand
col1, col2, col3, col4 = st.columns(4)
truncated_data = session["truncated_data"]
truncated_data["Date"] = pd.to_datetime(truncated_data["Date"])

# filtered the data for above manufacturer and brand
truncated_data2 = truncated_data[
    (truncated_data["Manufacturer"] == manufacturer)
    & (truncated_data["Brand"] == brand)
]

total_value = truncated_data["Value"].sum()
Volume_sales = truncated_data2[truncated_data2["Date"].dt.year == 2021]["Volume"].sum()
Value_sales = truncated_data2[truncated_data2["Date"].dt.year == 2021]["Value"].sum()
Market_sales = truncated_data2["Value"].sum() / total_value
# print(Market_sales)
Market_sales = "{:.2%}".format(Market_sales)
sku = truncated_data2["SKU Name"].unique().tolist()

col1.metric("YTD Volume Sales 2021", Volume_sales)
col2.metric("YTD $ Sales", Value_sales)
col3.metric("YTD Market Sales", Market_sales)
with col4.expander("List of SKU's"):
    for item in sku:
        st.write(item)
# print(truncated_data2.columns)


col1, col2 = st.columns(2)
with col1:
    st.subheader("Line chart showing weekly Volume sales and value sales")
    # line chart
    truncated_data3 = truncated_data2[["Date", "Volume", "Value"]]
    truncated_data3.set_index("Date", inplace=True)
    # Display line chart for both Value and Volume columns
    st.line_chart(
        truncated_data3, use_container_width=True, color=["#FF0000", "#0000FF"]
    )
with col2:
    st.subheader("Percentage of Sales Values for each SKU")
    pie_data = (
        truncated_data2[["SKU Name", "Value"]]
        .sort_values("Value")
        .groupby("SKU Name")["Value"]
        .sum()
        .reset_index()
    )
    fig = px.pie(
        pie_data,
        values="Value",
        names="SKU Name",
    )
    # Decrease the size of the chart
    fig.update_layout(width=400, height=300)
    # Display the pie chart using Streamlit's st.plotly_chart()
    st.write(fig)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Trend line chart showing Price and Volume sales")
    # line chart
    truncated_data3 = truncated_data2[["Date", "Price", "Volume"]]
    truncated_data3.set_index("Date", inplace=True)
    # Display line chart for both Value and Volume columns
    st.line_chart(
        truncated_data3, use_container_width=True, color=["#FF0000", "#0000FF"]
    )
with col2:
    st.subheader("Trend line chart showing Price and Value sales")
    # line chart
    truncated_data3 = truncated_data2[["Date", "Price", "Value"]]
    truncated_data3.set_index("Date", inplace=True)
    # Display line chart for both Value and Volume columns
    st.line_chart(
        truncated_data3, use_container_width=True, color=["#FF0000", "#0000FF"]
    )

# SKU multi select box
sku_selected = st.multiselect("select the SKU's", sku)
sku_truncated_data2 = truncated_data2[truncated_data2["SKU Name"].isin(sku_selected)]

col1, col2 = st.columns(2)
with col1:
    st.subheader(
        "Line chart showing weekly Volume sales and value sales for selected SKU's"
    )
    # line chart
    sku_truncated_data3 = sku_truncated_data2[["Date", "Volume", "Value"]]
    sku_truncated_data3.set_index("Date", inplace=True)
    # Display line chart for both Value and Volume columns
    st.line_chart(
        sku_truncated_data3, use_container_width=True, color=["#FF0000", "#0000FF"]
    )
with col2:
    st.subheader(
        "Bat chart showing average value sales for each month for selected SKU's"
    )
    sku_truncated_data2["month_year"] = sku_truncated_data2["Date"].dt.to_period("M")
    average_per_month = sku_truncated_data2.groupby("month_year")["Value"].mean()

    avg_value_monthly_df = average_per_month.reset_index()
    avg_value_monthly_df.columns = ["Month", "Average Value"]

    # Plotting the bar chart
    st.bar_chart(avg_value_monthly_df.set_index("Month"))
