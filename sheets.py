import gspread
import pandas as pd
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run_flow
from datetime import datetime

# Step 1: Authenticate with your Google Account using OAuth
def get_worksheet():
    CLIENT_SECRET = 'client_secret.json' 
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive']
    TOKEN_FILE = 'token.json'  # Used to store login credentials

    storage = Storage(TOKEN_FILE)
    creds = storage.get()

    if not creds or creds.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
        creds = run_flow(flow, storage)

    gc = gspread.authorize(creds)

    # Step 2: Open the spreadsheet from your Google Drive
    sh = gc.open('discord bot reminder')  # Replace with the actual spreadsheet name
    worksheet = sh.sheet1
    return worksheet

# Step 3: Load spreadsheet data into a DataFrame
def load_google_sheet():
    worksheet = get_worksheet()
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

# Update task status if work is done
def update_status(discord_id, task_name, new_status):
    worksheet = get_worksheet()
    records = worksheet.get_all_records()
    
    for i, row in enumerate(records):
        if str(row["discord_id"]) == str(discord_id) and row["task"] == task_name:
            worksheet.update_cell(i + 2, get_column_index(worksheet, "status"), new_status)
            break

# Update task due date if new due date provided
def update_due_date(discord_id, task_name, new_due_date):
    worksheet = get_worksheet()
    records = worksheet.get_all_records()
    
    for i, row in enumerate(records):
        if str(row["discord_id"]) == str(discord_id) and row["task"] == task_name:
            worksheet.update_cell(i + 2, get_column_index(worksheet, "due_date"), new_due_date)
            break

# Helper function to get column index
def get_column_index(worksheet, column_name):
    headers = worksheet.row_values(1)
    return headers.index(column_name) + 1

#A helper function that ensure the format of the deadlines are correct
def parse_due_date(date_str: str):
    """Try to parse a date string in multiple formats."""
    formats = ["%d-%m-%Y %H:%M", "%d-%m-%Y"]  # change if want different format
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {date_str}. Please use DD-MM-YYYY HH:MM")

if __name__ == "__main__":
    df = load_google_sheet()
    print(df.head()) 
