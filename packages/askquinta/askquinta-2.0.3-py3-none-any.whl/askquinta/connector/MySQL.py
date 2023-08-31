import os
from timeout_decorator import timeout
from requests.exceptions import RequestException

import pandas as pd
import pymysql

CONNECTION_TIMEOUT = 10 # Max time in second if we can't connect to DB

class About_MySQL:
    """
    A class to handle the MySQL database connection and queries.

    Attributes:
        host (str): The host IP or domain name for the MySQL server.
        port (int): The port number for the MySQL server.
        user (str): The username to connect to the MySQL server.
        password (str): The password associated with the username.
        database_name (str): The name of the database to connect to.
        connection (pymysql.connections.Connection): The MySQL connection object.

    Methods:
        __init__(self, host, port, user, password, database_name):
            Initializes the MySQLConnection object with the provided connection details.

        connect(self):
            Establishes a connection to the MySQL database.

        close(self):
            Closes the MySQL database connection.

        to_pull_data(self, query):
            Executes a SQL query on the connected MySQL database and returns the result as a pandas DataFrame.
    """

    def __init__(self, host=None, port = None, username = None, password = None, database_name = None):
        """
        Initializes the MySQLConnection object with the provided connection details.

        Args:
            host (str): The host IP or domain name for the MySQL server.
                By default, the host will be obtained from the environment variable 'mysql_config_ip_host'.
            port (int): The port number for the MySQL server.
                By default, the port will be obtained from the environment variable 'mysql_config_ip_port'.
            username (str): The username to connect to the MySQL server.
                By default, the username will be obtained from the environment variable 'mysql_config_user_name'.
            password (str): The password associated with the username.
                By default, the password will be obtained from the environment variable 'mysql_config_user_password'.
            database_name (str): The name of the database to connect to.
                in Paper.id, you can pick one of these database_name:
                    - paper_invoicer
                    - paper_gateway
                    - paper_payment
        """
        self.host = host or os.getenv('mysql_config_ip_host')
        self.port = port or int(os.getenv('mysql_config_ip_port'))
        self.user = username or os.getenv('mysql_config_user_name')
        self.password = password or os.getenv('mysql_config_user_password')
        self.database_name = database_name
        self.connection = None
      
    def __dir__(self):
        """
        Customize the list of attributes/methods shown by dir().

        Returns:
            list: A list of attribute/method names to be displayed.
        """        
        return ['connect', 'close', 'to_pull_data', 'show_example']

    @timeout(CONNECTION_TIMEOUT)
    def connect(self):
        """
        Establishes a connection to the MySQL database.

        Raises:
            ConnectionError: If there is an error connecting to the MySQL database.
        """
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database_name
            )
            print("Successfully connected to {} database".format(self.database_name))
        except Exception as e:
            raise ConnectionError("Connection error: " + str(e))

    def close(self):
        """
        Closes the MySQL database connection.
        """
        if self.connection:
            self.connection.close()

    def to_pull_data(self, query):
        """
        Executes a SQL query on the connected MySQL database and returns the result as a pandas DataFrame.

        Args:
            query (str): The SQL query to be executed.

        Returns:
            pd.DataFrame: A DataFrame containing the result of the SQL query.

        Raises:
            ConnectionError: If the connection to the MySQL database is not established.
            ValueError: If there is an error executing the SQL query.
        """
        if not self.connection:
            #add auto connect
            self.connect()
            
            # raise ConnectionError("Not connected to the database.")

        try:
            query_result = pd.read_sql(query, self.connection)
        except Exception as e:
            raise ValueError("Error executing the query: " + str(e))

        return query_result
    
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
        MySQL = askquinta.About_MySQL(database_name='paper_invoicer/paper_payment/payment_gateway')
        
        # If environment variables are not set, you can set connection details manually
        MySQL = askquinta.About_MySQL(
            host='host',
            port=port,  # Replace with an integer port number
            username='your_username',
            password='password',
            database_name='dataset_name'
        )
        
        query = '''
            SELECT *
            FROM <your_table>
            LIMIT 10
        '''
        
        result = MySQL.to_pull_data(query)

        #dont forget to close the connection if you done
        MySQL.close()
                    """
        print(information)
