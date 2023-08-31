import os
from timeout_decorator import timeout
from requests.exceptions import RequestException

import pandas as pd
from pyArango.connection import Connection

# ============================================================
# Config Do not Touch
# ============================================================
CONNECTION_TIMEOUT = 10 # Max time in second if we can't connect to DB

class About_ArangoDB:
    """
    A class to handle the connection to ArangoDB and perform queries.

    Attributes:
        arango_url (str): The URL of the ArangoDB server.
        username (str): The username to connect to the ArangoDB server.
        password (str): The password associated with the username.
        connection (pyArango.connection.Connection): The ArangoDB connection object.

    Methods:
        __init__(self, arango_url, username, password):
            Initializes the ArangoDBConnection object with the provided connection details.

        connect(self):
            Establishes a connection to the ArangoDB server.

        close(self):
            Closes the connection to the ArangoDB server.

        query(self, collection_name, query_codes):
            Executes an AQL query on a specific collection and returns the result as a DataFrame.
    """

    def __init__(self, arango_url = None, username = None, password = None):
        """
        Initializes the ArangoDBConnection object with the provided connection details.

        Args:
            arango_url (str): The URL of the ArangoDB server.
                By default, the arango_url will be obtained from the environment variable 'arango_replicate_config_url'.
            username (str): The username to connect to the ArangoDB server.
                By default, the username will be obtained from the environment variable 'arango_replicate_config_username'.
            password (str): The password associated with the username.
                By default, the password will be obtained from the environment variable 'arango_replicate_config_password'.
        """
        self.arango_url = arango_url or os.getenv('arango_replicate_config_url')
        self.username = username or os.getenv('arango_replicate_config_username')
        self.password = password or os.getenv('arango_replicate_config_password')
        self.connection = None

    @timeout(CONNECTION_TIMEOUT)
    def connect(self):
        """
        Establishes a connection to the ArangoDB server.

        Raises:
            ConnectionError: If there is an error connecting to the ArangoDB server.
        """
        try:
            self.connection = Connection(arangoURL=self.arango_url,
                                         username=self.username, 
                                         password=self.password)
            print("Successfully connected to ArangoDB server.")
          
        except RequestException as e:
            raise ConnectionError("Connection error: " + str(e))

    def to_pull_data(self, collection_name, query, batch_size = 100):
        """
        Executes an AQL query on a specific collection and returns the result as a DataFrame.

        Args:
            collection_name (str): The name of the ArangoDB collection to query.
            query (str): The AQL query codes to be executed.
            batch_size (int): Total rows will be gathered, such as LIMIT 100

        Returns:
            pd.DataFrame: A DataFrame containing the result of the AQL query.

        Raises:
            ConnectionError: If the connection to the ArangoDB server is not established.
        """
        # Try to connect
        if not self.connection:
            self.connect()
        collection_connection = self.connection[collection_name]
        # Config the connection
        query_result = collection_connection.AQLQuery(query, batchSize = int(batch_size)).response['result']
        return pd.DataFrame(query_result)
    
    def show_attributes(self):
        """
        Displays the values of the class attributes.
        """
        print("arango_url:", self.arango_url)
        print("username:", self.username)
        print("password:", self.password)
        print("connection:", self.connection)
    
    def show_example(self):
        """
        Display the usage of this Class
        """
        information = """
        #=========================================================
        # Usage Example
        #=========================================================
        
        import askquinta
        # Set up the About_MySQL object with environment variables if available
        ArangoDB = askquinta.About_ArangoDB()

        # If environment variables are not set, you can set connection details manually
        arango_url = os.getenv("arango_replicate_config_url")
        username = os.getenv("arango_replicate_config_username")
        password = os.getenv("arango_replicate_config_password")

        ArangoDB = askquinta.About_ArangoDB(arango_url, username, password)

        #Pull Data
        ArangoDB.to_pull_data(collection_name, query, batch_size)
        """
        print(information)
