import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Manufacture's market analysis")
data = pd.read_csv("Input_Sales_Data_v2.csv")
min_date = datetime.strptime(data["Date"].min(), "%Y-%m-%d")
max_date = datetime.strptime(data["Date"].max(), "%Y-%m-%d")
# print(type(min_date))
value = st.slider("Select the date", min_date, max_date)
st.write("Date:", value)
temp_data = (
    data[data["Date"] <= str(value)]
    .groupby("Manufacturer")
    .agg({"Volume": "sum", "Value": "sum"})
)
st.dataframe(temp_data)
top_manufactures_data = temp_data.sort_values("Value", ascending=False).head(5)
st.line_chart(top_manufactures_data)
logo = "download.png"
st.sidebar.image(logo)
