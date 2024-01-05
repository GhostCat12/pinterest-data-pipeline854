# Pinterest Data Pipeline



## Table of Contents

1. Project Overview
1. Installation and usage instructions 
1. Pipeline architecture
1. File structure of the project
1. Data
1. The Pipeline Build
1. License information


## Project overview: 

Pinterest is a visual discovery engine designed to provide ideas and inspiration. As each user interacts through viewing posts, following or uploading, Pinterest crunches billions of data points every day to decide how to provide more value to their users. 


This project aims to design an end-to-end pipeline utilising AWS cloud technologies and Databricks for analysing real-time and historical pinterest-emulated data.


## Installation and usage instructions
   
### Installation    
   For conda environment dependencies the `pinterest_pipeline.yaml` can be cloned.  

    conda env create -f pinterest_pipeline.yaml
    conda activate pinterest_pipeline 
   
**Note:** Due to confidential information for AWS and Databricks account access, this project cannot be run by others directly, however can function as a step by step guide on replicating the pipeline.  

### Tools and dependencies

- **Apache Kafka :**  
 Apache kafka is an unified event streaming platform for handling all real-time data feeds (for example, Internet of Thing sensors and smartphones). It combines messaging, storage, and stream processing to allow storage and analysis of both historical and real-time data. The documention can be found [here](https://kafka.apache.org/documentation/). 

- **AWS MSK :**   

- **AWS MSK Connect :**   

- **Kafka REST Proxy :**  

- **AWS API Gateway :**   

- **PySpark :**   

- **Apache Spark :**  

- **AWS MWAA (Managed Workflow for Apache Airflow) :**    

- **AWS Kinesis :**   

- **Databricks :**    


- **AWS EC2 :**   

- **AWS RDS :**   

- **AWS S3 :**    

 

## Pipeline architecture



## File structure of the project

1. **Project Log:** Contains a journey log of all steps taken.
2. **user_posting emulation.py :** A script which emulates the stream of POST requests by users on Pinterest.   
Contains the following : 
    - AWSDBConnector : (Class) Connects to an AWS RDS database  
        - create_db_connector : (Method) Creates and returns a SQLAlchemy engine for the database connection. 
    - map_select_row : (Function) Select a random row from the specified table in the database
    - convert_datetime: (Function) Convert datetime values in the dictionary to formatted strings.
    - run_infinite_post_data_loop : (Wrapper) Decorator function for running an infinite loop to post data.
    - api_send_to_kafka : (Function) Send data to Kafka using the specified API.
    - api_send_to_kinesis : (Function) Send data to Kinesis using the specified API.


3. user_posting emulation_batch.py : A script to post user, geo, and pin data to Kafka.
    - kafka_post: (Function) Calls api_send_to_kafka. Posts data to Kafka topics using the specified API endpoints.    
4. user_posting emulation_streaming.py : A script to post user, geo, and pin data to Kinesis.
    - kinesis_stream_post : (Function) Calls api_send_to_kinesis function. Posts data to Kinesis streams using the specified API endpoints.
5. data_frame_creation_from_s3_bucket.ipynb : Databricks notebook to authenticate, mount s3 bucket, and create dataframes.  
6. cleaning_df_batch_data.ipynb : Databricks notebook to clean batch dataframes. 
7. querying_batch_data.ipynb : Databricks notebook to query batch data.


## Data 

Infrastructure similar to what is found if data engineer working at Pinterest. 

user_posting_emulation.py, that contains the login credentials for a RDS database, which contains three tables with data resembling data received by the Pinterest API when a POST request is made by a user uploading data to Pinterest:

### **pinterest_data :** contains data about posts being updated to Pinterest
    
> Example data:

    {'index': 7528, 'unique_id': 'fbe53c66-3442-4773-b19e-d3ec6f54dddf', 'title': 'No Title Data Available', 'description': 'No description available Story format', 'poster_name': 'User Info Error', 'follower_count': 'User Info Error', 'tag_list': 'N,o, ,T,a,g,s, ,A,v,a,i,l,a,b,l,e', 'is_image_or_video': 'multi-video(story page format)', 'image_src': 'Image src error.', 'downloaded': 0, 'save_location': 'Local save in /data/mens-fashion', 'category': 'mens-fashion'}


### **geolocation_data :** contains data about the geolocation of each Pinterest post found in pinterest_data

> Example data:

    {'ind': 7528, 'timestamp': datetime.datetime(2020, 8, 28, 3, 52, 47), 'latitude': -89.9787, 'longitude': -173.293, 'country': 'Albania'}
### **user_data contains :** data about the user that has uploaded each post found in pinterest_data

> Example data:

    {'ind': 7528, 'first_name': 'Abigail', 'last_name': 'Ali', 'age': 20, 'date_joined': datetime.datetime(2015, 10, 24, 11, 23, 51)}


## The Pipeline Build  


### Details of steps taken can be found in the `project_log.ipynb`file. 

### 1. Setting up project environment 

### 2. Exploring the Pinterest emulation data. As shown under the [Data](#data) section. 

### 3. Configuring EC2 Kafka client

### 4. Connect MSK cluster to an S3 bucket

### 5. Configuring API in API gateway

### 6. Mounting AWS S3 bucket onto Databricks

In order to clean and query the batch data, mounting the S3 bucket on Databricks is required. Therefore, `data_frame_creation_from_s3_bucket.ipynb` was run in Databricks: 

1. Read the credentials .csv into a Sparks dataframe
2. Created variables using AWS access key and secret key from the spark dataframe
3. Mounted the S3 bucket using credentials
4. Creates a three Spark dataframes, one for each topic (user, pin, and geo)
5. Read the .json files into three Spark dataframes


### 7. Cleaning the three dataframes: 
- df_pin
- df_geo 
- df_user   

detailed steps can be found in `cleaning_df_batch_data.ipynb` file

### 8. Querying batch data on Databricks using pyspark.
Detailed steps can be seen in `querying_batch_data.ipynb` file. Queries were as follows:

1. Find the most popular Pinterest category people post to based on their country.
2. Find the most popular category in each year between 2018 and 2022
3. Find the user with most followers in each country
4. What is the most popular category people post to for different age groups?
5. What is the median follower count for users in different age groups?
6. Find how many users have joined each year between 2015 and 2020
7. Find the median follower count of users based on their joining year between 2015 and 2020.
8. Find the median follower count of users based on their joining year and age group for 2015 to 2020.  

### 9. Batch processing: AWS MWAA    
Utilising AWS Managed Workflows for Apache Airflow (MWAA) to automate **daily** batch processing of the previously created databricks notebook. 

Uploading the `0a60b9a8a831_dag.py` directed acyclic graph (DAG) file to the S3 bucket `mwaa-dags-bucket/dags` associated with the MWAA environment. This allows us to run the DAG from the AWS airflow UI. 

### 10. Stream Processing: AWS Kinesis

Created 3 streams each sourcing data from one the 3 Pinterest data tables :     
1. streaming-0a60b9a8a831-pin  
2. streaming-0a60b9a8a831-geo    
3. streaming-0a60b9a8a831-user 



## License information




