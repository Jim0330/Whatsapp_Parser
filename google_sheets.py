import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet(spreadsheet_id, sheet_name='Sheet1'):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
    return sheet

def append_row(spreadsheet_id, row, sheet_name='Sheet1'):
    sheet = get_sheet(spreadsheet_id, sheet_name)
    sheet.append_row(row, value_input_option='USER_ENTERED')
