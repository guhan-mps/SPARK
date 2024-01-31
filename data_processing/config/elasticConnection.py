from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

def elastic_connect():
    load_dotenv()
    """
    Create a python client to the Elastic search deployment using the deployment's cloud_id, the username and password
    for the elastic search service account
    """
    client = Elasticsearch(
        cloud_id=os.getenv('CLOUD_ID'),
        basic_auth=(os.getenv('ELASTIC_USER'), os.getenv('ELASTIC_PASSWORD'))
    )
    return client