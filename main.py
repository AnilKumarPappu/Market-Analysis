import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Manufacture's market analysis")
data = pd.read_csv("Input_Sales_Data_v2.csv")
min_date = datetime.strptime(data["Date"].min(), "%Y-%m-%d")
max_date = datetime.strptime(data["Date"].max(), "%Y-%m-%d")
# print(type(min_date))
value = st.slider("Select the date", min_date, max_date)
st.write("Start Date:", value)
st.write("End Date:", max_date)

# print(data)
truncated_data = data[data["Date"] >= str(value)]

temp_data = truncated_data.groupby(["Manufacturer"], as_index=False).agg(
    {"Volume": "sum", "Value": "sum"}
)
st.dataframe(temp_data)
top_manufactures = temp_data.sort_values("Value", ascending=False).head(5)
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

print(pivot_df)
st.line_chart(pivot_df)
logo = "download.png"
st.sidebar.image(logo, width=100)
