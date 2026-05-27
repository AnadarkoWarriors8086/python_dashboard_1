import streamlit as st
import pandas as pd
import numpy as np
import gspread 
import google.auth
from google.oauth2 import service_account

#This is for Google Authentication.
scope= ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_file('C:/Users/Racadio/Documents/Python_dashboard_1/client_secret.json', scopes=scope)
client = gspread.authorize(creds)

#This is for Page Configuration.
st.set_page_config(page_title='Jan-Mar 2026 Expenses', layout='wide')
tab1, tab2, tab3 = st.tabs(['Table View', 'KPIs', 'Charts'])

#This is to connect to the Google Sheet and put the data into a DataFrame.
with tab1:
    st.header('Table View')
    st.write('Jan-Mar 2026 Expenses - Table Views')
    selection = st.multiselect('Select the Expense Type:', ['Babysitting', 'Bills', 'Food', 'Fuel', 'House', 'prosper', 'tinker', 'Will Oil Change'], default=['Babysitting', 'Bills', 'Food', 'Fuel', 'House', 'prosper', 'Will Oil Change'])
    sheet = client.open('January/February/March Budget SpreadSheet for Python').sheet1
    data = sheet.get_all_records(expected_headers=['Type', 'Date', 'Amounts', 'Description'])
    df = pd.DataFrame(data)
    if selection:
        filtered_df = df[df['Type'].isin(selection)]
    else:
        filtered_df = df
    st.write(filtered_df)

with tab2:
    st.header('KPIs')
    st.write('Jan-Mar 2026 Expenses - KPIs')
    selection = st.multiselect('Select the Expense Type(s):', ['Babysitting', 'Bills', 'Food', 'Fuel', 'House', 'prosper', 'tinker', 'Will Oil Change'], default=['Babysitting', 'Bills', 'Food', 'Fuel', 'House', 'prosper', 'Will Oil Change'])
    if selection:
        filtered_df = df[df['Type'].isin(selection)]
        total_expenses_filtered = filtered_df['Amounts'].sum()
        st.metric(label='Total Expenses (Filtered)', value=f"${total_expenses_filtered:,.2f}")
    
with tab3:
    st.header('Charts')
    st.write('Jan-Mar 2026 Expenses - Charts')
    st.write('Bar Chart: Total Expenses by Type')
    st.bar_chart(df.groupby('Type')['Amounts'].sum())
    st.write('Line Chart: Expenses Over Time')
    selection = st.multiselect('Select the Expense Types:', ['Babysitting', 'Bills', 'Food', 'Fuel', 'House', 'prosper', 'tinker', 'Will Oil Change'], default=[])
    if selection:
        filtered_df = df[df['Type'].isin(selection)]
        st.line_chart(filtered_df.groupby('Date')['Amounts'].sum())