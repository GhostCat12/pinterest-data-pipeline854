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
Amazon Managed Streaming for Apache Kafka (MSK) is a fully managed service that enables you to build and run applications that use Apache Kafka to process streaming data. The guide can be found [here](https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html).

- **AWS MSK Connect :**  
MSK connect is a feature of Amazon MSK, that makes it easy for developers to stream data to and from their Apache Kafka clusters. It uses the Kafka Connect framework for connecting Apache Kafka clusters with external systems such as databases, search indexes, and file systems. The guide can be found [here](https://docs.aws.amazon.com/msk/latest/developerguide/msk-connect-getting-started.html).

- **Kafka REST Proxy :**  
The Confluent REST Proxy provides a RESTful interface to an Apache Kafka® cluster, making it easy to produce and consume messages, view the state of the cluster, and perform administrative actions without using the native Kafka protocol or clients. The guide can be found [here](https://docs.confluent.io/platform/current/kafka-rest/index.html).

- **AWS API Gateway :**  
Amazon API Gateway is a fully managed service for creating, publishing, maintaining, monitoring, and securing APIs at any scale. APIs act as the "front door" for applications to access data, business logic, or functionality from your backend services. The documentation can be found [here](https://docs.aws.amazon.com/apigateway/)


- **Apache Spark :**  
Apache Spark is a unified analytics engine for large-scale data processing. It provides high-level APIs in multiple languages and an optimized engine that supports general execution graphs.
It also contains higher-level tools including Spark SQL, pandas API on Spark, MLib, GraphX, and Structure Streaming. All documentation can be found [here](https://spark.apache.org/documentation.html) 

- **PySpark :**  
PySpark is the Python API for Apache Spark, used to process data with Spark in Python. It supports all of the features mentioned in Apache Spark. [here](https://spark.apache.org/docs/latest/api/python/index.html)


- **AWS MWAA :**  
Amazon Managed Workflows for Apache Airflow (MWAA) is a managed orchestration service for Apache Airflow that sets up and operates data pipelines in the cloud at scale. programmatically author, schedule, and monitor sequences of processes and tasks referred to as workflows.
[here](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html)


- **AWS Kinesis :**  
Amazon Kinesis is used to capture, process, and store video and data streams in real-time for analytics and machine learning. The documentation can be found [here](https://docs.aws.amazon.com/kinesis/)

- **Databricks :**  
The Databricks Lakehouse platform can be used for building, deploying, sharing, and maintaining enterprise-grade data, analytics, and AI solutions at scale. It performs Spark processing of batch and streaming data. The documentation can be found [here](https://docs.databricks.com/en/index.html)

- **AWS EC2 :**  
Amazon Elastic Compute Cloud (Amazon EC2) provides on-demand, scalable computing capacity in the Amazon Web Services (AWS) Cloud. It can launch virtual servers, configure security and networking, and manage storage. The documentation can be found [here](https://docs.aws.amazon.com/ec2/)

- **AWS RDS :**  
Amazon Relational Database Service is a web service that makes it easier to set up, operate, and scale a relational database in the AWS Cloud. The documentation can be found [here](https://docs.aws.amazon.com/rds/)
 

## Pipeline architecture


## File structure of the project

1. **Project Log:** Contains a journey log of all steps taken.
2. **user_posting_emulation.py :** A script which emulates the stream of POST requests by users on Pinterest.   
Contains the following : 
    - AWSDBConnector : (Class) Connects to an AWS RDS database  
        - create_db_connector : (Method) Creates and returns a SQLAlchemy engine for the database connection. 
    - map_select_row : (Function) Select a random row from the specified table in the database
    - convert_datetime: (Function) Convert datetime values in the dictionary to formatted strings.
    - run_infinite_post_data_loop : (Wrapper) Decorator function for running an infinite loop to post data.
    - api_send_to_kafka : (Function) Send data to Kafka using the specified API.
    - api_send_to_kinesis : (Function) Send data to Kinesis using the specified API.


3. user_posting_emulation_batch.py : A script to post user, geo, and pin data to Kafka.
    - kafka_post: (Function) Calls api_send_to_kafka. Posts data to Kafka topics using the specified API endpoints.    
4. user_posting_emulation_streaming.py : A script to post user, geo, and pin data to Kinesis.
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
    - Setup a conda enviroment and install required libraires 

### 2. Exploring the Pinterest emulation data. As shown under the [Data](#data) section. 

### 3. Batch processing: Configuring EC2 Kafka client
    - Create MSK cluster, a client is needed to communicate with this MSK cluster. In this project, an EC2 instance is used to act as the client.
    - Create EC2 instance
    - Use key pair of EC2 instance to create .pem file locally to connect securely to EC2 via SSH
    - In order for the client machine to connect to the cluster, edit the inbound rules for the security group associated with MSK cluster
    - Install Java and Kafka on EC2 client machine 
    - Install IAM MSK authentication package to connect to MSK clusters to authenticate the client
    - Configure the client classpath environment variable to be able to use the IAM package
    - Authenticate MSK cluster using EC2 IAM role 
    - Configure Kafka client to use AWS IAM authentication to the cluster
    - Create 3 Kafka topics on the kafka cluster 

### 4. Connect MSK cluster to an S3 bucket
    - Download the Confluent.io Amazon S3 Connector and copy it to the S3 bucket in the EC2 client machine 
    - Create custom plugin in the MSK Connect console
    - Create a connector in MSK connect using custom plugin to connect to S3

### 5. Configuring API in API gateway
    - Create a REST API
    - Create a resource that allows building a PROXY integration for the API and setup a HTTP any method onto it
    - Deploy the API
    - Install Confluent package to setup a REST proxy API on EC2 which listens for requests and interacts with the kafka cluster 
    - Allow the REST proxy to perform IAM authentication to MSK cluster by modifying the kafka-rest.properties file
    - Start the REST proxy on the EC2 client machine
    - By running user_posting_emulation_batch_data.py which posts data messages to the cluster via the API gateway and the kafka REST proxy


### 6. Mount AWS S3 bucket onto Databricks

In order to clean and query the batch data, mounting the S3 bucket on Databricks is required. Therefore, `data_frame_creation_from_s3_bucket.ipynb` was run in Databricks: 

1. Read the credentials .csv into a Sparks dataframe
2. Create variables using AWS access key and secret key from the spark dataframe
3. Mount the S3 bucket using credentials
4. Create three Spark dataframes, one for each topic (user, pin, and geo)
5. Read the .json files into three Spark dataframes


### 7. Clean the three dataframes and query the data on databricks using puspark : 
Clean df_pin, df_geo, df_user

Detailed steps can be found in `cleaning_df_batch_data.ipynb` file
Queries were as follows:

1. Find the most popular Pinterest category people post to based on their country.
2. Find the most popular category in each year between 2018 and 2022
3. Find the user with most followers in each country
4. What is the most popular category people post to for different age groups?
5. What is the median follower count for users in different age groups?
6. Find how many users have joined each year between 2015 and 2020
7. Find the median follower count of users based on their joining year between 2015 and 2020.
8. Find the median follower count of users based on their joining year and age group for 2015 to 2020.

Detailed steps can be seen in `querying_batch_data.ipynb` file.


### 8. Batch processing: AWS MWAA 
    -create MWAA enviroment linked to an S3 bucket
    - Upload the `0a60b9a8a831_dag.py` directed acyclic graph (DAG) file to the S3 bucket `mwaa-dags-bucket/dags` associated with the MWAA environment. This allows us to run the DAG from the AWS airflow UI
    - Utilise AWS Managed Workflows for Apache Airflow (MWAA) to automate **daily** batch processing of the previously created databricks notebook. 

### 9. Stream Processing: AWS Kinesis

    -Create 3 streams each sourcing data from one the 3 Pinterest data tables :     
        1. streaming-0a60b9a8a831-pin  
        2. streaming-0a60b9a8a831-geo    
        3. streaming-0a60b9a8a831-user 
    - Configure your previously created REST API to allow it to invoke Kinesis actions
    - API should be able to invoke the following actions:
        1. List streams in Kinesis
        2. Create, describe and delete streams in Kinesis
        3. Add records to streams in Kinesis
    -Create a new script user_posting_emulation_streaming.py to send requests to the API, which adds one tables record at a time to the coresponding kinesis streams created.
    -Read data from Kinesis streams into Databricks
    -Clean the streaming data in the same way as the batch data
    -Write streaming data into Databricks delta tables


## License information




