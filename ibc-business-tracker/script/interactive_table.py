import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd


def color_hr(val, hour=40):
    color = 'green' if val >= hour else 'red'
    return f'background-color: {color}'

# Sample data
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Total Hours Worked': [40, 38, 45, 50]
}
details_data = {
    'Name': ['Alice', 'Alice', 'Alice', 'Bob', 'Bob', 'Charlie', 'Charlie', 'Charlie', 'Charlie', 'David', 'David'],
    'Task': ['Task A', 'Task B', 'Task C', 'Task A', 'Task B', 'Task A', 'Task B', 'Task C', 'Task D', 'Task A', 'Task B'],
    'Hours': [10, 15, 15, 20, 18, 10, 20, 5, 10, 25, 25]
}

df_summary = pd.DataFrame(data)
df_details = pd.DataFrame(details_data)
df_summary_styled = df_summary.style.applymap(color_hr, subset=['Total Hours Worked'])
# Display the styled dataframe
st.dataframe(df_summary_styled)
# Display summary table
st.write("Summary of Hours Worked:")
gb_summary = GridOptionsBuilder.from_dataframe(df_summary)
gb_summary.configure_default_column(editable=False, groupable=True)
gb_summary.configure_selection('single', use_checkbox=True)
gridOptions_summary = gb_summary.build()

summary_response = AgGrid(
    df_summary,
    gridOptions=gridOptions_summary,
    enable_enterprise_modules=False,
    editable=False,
    fit_columns_on_grid_load=True,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    theme='streamlit',
    height=200,
    width='100%'
)

# Debugging: Print the selected rows and its type
# st.write("Selected Rows Debug Info:")
# st.write(summary_response['selected_rows'])
# st.write("Type of selected rows:")
# st.write(type(summary_response['selected_rows']))

# Get selected person
try:
    selected = summary_response['selected_rows']

    if not selected.empty:
        selected_name = selected.iloc[0]['Name']
        st.write(f"Tasks for {selected_name}:")
        df_selected_details = df_details[df_details['Name'] == selected_name]
        gb_details = GridOptionsBuilder.from_dataframe(df_selected_details)
        gb_details.configure_default_column(editable=False, groupable=True)
        gridOptions_details = gb_details.build()

        details_response = AgGrid(
            df_selected_details,
            gridOptions=gridOptions_details,
            enable_enterprise_modules=False,
            editable=False,
            fit_columns_on_grid_load=True,
            update_mode=GridUpdateMode.NO_UPDATE,
            theme='streamlit',
            height=200,
            width='100%'
        )
    else:
        st.write("No selection made. Please select a row to see task details.")
except:
    st.write("No selection made. Please select a row to see task details.")


