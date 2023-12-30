import boto3
import datetime
import requests
import random
import json
import sqlalchemy

from multiprocessing import Process
from time import sleep
from sqlalchemy import text


random.seed(100)


class AWSDBConnector:

    def __init__(self):

        self.HOST = "pinterestdbreadonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com"
        self.USER = 'project_user'
        self.PASSWORD = ':t%;yCY3Yjg'
        self.DATABASE = 'pinterest_data'
        self.PORT = 3306
        
    def create_db_connector(self):
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine


new_connector = AWSDBConnector()


def map_select_row(connection, random_row, table):
	select_row_string = text(f"SELECT * FROM {table} LIMIT {random_row}, 1")
	table_selected_row = connection.execute(select_row_string)
	
	for row in table_selected_row: 
		result_dict = dict(row._mapping)
		
	return result_dict


def convert_datetime(dict_result):
	for key, value in dict_result.items():
		if type(value) == datetime.datetime:
			dict_result[key] = value.strftime("%Y-%m-%d %H:%M:%S")

	return dict_result



def run_infinite_post_data_loop(func):
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
      
	#To send JSON messages of table_dict
    payload_json = json.dumps({
            "records": [
                {
                #Data should be sent as pairs of column_name:value, with different columns separated by commas        
                "value": table_dict
                }
                ]
        })

    response_result = requests.request(method="POST", url=invoke_url, headers=header, data=payload_json)
    print(response_result.status_code)



def api_send_to_kinesis(invoke_url, header, table_dict, partition_key):
   
    #To send JSON messages you need to follow this structure
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
    
    


