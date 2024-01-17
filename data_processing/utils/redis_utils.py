import json
from typing import List
from redis import Redis
from redis.commands.search.field import NumericField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search import Search
def data_index(r:Redis,res:List[str])-> Search:
    try:
        r.ft("idx:shoes_index").dropindex(delete_documents=True)
    except:
        print("No index")
    print(len(res))
    for i in range(5):
        r.json().set("shoe:"+str(i+1), '$',  json.loads(res[i]))
    search_schema = (
        TextField("$.name", as_name="name"), 
        TextField("$.colors", as_name="colors"),
        NumericField("$.dateAddedInt", as_name="dateAddedInt"),
        NumericField("$.dateUpdatedInt", as_name="dateUpdatedInt")
    )
    rs_shoe = r.ft("idx:shoes_index")
    rs_shoe.create_index(
            fields=search_schema, 
            definition=IndexDefinition(
                prefix=["shoe:"], 
                index_type=IndexType.JSON
                )
            )
    return rs_shoe