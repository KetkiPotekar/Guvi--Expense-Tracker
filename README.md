# Guvi--Expense-Tracker

Mini project for Guvi class for analyzing personal expenses

Mini Project - Expense Tracker

Name - Ketki Potekar 

Batch - 

Date - 31/12/2024

# Introduction
Purpose: 
Managing personal expenses is a critical skill, yet many people struggle with handling expenses. The purpose of this project is to develop an expense tracker that simplifies this process and gives insights into spending analysis and patterns.

# Problem Statement:
This project aims to simulate an expense tracker for an individual using the Faker library. The project generates realistic monthly expense data, processes and stores it in a SQL database, and creates SQL queries to derive insights into spending behavior. A Streamlit app is developed to visualize these insights and showcase the results of SQL queries. The tracker will highlight expenses across categories like bills, groceries, subscriptions, and personal spending, providing a comprehensive overview of financial habits over a year.

# Objectives:






# Data Generation using Faker library
# Step 1 : Generate expense data for each month 

    from faker import Faker
    import random
    import pandas as pd
    fake = Faker()
    
    def generate_expenses(num_entries, month, year):
        categories = ['Food', 'Transportation', 'Bills', 'Groceries', 'Subscriptions', 'Entertainment', 'Miscellaneous']
        payment_modes = ['Cash', 'UPI', 'Credit Card', 'Debit Card', 'NetBanking']
        bills = ['electricity', 'gas', 'water', 'wifi', 'phone']
        subscription = ['spotify', 'wynk', 'prime', 'netflix', 'youtube']
        
        data = []
        for _ in range(num_entries):
            # Generate a random date within the specified month and year
            date = fake.date_between_dates(
                date_start=pd.Timestamp(year, month, 1),
                date_end=pd.Timestamp(year, month, 28)  # Assume 28 days for simplicity
            )
            data.append({
                'Date': date,
                'Category': random.choice(categories),
                'Payment_Mode': random.choice(payment_modes),
                'Description': fake.sentence(nb_words=5),
                'Amount_Paid': round(random.uniform(10, 500), 2),
                'Cashback': round(random.uniform(0, 20), 2) if random.random() > 0.5 else 0.0
            })
    return pd.DataFrame(data)
   
    # User input for month and year
    target_month = int(input("Enter the target month (1-12): "))
    target_year = int(input("Enter the target year (e.g., 2024): "))
   
    # Generate data
    df = generate_expenses(100, target_month, target_year)
   
    # Save to CSV
    df.to_csv('expenses_specific_month.csv', index=False)
    print("Sample data for the specified month generated!")

This will give the following output where one needs to input the desired month and year.
    Enter the target month (1-12):  1
    Enter the target year (e.g., 2024):  2024
    Sample data for the specified month generated!

# The generated data was added to a table called JANUARY and saved using pandas and sqlite3.
    import sqlite3
    conn = sqlite3.connect('expenses.db')
    df.to_sql('January', conn, if_exists='replace', index=False)

Once the sample data for January month is generated and stored in a table, this step was repeated another 11 times to generate data for all 12 months using the same code.

# Step 2: Compile the data of all 12 months table into one single table
    import sqlite3

    #Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    #Create the consolidated table if it doesn't already exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AllMonths (
        Date TEXT,
        Category TEXT,
        Payment_Mode TEXT,
        Description TEXT,
        Amount_Paid REAL,
        Cashback REAL
    );
    ''')
    conn.commit()

    #List of monthly table names
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    #Loop through each month and copy data into the consolidated table
    for month in months:
        try:
            # Copy data from the monthly table to the consolidated table
            cursor.execute(f'''
            INSERT INTO AllMonths
            SELECT * FROM {month};
            ''')
            print(f"Data from {month} table has been added to AllMonths.")
        except sqlite3.OperationalError as e:
            print(f"Error with {month} table: {e}. Skipping this table.")

    #Commit the changes
    conn.commit()

    #Verify the number of rows in the consolidated table
    cursor.execute('SELECT COUNT(*) FROM AllMonths;')
    row_count = cursor.fetchone()[0]
    print(f"Total rows in AllMonths table: {row_count}")

    #Close the connection
    conn.close()

The following output is displayed -
	
 Data from January table has been added to AllMonths.
	
 Data from February table has been added to AllMonths.
	
 Data from March table has been added to AllMonths.
	
 Data from April table has been added to AllMonths.
	
 Data from May table has been added to AllMonths.
	
 Data from June table has been added to AllMonths.
	
 Data from July table has been added to AllMonths.
	
 Data from August table has been added to AllMonths.
	
 Data from September table has been added to AllMonths.
	
 Data from October table has been added to AllMonths.
	
 Data from November table has been added to AllMonths.
	
 Data from December table has been added to AllMonths.
	
 Total rows in AllMonths table: 1200

Now we have a table called AllMonths with expense data ready for analysis. We can view this table in python using the following code - 

    import sqlite3
    import pandas as pd
    
    # Connect to the database
    conn = sqlite3.connect('expenses.db')
    
    # Load the table into a Pandas DataFrame
    df = pd.read_sql_query("SELECT * FROM AllMonths;", conn)
    
    # Display the DataFrame
    print(df)
    
    # show as a table in Jupyter Notebook
    from IPython.display import display
    display(df)
    
    # Close the connection
    conn.close()

This is the output generated -

<img width="728" alt="Expenses_Table" src="https://github.com/user-attachments/assets/0ed3dccc-6eea-49be-b6fb-6e8cb1bbeca8" />

# Step3: Save this table in .csv format 
    import sqlite3
    import pandas as pd
    
    # Connect to the SQLite database
    conn = sqlite3.connect('expenses.db')
    
    # Load the data from the AllMonths table into a Pandas DataFrame
    df = pd.read_sql_query("SELECT * FROM AllMonths;", conn)
    
    # Save the DataFrame as a CSV file
    csv_file_path = "all_months_expenses.csv"
    df.to_csv(csv_file_path, index=False)
    
    # Close the database connection
    conn.close()
    
    print(f"Data exported successfully to {csv_file_path}")
    
Output -
	Data exported successfully to all_months_expenses.csv

# Step 4: Running SQL queries
The “all_months_expenses.csv” table was downloaded. A MySQL connection was established so that queries could be run on sql workbench.

# Query 1: Total Expenditure
    SELECT SUM(Amount_Paid) AS Total_Expenditure
    FROM allmonths

This gives the total expenditure throughout the year which was Rs.309731.55/-

<img width="575" alt="Query1" src="https://github.com/user-attachments/assets/a3a9d114-7c74-4718-a0f0-9112a63d068a" />

# Query 2: Most Expensive Transaction
    SELECT * 
    FROM allmonths
    ORDER BY Amount_Paid DESC
    Limit 1

<img width="575" alt="Query2" src="https://github.com/user-attachments/assets/7b553197-19f3-42a3-8d70-e75fc139895b" />

# Query 3: Total Monthly Expenditure
    SELECT 
	    Month(Date) AS Month,
	    SUM(Amount_Paid) AS Monthly_Expenditure
    FROM allmonths
    GROUP BY Month(Date)
    ORDER BY month

<img width="577" alt="Query3" src="https://github.com/user-attachments/assets/00a41d3c-6e98-4ae4-8849-0ee7fb61ed56" />
    
# Query 4: Top Spending Categories
    SELECT 
	    Category
	    SUM(Amount_Paid) AS Total_Spent
    FROM allmonths
    GROUP BY Category
    ORDER BY Total_Spent DESC

<img width="572" alt="Query4" src="https://github.com/user-attachments/assets/440cdfff-ad43-44d7-acde-14002421424a" />

# Query 5: Payment Mode Distribution
    SELECT
	    Month(Date) AS Month
	    SUM(Cashback) AS Total_Cashback
    FROM allmonths
    GROUP BY Month(Date)
    ORDER BY Month

<img width="567" alt="Query5" src="https://github.com/user-attachments/assets/77de06f0-5ba6-4c4b-825f-670e0a1e930d" />

# Query 6: Average Spend per Transaction
    SELECT 
	    AVG(Amount_Paid) AS Average_Transaction_Amount
    FROM allmonths

<img width="528" alt="Query6" src="https://github.com/user-attachments/assets/cbb45fff-ec6a-47be-b621-5768501fc8b0" />

# Query 7: Categories with Cashback Opportunities
    SELECT 
	    Category,
	    SUM(Cashback) as Total_Cashback
    FROM allmonths
    GROUP BY Category
    ORDER BY Total_Cashback DESC

<img width="526" alt="Query7" src="https://github.com/user-attachments/assets/5d0caf1c-a995-45a0-897b-230fa168dd8a" />

# Query 8: Least Spending Categories
    SELECT 
	    Category
	    SUM(Amount_Paid) AS Total_Spent
    FROM allmonths
    GROUP BY Category
    ORDER BY Total Spent  ASC
    LIMIT 1

<img width="526" alt="Query8" src="https://github.com/user-attachments/assets/d69c6e8c-41d2-4dfe-8d11-c3419986adc9" />

# Query 9: Average Monthly Cashback
    SELECT
        Month(Date) AS Month,
        AVG(Cashback) AS Avg_Cashback
    FROM allmonths
    GROUP BY Month(Date)

<img width="530" alt="Query9" src="https://github.com/user-attachments/assets/e2c54e6f-acab-412f-9c5e-8632c99a82ec" />

# Query 10: Daily Spending Trends
    SELECT 
	    Day(Date) AS Date,
	    SUM(Amount_Paid) AS Total_Spent
    FROM allmonths

<img width="572" alt="Query10 1" src="https://github.com/user-attachments/assets/c7701596-845a-48c9-acf7-2f5c473d8f5b" />
<img width="572" alt="Query10 2" src="https://github.com/user-attachments/assets/ac0d6c7c-4f25-44b4-b493-06144f7f7dbf" />

# Query 11: Month with Maximum Expenditure
    SELECT 
	    Month(Date) AS Month,
	    SUM(Amount_Paid) AS Total_Expenditure
    FROM allmonths
    GROUP BY Month(Date)
    ORDER BY Total_Expenditure DESC
    LIMIT 1

<img width="568" alt="Query11" src="https://github.com/user-attachments/assets/eb39fe3b-095b-40ff-8fc8-e9accfd1713d" />

# Query 12: Maximum and Minimum Transaction Amount
    SELECT
	    MAX(Amount_Paid) AS Max_Transaction
	    MIN(Amount_Paid) AS Min_Transaction
    FROM allmonths

<img width="533" alt="Query12" src="https://github.com/user-attachments/assets/e13b805e-9542-4fcb-92d3-a24bb81e763b" />

# Query 13: Cashback earned by Month
    SELECT 
	    Month(Date) AS Month
    SUM(Cashback) AS Total_Cashback
    FROM allmonths
    GROUP BY Month(Date)
    ORDER BY Month

<img width="572" alt="Query13" src="https://github.com/user-attachments/assets/2bf3082d-a2ac-4578-a409-110f69e0c037" />

# Query 14: Transaction exceeding amount Rs 490
    SELECT *
    FROM allmonths
    WHERE Amount_Paid > 490

<img width="517" alt="Query14" src="https://github.com/user-attachments/assets/fad9eeaf-79b6-496a-b665-f0d3a7607a20" />

# Query 15: Average Transaction Amount by Category
    SELECT 
	    Category,
	    AVG(Amount_Paid) AS Avg_Transaction_Amount
    FROM allmonths
    GROUP BY Category

<img width="539" alt="Query15" src="https://github.com/user-attachments/assets/2e998368-0bce-45dd-9248-cdd4e338c399" />

# Step 5: Data Visualisation

# Visualisation 1 - Line Graph

    import pandas as pd
    import streamlit as st
    from pandas.api.types import CategoricalDtype

    #Streamlit file uploader
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


# Visualisation 2: Pie chart
Note- Libraries such as matplot and pyplot were installed in the VScode terminal before running the code.
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

# Visualisation 3: Box-plot

	import streamlit as st
	import pandas as pd
	import plotly.express as px
	
	# Streamlit file uploader
 	df = pd.read_csv('your_data.csv')  # Load your CSV data
	
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


