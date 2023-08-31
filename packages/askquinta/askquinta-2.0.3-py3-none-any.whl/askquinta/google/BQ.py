import os,re,time
import pandas as pd
from google.oauth2 import service_account
from pandas_gbq import to_gbq, read_gbq
from google.cloud import bigquery

class About_BQ:
    """
    A class to handle pulling and pushing data to Google BigQuery.

    Attributes:
        path (str): The path to the directory containing credentials.
        project_id (str): The Google Cloud project ID.
        credentials (Credentials): The Google Cloud credentials object.
    """
    def __init__(self, project_id=None, credentials_loc=None, location=None ):
        """
        Initialize the About_BQ class.

        Args:
            credentials_loc (str): The path to the directory containing credentials.
                By default, the credentials_loc will be obtained from the environment variable 'bq_creds_file'|'bq_config_testing_google_cred_location'|bq_config_prod_google_cred_location.
            project_id (str, optional): The Google Cloud project ID.
                By default, the project_id will be obtained from the environment variable 'bq_projectid'|bq_config_testing_projectid|bq_config_prod_projectid.
            location (str, optional): The Google Cloud project ID.
                By default, the location will be obtained from the environment variable 'bq_location'|bq_config_location or will be 'asia-southeast1'

        """

        self.credentials_loc = credentials_loc or os.getenv('bq_creds_file') or os.getenv('bq_config_testing_google_cred_location') or os.getenv('bq_config_prod_google_cred_location')
        self.project_id = project_id or os.getenv("bq_projectid") or os.getenv('bq_config_testing_projectid') or os.getenv('bq_config_prod_projectid')
        self.credentials = None
        self.location_bq = location or os.getenv('bq_location') or os.getenv('bq_config_location') or 'asia-southeast1'
        self.client = None  # Inisialisasi klien sebagai None
        
    def __dir__(self):
        """
        Customize the list of attributes/methods shown by dir().

        Returns:
            list: A list of attribute/method names to be displayed.
        """        
        return ['to_pull_data', 'to_push_data']

    def load_credentials(self):
        """
        Load Google Cloud credentials.

        Returns:
            Credentials: The Google Cloud credentials object.
        """
        
        if not self.credentials:
            self.credentials = service_account.Credentials.from_service_account_file(self.credentials_loc)
        return self.credentials

    def to_pull_data(self, query):
        """
        Pull data from Google BigQuery.

        Args:
            query (str): The SQL query to execute.

        Returns:
            pd.DataFrame: The pulled data as a DataFrame.
        """
        self.load_credentials()
        
        df = read_gbq(query, credentials=self.credentials, project_id=self.project_id, use_bqstorage_api=True)
        return df

    def to_push_data(self, data, dataset_name, table_name, if_exists):
        """
        Push data to Google BigQuery.
    
        This method allows you to push a pandas DataFrame to Google BigQuery.
        
        Args:
            data (pd.DataFrame): The data to push. The DataFrame to be pushed to BigQuery.
            dataset_name (str): The name of the BigQuery dataset where the data will be stored. example datascience or datascience_public
            table_name (str): The name of the BigQuery table to be created or updated.
            if_exist (str): Specifies behavior if the table already exists.
                - 'fail': Fails if the table already exists.
                - 'replace': Replaces the table if it already exists.
                - 'append': Appends the data to the existing table.
            
        Returns:
            None
            
        Raises:
            ValueError: If the `if_exist` parameter value is not one of 'fail', 'replace', or 'append'.
            
        Example:
            bq_handler = About_BQ(path='path_to_credentials_folder', project_id='your_project_id')
            data_to_push = pd.DataFrame({'column_1': [1, 2, 3], 'column_2': ['A', 'B', 'C']})
            bq_handler.to_push_data(data=data_to_push, dataset_name='datascience', table_name='my_table', if_exist='replace')
        
        Note:
            - The `dataset_name` should be an existing dataset in your Google BigQuery project.
            - The `table_name` will be created or updated based on the `if_exist` parameter.
            - Make sure you have the necessary credentials set up and loaded to use this method.
        """
        # Store to BQ 
        self.load_credentials()
        
        to_gbq(data, '{}.{}'.format(dataset_name, table_name),
               credentials=self.credentials,
               project_id=self.project_id,
               if_exists=if_exists,
               location=self.location_bq)

        print('{} data store to {}.{} with {} mode success'.format(data.shape, dataset_name, table_name, if_exists))
        
    def initialize_client(self):
        """
        Initialize the BigQuery client if not already initialized.

        Returns:
            Client: The initialized BigQuery client.
        """
        if not self.client:  # Inisialisasi hanya jika klien belum ada
            self.client = bigquery.Client(credentials=self.credentials, project=self.project_id)
        return self.client

    def to_update_data(self, dataset_name, table_name, update_values, condition, show = False):
        self.initialize_client()  # Memastikan klien diinisialisasi
        
        list_columns = list(set([i.split()[0].strip() for i in re.split(r'AND|OR', condition)]\
                                +list(update_values.keys())))
        query_pull = f"""
        select {', '.join(list_columns)} 
        from {self.project_id}.{dataset_name}.{table_name}
        WHERE {condition}
        
        """
        original_data = self.to_pull_data(query_pull)
        
        
        update_query = f"""
            UPDATE {self.project_id}.{dataset_name}.{table_name}
            SET {', '.join([f'{col} = {val}' for col, val in update_values.items()])}
            WHERE {condition}
        """
        
        print(update_query)
        self.client.query(update_query)
        print(f"Number of rows updated: {original_data.shape[0]}")
        if show:
            time.sleep(1)
            updated_data = self.to_pull_data(query_pull)
     
            print("Only a sample (10 data) is displayed below.")
            print('Before Updated')
            display(original_data[:10])

            print('After Updated')
            display(updated_data[:10])
            print("Note: If the data above doesnt change, you can verify it using the to_pull_data function, as BigQuery may require time to update the data.")

