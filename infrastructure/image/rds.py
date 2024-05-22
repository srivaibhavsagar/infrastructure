#!/usr/bin/python

import pymysql
import os
import sys
import boto3

import boto3,json
from botocore.exceptions import ClientError


def get_secret(region_name,secret_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        error = ("Unable to get the credentials")
        raise Exception(error)

    secret = get_secret_value_response['SecretString']
    print(secret)

    return json.loads(secret)

try:
  secret_name = os.environ['secret_name']
  region_name = os.environ['region']
  print(f"Region found from environment variable is: {region_name}")
  print(f"Secret found from environment variable is: {secret_name}")
  secrets = get_secret(region_name,secret_name)
  Database_endpoint = secrets["host"]
  print(Database_endpoint)
  Username = secrets["username"]
  Password = secrets["password"]
except Exception as e:
   raise e

try:
  print("Connecting to " + Database_endpoint)
  db = pymysql.connect(host = Database_endpoint, user = Username, password = Password,port=3306)
  print("Connection successful to " + Database_endpoint)
  db.close()
except Exception as e:
  print("Connection unsuccessful due to " + str(e))