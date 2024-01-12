
import datetime
import json
import requests
import random
import sqlalchemy

from multiprocessing import Process
from sqlalchemy import text
from time import sleep



random.seed(100)


class AWSDBConnector:
    """Class for connecting to an AWS RDS database.

    Attributes:
        HOST (str): The host address of the RDS instance.
        USER (str): The username for connecting to the database.
        PASSWORD (str): The password for connecting to the database.
        DATABASE (str): The name of the database.
        PORT (int): The port number for the database connection.

    Methods:
        create_db_connector: Creates and returns a SQLAlchemy engine for the database connection.
    """
    def __init__(self):
        """Initialize AWSDBConnector with default values."""
        self.HOST = "pinterestdbreadonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com"
        self.USER = 'project_user'
        self.PASSWORD = ':t%;yCY3Yjg'
        self.DATABASE = 'pinterest_data'
        self.PORT = 3306
        
    def create_db_connector(self):
        """Create and return a SQLAlchemy engine for the database connection.

        Returns:
            sqlalchemy.engine.base.Engine: SQLAlchemy engine for the database connection.
        """
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine


new_connector = AWSDBConnector()


def map_select_row(connection, random_row, table):
    """Select a random row from the specified table in the database.

    Args:
        connection (sqlalchemy.engine.base.Connection): SQLAlchemy database connection.
        random_row (int): Randomly selected row number.
        table (str): Name of the table to select the row from.

    Returns:
        dict: Dictionary containing the selected row's data.
    """
    select_row_string = text(f"SELECT * FROM {table} LIMIT {random_row}, 1")
    table_selected_row = connection.execute(select_row_string)
	
    for row in table_selected_row: 
        result_dict = dict(row._mapping)
		
    return result_dict


def convert_datetime(dict_result):
    """Convert datetime values in the dictionary to formatted strings.

    Args:
        dict_result (dict): Dictionary containing data with datetime values.

    Returns:
        dict: Dictionary with datetime values formatted as strings.
    """
    for key, value in dict_result.items():
        if type(value) == datetime.datetime:
            dict_result[key] = value.strftime("%Y-%m-%d %H:%M:%S")

    return dict_result



def run_infinite_post_data_loop(func):
    """Decorator function for running an infinite loop to post data.

    Args:
        func: The function to be wrapped.

    Returns:
        function: Wrapper function for running an infinite loop and invoking the specified function.
    """
    def wrapper(*args):
        while True:
            sleep(random.randrange(0, 2))
            random_row = random.randint(0, 11000)
            engine = new_connector.create_db_connector()

            with engine.connect() as connection:  #
            
                pin_result = map_select_row(connection, random_row, 'pinterest_data')
                geo_result = map_select_row(connection, random_row, 'geolocation_data')
                user_result = map_select_row(connection, random_row, 'user_data')

            #
                geo_result = convert_datetime(geo_result)
                user_result = convert_datetime(user_result)
                
            func(pin_result, geo_result, user_result, *args)

    return wrapper  
            


def api_send_to_kafka(invoke_url, header, table_dict): 
    """Send data to Kafka using the specified API.

    Args:
        invoke_url (str): URL for invoking the API.
        header (dict): HTTP headers for the API request.
        table_dict (dict): Dictionary containing data to be sent to Kafka.

    Returns:
        None
    """
      
	#To send JSON messages of table_dict
    payload_json = json.dumps({
            "records": [
                {
                # Data should be sent as pairs of column_name:value, with different columns separated by commas        
                "value": table_dict
                }
                ]
        })

    response_result = requests.request(method="POST", url=invoke_url, headers=header, data=payload_json)
    print(response_result.status_code)



def api_send_to_kinesis(invoke_url, header, table_dict, partition_key):
    """Send data to Kinesis using the specified API.

        Args:
            invoke_url (str): URL for invoking the API.
            header (dict): HTTP headers for the API request.
            table_dict (dict): Dictionary containing data to be sent to Kinesis.
            partition_key (str): Partition key for Kinesis stream.

        Returns:
            None
        """   
    # To send JSON messages you need to follow this structure
    payload_json = json.dumps({
        "StreamName": f"streaming-0a60b9a8a831-{partition_key}",
        "Data": table_dict,
        "PartitionKey": partition_key
    })

    response_result = requests.request(method="PUT", url=invoke_url, headers=header, data=payload_json)
    print(response_result.status_code)



#if __name__ == "__main__":
    #print(run_infinite_post_data_loop())
    #print('Working')
    
    


