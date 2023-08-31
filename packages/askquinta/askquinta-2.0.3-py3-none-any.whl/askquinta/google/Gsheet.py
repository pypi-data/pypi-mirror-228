import pandas as pd
from gspread import authorize
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

class About_Gsheet:
    def __init__(self, credentials_path):
        """
        Initializes the About_Gsheet object.

        Args:
            credentials_path (str): Path to the JSON credentials file.

        Returns:
            About_Gsheet: The initialized About_Gsheet object.
        """
        self.credentials_path = credentials_path
        self.client = self.connect()

    def connect(self):
        """
        Authorizes the connection to Google Sheets API.

        Returns:
            gspread.Client: Authorized client object for interacting with Google Sheets.
        """
        
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_path, 
                                                                      ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
        return authorize(self.creds)

    def to_push_data(self, data, spreadsheet_name, worksheet_name="Sheet1", append=True, folder_id=None):
        """
        Pushes data to a specified worksheet in the Google Sheets spreadsheet.

        Args:
            data (dataframe): List of rows to be added to the worksheet.
            spreadsheet_name (str): Name or URL of the spreadsheet.
            worksheet_name (str, optional): Name of the worksheet to add data to.
            folder_id (str, optional): ID of the folder to move the spreadsheet to.
            append (bool): If True, append data to the worksheet. If False, replace existing data.

        Returns:
            None
        """

        if "https://docs.google.com/spreadsheets/" in spreadsheet_name:
            spreadsheet = self.client.open_by_url(spreadsheet_name)
        else:
            try:
                spreadsheet = self.client.open(spreadsheet_name)
            except SpreadsheetNotFound:
                # Jika belum ada, buat spreadsheet baru
                spreadsheet = self.client.create(spreadsheet_name)
                spreadsheet.share('', perm_type='anyone', role='writer')

        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except WorksheetNotFound:
            # Jika belum ada, buat worksheet baru
            worksheet = spreadsheet.add_worksheet(worksheet_name, rows=1, cols=1)

        if append:
            # Calculate the next available row index
            next_row_index = len(worksheet.col_values(1))+1
            # Paste the data into the worksheet starting from the next available row
            worksheet.update(f'A{next_row_index}', data.values.tolist())
            
        else:
            worksheet.clear()
            data_values = data.values.tolist()
            data_values.insert(0, data.columns.tolist())  # Add column headers
            worksheet.update(data_values)
            
        if folder_id:
            drive_service = build('drive', 'v3', credentials=self.creds)
            file = drive_service.files().get(fileId=spreadsheet.id, fields='parents').execute()
            previous_parents = ",".join(file.get('parents'))
            drive_service.files().update(fileId=spreadsheet.id, addParents=folder_id, removeParents=previous_parents).execute()

        print(f"Push data to {spreadsheet.url} completed")

    def to_pull_data(self, spreadsheet_name, worksheet_name='Sheet1'):
        """
        Pulls data from a specified worksheet in the Google Sheets spreadsheet.

        Args:
            spreadsheet_name (str): Name or URL of the spreadsheet.
            worksheet_name (str): Name of the worksheet to retrieve data from.

        Returns:
            DataFrame: List of rows containing the data from the worksheet.
        """
        if "https://docs.google.com/spreadsheets/" in spreadsheet_name:
            spreadsheet = self.client.open_by_url(spreadsheet_name)
        else:
            try:
                spreadsheet = self.client.open(spreadsheet_name)
            except SpreadsheetNotFound:
                raise SpreadsheetNotFound(f"Spreadsheet {spreadsheet_name} Not Found")
            
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except WorksheetNotFound as e:
            raise WorksheetNotFound(f"Worksheet '{worksheet_name}' not found in the spreadsheet.")
        data = worksheet.get_all_values()
        return pd.DataFrame( data[1:], columns=data[0])

    def to_update_data(self, data, spreadsheet_name, cell_range, worksheet_name='Sheet1'):
        """
        Updates data in a specified range of cells in the Google Sheets spreadsheet.

        Args:
            data (list): List of rows to be updated in the specified cell range.
            spreadsheet_name (str): Name or URL of the spreadsheet.
            worksheet_name (str): Name of the worksheet to update data in.
            cell_range (str): Range of cells to be updated (e.g., 'A1:B2').

        Returns:
            None
        """
        if "https://docs.google.com/spreadsheets/" in spreadsheet_name:
            spreadsheet = self.client.open_by_url(spreadsheet_name)
        else:
            try:
                spreadsheet = self.client.open(spreadsheet_name)
            except SpreadsheetNotFound:
                raise SpreadsheetNotFound(f"Spreadsheet {spreadsheet_name} Not Found")
                
        worksheet = spreadsheet.worksheet(worksheet_name)
        worksheet.update(cell_range, data, value_input_option='RAW')
        print(f"Spreadsheet {spreadsheet.url} updated")
