import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import numpy as np

SERVER_NAME = "your-server-name.database.windows.net"
DATABASE_NAME = "your-database-name"
DB_USER = "your-database-username"
DB_PASSWORD = "your-database-password"

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={SERVER_NAME};"
    f"DATABASE={DATABASE_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
    "Authentication=SqlPassword;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")

pd.set_option('display.max_columns', None)  # Show all columns

pd.set_option('display.width', None)  # Show full width
df = pd.read_sql("SELECT Id, OrderCode, Quantity, TotalAmount, Status FROM dbo.OrderDetail WHERE Status NOT IN ('Cancel') AND TotalAmount > 0", engine)

df['OderType'] = np.where(df['Quantity'] >= 10, 'Bulk', 'Retail')


df['OrderID'] = df['Id'] - 19471
#Row ID start from 19472 and increase so I delete by 19471 to get Row ID starting 1

summary_df = df.groupby('OderType')['TotalAmount'].sum().reset_index()

# 2. Calculate total revenue of entire system
total_revenue = df['TotalAmount'].sum()

# 3. Calculate percentage (Eg: 45.2%)
summary_df['Percentage'] = (summary_df['TotalAmount'] / total_revenue) * 100

# 4. Display result
print("\n--- Revenue Summary Table Based On Order Type ---")
print(summary_df)
