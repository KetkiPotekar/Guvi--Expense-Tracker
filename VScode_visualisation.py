import streamlit as st
st.write("Mini Project: Expense Tracker Analysis")
st.write("Name- Ketki Potekar")

import pandas as pd
import streamlit as st
from pandas.api.types import CategoricalDtype


# Streamlit file uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])


if uploaded_file is not None:
    # Load the data
    df = pd.read_csv(uploaded_file)


    # Ensure 'Date' column is in datetime format
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])  # Convert to datetime
        df['Month_Num'] = df['Date'].dt.month    # Extract numerical month
        df['Month_Name'] = df['Date'].dt.strftime('%B')  # Extract month name
    else:
        st.error("The uploaded file must contain a 'Date' column.")


    # Define the correct month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    month_type = CategoricalDtype(categories=month_order, ordered=True)
    df['Month_Name'] = df['Month_Name'].astype(month_type)  # Set categorical type


    # Sort the DataFrame by Month_Name
    df = df.sort_values('Month_Name')


    # Pivot data for visualization
    pivot_table = df.pivot_table(
        index='Month_Name', columns='Category', values='Amount_Paid', aggfunc='sum'
    )


    # Display the line chart
    st.line_chart(pivot_table)


# visualisation 2: pie chart
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# Streamlit file uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'], key='csv_upload')


if uploaded_file is not None:
    # Load the data
    df = pd.read_csv(uploaded_file)


    # Ensure 'Date' column is in datetime format
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])  # Convert to datetime
        df['Month_Name'] = df['Date'].dt.strftime('%B')  # Extract month name
    else:
        st.error("The uploaded file must contain a 'Date' column.")


    # Calculate total amount spent by category
    category_totals = df.groupby('Category')['Amount_Paid'].sum()


    # Display the pie chart
    fig, ax = plt.subplots()
    ax.pie(
        category_totals,
        labels=category_totals.index,
        autopct='%1.1f%%',
        startangle=90
    )
    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
    st.pyplot(fig)



#Visualisation 3: Box plot

import streamlit as st
import pandas as pd
import plotly.express as px


# Streamlit file uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'], key='unique_key')


# Convert the 'date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])


# Create a box plot to represent the highest and lowest amount spent by category
fig = px.box(df,
             x='Category',  # Change x-axis to 'Category' for the categories of expenditure
             y='Amount_Paid',
             title='Spending Distribution by Category',
             labels={'Amount_Paid': 'Amount Spent', 'Category': 'Expense Category'},
             color='Category')  # Color categories for clarity


# Display the box plot in Streamlit
st.plotly_chart(fig)