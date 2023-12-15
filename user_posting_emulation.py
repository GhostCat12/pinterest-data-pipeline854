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


def run_infinite_post_data_loop():
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:

            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            
            for row in pin_selected_row:
                pin_result = dict(row._mapping)

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)

                
            
        # Convert any datetime values into string format                                                                                                         ### DOES NOT CURRENTLY FOLLOW DRY PRINCIPLES 
        for key, value in geo_result.items():

            if type(value) == datetime.datetime:
                geo_result[key] = value.strftime("%Y-%m-%d %H:%M:%S")


        # Convert any datetime values into string format                                                                                      ### DOES NOT CURRENTLY FOLLOW DRY PRINCIPLES    
        for key, value in user_result.items():

            if type(value) == datetime.datetime:
                user_result[key] = value.strftime("%Y-%m-%d %H:%M:%S")



        invoke_url_pin_result = "https://vqbq2ubp7a.execute-api.us-east-1.amazonaws.com/prod/topics/0a60b9a8a831.pin"
        invoke_url_geo_result = "https://vqbq2ubp7a.execute-api.us-east-1.amazonaws.com/prod/topics/0a60b9a8a831.geo"
        invoke_url_user_result = "https://vqbq2ubp7a.execute-api.us-east-1.amazonaws.com/prod/topics/0a60b9a8a831.user"

        #To send JSON messages of pin_result                                                                                               ### DOES NOT CURRENTLY FOLLOW DRY PRINCIPLES 
        payload_pin_result = json.dumps({
            "records": [
                {
                #Data should be send as pairs of column_name:value, with different columns separated by commas       
                "value": {"index": pin_result["index"], "unique_id": pin_result["unique_id"], "title": pin_result["title"], "description": pin_result["description"], 
                          "poster_name": pin_result["poster_name"], "follower_count": pin_result["follower_count"], "tag_list": pin_result["tag_list"], "is_image_or_video": pin_result["is_image_or_video"],
                          "image_src": pin_result["image_src"], "downloaded": pin_result["downloaded"], "save_location": pin_result["save_location"], "category": pin_result["category"]}
                }
            ]
        })


        #To send JSON messages of geo_result
        payload_geo_result = json.dumps({
            "records": [
                {
                #Data should be send as pairs of column_name:value, with different columns separated by commas       
                "value": {"ind": geo_result["ind"], "timestamp": geo_result["timestamp"], "latitude": geo_result["latitude"], "longitude": geo_result["longitude"], "country": geo_result["country"]}
                }
            ]
        })


        #To send JSON messages of user_result
        payload_user_result = json.dumps({
            "records": [
                {
                #Data should be send as pairs of column_name:value, with different columns separated by commas       
                "value": {"ind": user_result["ind"], "first_name": user_result["first_name"], "last_name": user_result["last_name"], "age": user_result["age"], "date_joined": user_result["date_joined"]}
                }
            ]
        })

        headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}

        response_pin_result = requests.request("POST", invoke_url_pin_result, headers=headers, data=payload_pin_result)                    ### DOES NOT CURRENTLY FOLLOW DRY PRINCIPLES 
        response_geo_result = requests.request("POST", invoke_url_geo_result, headers=headers, data=payload_geo_result)
        response_user_result = requests.request("POST", invoke_url_user_result, headers=headers, data=payload_user_result)
        print(response_pin_result.status_code)



if __name__ == "__main__":
    print(run_infinite_post_data_loop())
    print('Working')
    
    


