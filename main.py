import streamlit as st
import pandas as pd
from datetime import datetime

# from session_state import get_session


def get_session():
    # Create a dictionary to store session variables
    if "session" not in st.session_state:
        st.session_state.session = {}
    return st.session_state.session


st.title("Manufacture's market analysis")
data = pd.read_csv("Input_Sales_Data_v2.csv")
min_date = datetime.strptime(data["Date"].min(), "%Y-%m-%d")
max_date = datetime.strptime(data["Date"].max(), "%Y-%m-%d")

col1, col2 = st.columns(2)

with col1:
    # st.header("Slider")
    value = st.slider("Select the date", min_date, max_date)
    st.write("Start Date:", value)
    st.write("End Date:", max_date)
with col2:
    # st.header("Dropdown")
    Category = st.selectbox("Choose Category", ["Category_1", "Category_0"])

session = get_session()
session["category"] = Category

# print(data)
# data according to slider and category
truncated_data = data[(data["Date"] >= str(value)) & (data["Category"] == Category)]
session["truncated_data"] = truncated_data
session["manufacturers_list"] = truncated_data["Manufacturer"].unique().tolist()
session["brand_list"] = truncated_data["Brand"].unique().tolist()
# Data gropped according to manufacturer
gropped_data = (
    truncated_data.groupby(["Manufacturer"], as_index=False)
    .agg({"Volume": "sum", "Value": "sum"})
    .sort_values("Value", ascending=False)
    .reset_index()[["Manufacturer", "Volume", "Value"]]
)
# session["manufacturers_list"] = gropped_data["Manufacturer"].to_list()
# Market percentage collumn is added
total_value = gropped_data["Value"].sum()
gropped_data["Market Percentage"] = (gropped_data["Value"] / total_value) * 100

# Styling to applied to the dataframe
styled_df = (
    gropped_data.style.format({"Market Percentage": "{:.2f}%"}).format(
        {"Value": "{:,.2f}", "Volume": "{:,.2f}"}
        # precision=5, thousands=",", decimal="."
    )
    # .background_gradient(cmap="YlGnBu", subset=["Market Percentage"])
)

st.dataframe(styled_df)
# print(styled_df)

# capturing the top manufacturers
top_manufactures = gropped_data.sort_values("Value", ascending=False).head(5)
top_manufactures_data = (
    truncated_data[
        truncated_data["Manufacturer"].isin(top_manufactures["Manufacturer"])
    ][["Date", "Manufacturer", "Value", "Volume"]]
    .groupby(["Manufacturer", "Date"], as_index=False)
    .agg({"Volume": "sum", "Value": "sum"})
)
pivot_df = top_manufactures_data.pivot_table(
    index="Date", columns="Manufacturer", values="Value", aggfunc="sum"
)
# Line chart according to top manufacturers
# print(pivot_df)
st.line_chart(pivot_df)
logo = "logo3.png"
st.sidebar.image(logo, width=150, use_column_width=True)
