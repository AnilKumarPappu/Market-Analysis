import plotly.express as px
import streamlit as st
import pandas as pd

# from st_aggrid import AgGrid,     GridOptionsBuilder

# from st_aggrid import AgGrid
from st_aggrid import AgGrid, GridOptionsBuilder

df = pd.read_csv("Scenarios Summary.csv")
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_selection(use_checkbox=True, selection_mode="multiple")
gridoptions = gd.build()
grid_return = AgGrid(df, gridOptions=gridoptions)
new_df = grid_return["selected_rows"]

# st.dataframe(new_df)
new_df = pd.DataFrame(new_df)
# print(new_df)
# print(type(new_df))
if (new_df.empty) == 0:
    new_df = (
        new_df[["Name", "revenue", "cost", "profit"]].set_index("Name").T.reset_index()
    )
    # new_df.rename_axis("Metric")
    df = pd.DataFrame(new_df)
    # st.dataframe(df)

    columns = df.columns.to_list()
    fig = px.bar(
        new_df,
        x="index",
        y=columns,
        barmode="group",
        labels={"value": "Value($)", "variable": "Values"},
        # text=new_df.drop("index", axis=1).values.flatten(),
        title="Comparision of selected scenarios",
    )
    st.plotly_chart(fig)
