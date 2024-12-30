# Guvi--Expense-Tracker
Mini project for Guvi class for analyzing personal expenses
Mini Project - Expense Tracker
Name - Ketki Potekar 
Batch - 
Date - 30/12/2024

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


