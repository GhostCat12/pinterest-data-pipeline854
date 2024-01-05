from user_posting_emulation import *


# invoke url for one record, if you want to put more records replace record with records
invoke_url_pin_result = "https://vqbq2ubp7a.execute-api.us-east-1.amazonaws.com/prod/streams/streaming-0a60b9a8a831-pin/record"
invoke_url_geo_result = "https://vqbq2ubp7a.execute-api.us-east-1.amazonaws.com/prod/streams/streaming-0a60b9a8a831-geo/record"
invoke_url_user_result = "https://vqbq2ubp7a.execute-api.us-east-1.amazonaws.com/prod/streams/streaming-0a60b9a8a831-user/record"


headers = {'Content-Type': 'application/json'}


@run_infinite_post_data_loop
def kinesis_stream_post(pin_result, geo_result, user_result):
    """Post data to Kinesis streams using the specified API endpoints.

    Args:
        pin_result (dict): Dictionary containing Pinterest data.
        geo_result (dict): Dictionary containing geolocation data.
        user_result (dict): Dictionary containing user data.

    Returns:
        None
    """
    payload_pin_result = api_send_to_kinesis(invoke_url_pin_result, headers, table_dict=pin_result, partition_key="pin")
    payload_geo_result = api_send_to_kinesis(invoke_url_geo_result, headers, table_dict=geo_result, partition_key="geo")
    payload_user_result = api_send_to_kinesis(invoke_url_user_result, headers, table_dict=user_result, partition_key="user")

kinesis_stream_post()