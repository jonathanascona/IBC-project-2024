import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import matplotlib.pyplot as plt

# Useful functions
def color_hr(val, hour=20):
    color = 'green' if val >= hour else 'red'
    return f'background-color: {color}'

def app():
    st.title('📊 Manage Data')

    if 'uploaded_file' in st.session_state:
        uploaded_file = st.session_state.uploaded_file
        df = pd.read_excel(uploaded_file, sheet_name=['Member Actions'])
        df_details = df['Member Actions']
        df_summary = df_details[['Member Name', 'Duration']].groupby('Member Name')['Duration'].sum().reset_index()  
        df_summary_styled = df_summary.style.applymap(color_hr, subset=['Duration'])

        # # Display the styled dataframe
        # st.dataframe(df_summary_styled)
        # Display summary table
        st.dataframe(df_summary_styled)
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
        st.write("Selected Rows Debug Info:")
        st.write(summary_response['selected_rows'])
        # st.write("Type of selected rows:")
        # st.write(type(summary_response['selected_rows']))

        # Get selected person
        try:
            selected = summary_response['selected_rows']

            if not selected.empty:
                selected_name = selected.iloc[0]['Member Name']
                st.write(f"Tasks for {selected_name}:")
                df_selected_details = df_details[df_details['Member Name'] == selected_name]
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

        # Create and display the bar chart with a dotted line at the 40-hour mark
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df_summary['Member Name'], df_summary['Duration'], color='skyblue')
        ax.axhline(y=40, color='r', linestyle='--', linewidth=2)
        ax.set_xlabel('Member Name')
        ax.set_ylabel('Total Duration')
        ax.set_title('Total Duration by Member Name')
        ax.text(0, 42, '40-hour mark', color='red')
        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)
        
    else:
        st.info("Please upload an Excel file on the Home page to get started")
