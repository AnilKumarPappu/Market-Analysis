import pandas as pd
import streamlit as st

# import matplotlib.pyplot as plt
# import plotly.express as px

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
    # line chart
    truncated_data3 = truncated_data2[["Date", "Volume", "Value"]]
    truncated_data3.set_index("Date", inplace=True)
    # Display line chart for both Value and Volume columns
    st.line_chart(
        truncated_data3, use_container_width=True, color=["#FF0000", "#0000FF"]
    )
# with col2:
# pie_data = (
#     truncated_data2[["SKU Name", "Value"]]
#     .sort_values("Value")
#     .groupby("SKU Name")["Value"]
#     .sum()
#     .reset_index()
# )
# fig = px.pie(
#     pie_data,
#     values="Value",
#     names="SKU Name",
#     title="Percentage of Sales Values for each SKU",
# )

# Display the pie chart using Streamlit's st.plotly_chart()
# st.write(fig)


# pie chart
# pie_data = (
#     truncated_data2[["SKU Name", "Value"]]
#     .sort_values("Value")
#     .groupby("SKU Name")["Value"]
#     .sum()
#     .reset_index()
# )
# # st.write("Percentage of Sales Values for each SKU")
# # st.write(pie_data.set_index('SKU Name')['Value'].plot.pie(autopct='%1.1f%%'))
# fig, ax = plt.subplots()
# # ax.pie(
# #     pie_data["Value"], labels=pie_data["SKU Name"], autopct="%1.1f%%", startangle=90
# # )
# wedges, texts, autotexts = ax.pie(
#     pie_data["Value"],
#     labels=pie_data["SKU Name"],
#     autopct="%1.1f%%",
#     startangle=90,
#     textprops=dict(color="w"),
#     # wedgeprops=dict(width=0.3),
# )
# ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
# ax.legend(
#     wedges, pie_data["SKU Name"], loc="center left", bbox_to_anchor=(1, 0, 0.5, 1)
# )

# # Display pie chart using Streamlit's st.pyplot()
# st.write("Percentage of Sales Values for each SKU")
# st.pyplot(fig)

##############
# truncated_data4 = truncated_data2[["Date", "Volume", "Value"]]
# # Create a figure with secondary y-axis
# fig = go.Figure()

# # Add traces for Value and Volume on different y-axes
# fig.add_trace(
#     go.Scatter(
#         x=truncated_data4["Date"], y=truncated_data4["Value"], name="Value", yaxis="y"
#     )
# )
# fig.add_trace(
#     go.Scatter(
#         x=truncated_data4["Date"],
#         y=truncated_data4["Volume"],
#         name="Volume",
#         yaxis="y2",
#     )
# )

# # Update layout to have two y-axes
# fig.update_layout(
#     yaxis=dict(title="Value", side="left", showgrid=False),
#     yaxis2=dict(title="Volume", side="right", overlaying="y", showgrid=False),
#     xaxis=dict(title="Date"),
#     legend=dict(x=0, y=1),
# )

# # Display the figure
# st.plotly_chart(fig)
#######################
col1, col2 = st.columns(2)
with col1:
    # line chart
    truncated_data3 = truncated_data2[["Date", "Price", "Volume"]]
    truncated_data3.set_index("Date", inplace=True)
    # Display line chart for both Value and Volume columns
    st.line_chart(
        truncated_data3, use_container_width=True, color=["#FF0000", "#0000FF"]
    )
with col2:
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
    # line chart
    sku_truncated_data3 = sku_truncated_data2[["Date", "Volume", "Value"]]
    sku_truncated_data3.set_index("Date", inplace=True)
    # Display line chart for both Value and Volume columns
    st.line_chart(
        sku_truncated_data3, use_container_width=True, color=["#FF0000", "#0000FF"]
    )
with col2:
    sku_truncated_data2["month_year"] = sku_truncated_data2["Date"].dt.to_period("M")
    average_per_month = sku_truncated_data2.groupby("month_year")["Value"].mean()

    avg_value_monthly_df = average_per_month.reset_index()
    avg_value_monthly_df.columns = ["Month", "Average Value"]

    # Plotting the bar chart
    st.bar_chart(avg_value_monthly_df.set_index("Month"))
