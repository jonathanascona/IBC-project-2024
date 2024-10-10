import streamlit as st
import numpy as np
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import seaborn as sns

# Page title
# st.set_page_config(page_title='Sales Dashboard', page_icon='📊')
st.title('Sales Dashboard')

def app():

    if 'uploaded_file' in st.session_state:
        uploaded_file = st.session_state.uploaded_file
        
        # Load data
        dataframe = pd.read_excel(uploaded_file, sheet_name=['Sales'])
        df = dataframe['Sales']
        
        st.write("This dashboard provides a comprehensive analysis of sales and quantity data over specified dates. Each chart offers insights into different aspects of the data, helping you to understand the patterns and trends. The filter is on the far lefthand side of the screen.")
        
        st.write(f"Summary of the dashboard:  \n- First table is the raw data from the Sales sheet   \n- The following charts give insights into what items are the most popular and profitable. This can help workers to be more effective with inventory. As well as be able to forecast future profits and risks.")
        
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Sidebar filters
        st.sidebar.header('Filters')
        date_range = st.sidebar.date_input('Date range', value=[df['Date'].min().date(), df['Date'].max().date()])
        items = st.sidebar.multiselect('Select Items Sold', options=df['Item Sold'].unique(), default=df['Item Sold'].unique())
        
        # Convert date_range to datetime
        date_range = [pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])]
        
        # Filter data
        # filtered_data = df[(df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])]
        # if items:
        #     filtered_data = filtered_data[filtered_data['Item Sold'].isin(items)]
        
        # Display data
        st.header('Data')
        st.dataframe(df)
        
        # def plot_line_chart(df, title):
        #         plt.figure(figsize=(10, 6))
        #         sns.lineplot(data=df, x=df["Date"], y=df["Total Sales"])
        #         plt.title(title)
        #         plt.xlabel('Date')
        #         plt.ylabel('Total Sales')
        #         plt.xticks(rotation=45)
        #         st.pyplot(plt)
        
        # plot_line_chart(df,'Sales by Date')
        
        # Sales by Date (Line Chart)
        st.header('Sales by Date')
        sales_by_date = df.groupby('Date')['Total Sales'].sum()
        fig, ax = plt.subplots()
        ax.plot(sales_by_date.index, sales_by_date.values, marker='o')
        ax.set_xlabel('Date')
        ax.set_ylabel('Total Sales')
        # ax.set_title('Sales by Date')
        ax.tick_params(axis='x', rotation=45)  # Make x-axis labels horizontal
        st.pyplot(fig)
        
        # Sales by Item Sold (Bar Chart)
        st.header('Sales by Item Sold')
        sales_by_item = df.groupby('Item Sold')['Total Sales'].sum()
        fig, ax = plt.subplots()
        sales_by_item.plot(kind='barh', ax=ax)
        ax.set_ylabel('')
        ax.set_xlabel('Total Sales $')
        # ax.set_title('Sales by Item Sold')
        st.pyplot(fig)
        
        # Quantity Sold by Item Sold (Horizontal Bar Chart)
        st.header('Quantity Sold by Item Sold')
        quantity_by_item = df.groupby('Item Sold')['Quantity Sold '].sum()
        fig, ax = plt.subplots()
        quantity_by_item.plot(kind='barh', ax=ax)
        ax.set_xlabel('Quantity Sold')
        ax.set_ylabel('')
        # ax.set_title('Quantity Sold by Item Sold')
        st.pyplot(fig)
        
        # Extract day of the week
        df['DayOfWeek'] = df['Date'].dt.day_name()
        
        # Filter for weekdays (Monday to Friday)
        weekday_data = df[df['DayOfWeek'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]
        
        fig, ax = plt.subplots()
        weekday_data.groupby('DayOfWeek')['Quantity Sold '].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']).plot(ax=ax, marker='o', label="")
        
        st.header('Average Quantity Sold by Day of the Week')
        ax.set_ylabel('Average Quantity Sold')
        # ax.set_title('Average Quantity Sold by Day of the Week')
        ax.set_xlabel('Day of the Week')
        ax.legend()
        st.pyplot(fig)
        
        # Advanced Chart: Pair Plot of Sales Data
        # st.header('Pair Plot of Sales Data')
        # sns.pairplot(df, diag_kind='kde', markers='+')
        # st.pyplot(plt.gcf())
        
    else:
        st.info("Please upload an Excel file on the Home page to get started")
