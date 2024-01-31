from elasticsearch import Elasticsearch
from typing import List
import json
from elasticsearch.helpers import bulk

def write_elastic(client: Elasticsearch,res:List[str])->None:
    mappings = {
        "properties": {
            "name": {"type": "text"},
            "dateAdded": {"type": "date"},
            "dateUpdated": {"type": "date"},
            "brand": {"type": "text"},
            "categories": {"type": "text"},
            "colors": {"type": "text"},
            "dateAddedInt": {"type": "integer"},
            "dateUpdatedInt": {"type": "integer"}
        }
    }
    try:
        client.indices.delete(index="shoes")
    except:
        print("No index")
    client.indices.create(index="shoes",mappings=mappings)
    bulk_data=[]
    for i in range(len(res)):
        bulk_data.append({
            "_index": "shoes",
            "_id":i,
            "_source":json.loads(res[i])
        })
        # client.index(index="shoes",id=i,document=json.loads(res[i])) # for single entry writing
    bulk(client,bulk_data)
    client.indices.refresh(index="shoes")
    print(client.cat.count(index="shoes", format="json"))