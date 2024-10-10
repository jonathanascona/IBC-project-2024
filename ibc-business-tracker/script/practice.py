import pandas as pd
import openpyxl

df = pd.read_excel('data\Student_Business_Test2.xlsx', sheet_name=["Daily Business Hours", "Inventory", "Sales", "Member Actions"])
dbh_df = df['Daily Business Hours']
inv_df = df["Inventory"]
sale_df = df["Sales"]
member_df = df["Member Actions"]

print(dbh_df)
print(inv_df)
print(sale_df)
print(member_df)
print(openpyxl.__version__)