from user_posting_emulation import *


       
invoke_url_pin_result = "https://vqbq2ubp7a.execute-api.us-east-1.amazonaws.com/prod/topics/0a60b9a8a831.pin" # specifically for batch kafka 
invoke_url_geo_result = "https://vqbq2ubp7a.execute-api.us-east-1.amazonaws.com/prod/topics/0a60b9a8a831.geo"
invoke_url_user_result = "https://vqbq2ubp7a.execute-api.us-east-1.amazonaws.com/prod/topics/0a60b9a8a831.user"


headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'} #inside kafka file
 
@run_infinite_post_data_loop
def kafka_post(pin_result, geo_result, user_result):
    
    payload_pin_result = api_send_to_kafka(invoke_url_pin_result, header=headers, table_dict=pin_result)
    payload_geo_result = api_send_to_kafka(invoke_url_geo_result, header=headers, table_dict=geo_result)
    payload_user_result = api_send_to_kafka(invoke_url_user_result, header=headers, table_dict=user_result)


kafka_post()