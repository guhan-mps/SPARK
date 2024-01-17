import redis
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.json.path import Path
from redis.commands.search.field import NumericField, TagField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

"""
Connection to redis server
"""
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

"""
Clean up already created indices
"""
#r.flushall()
r.ft("idx:users_comma").dropindex(delete_documents=True)

"""
Data to be cached in redis
"""
user1 = {
    "name": "Paul John",
    "email": "paul.john@example.com",
    "age": 42,
    "city": "London, Chennai, Akihabara, Fuyuki city"
}
user2 = {
    "name": "Eden Zamir",
    "email": "eden.zamir@example.com",
    "age": 29,
    "city": "Tel Aviv"
}
user3 = {
    "name": "Paul Zamir",
    "email": "paul.zamir@example.com",
    "age": 35,
    "city": "Tel Aviv"
}

"""
Schema for index creation
"""
search_schema = (
    TextField("$.name", as_name="name",weight=5.0), 
    TagField("$.city", as_name="city"), 
    NumericField("$.age", as_name="age")
)

"""
Write the data as json into redis
"""
r.json().set("user:1", '$',  user1)
r.json().set("user:2", Path.root_path(),  user2)
r.json().set("user:3", Path.root_path(),  user3)

"""
Create Index(namely users_comma) for the name, city, age fields of the json data with prefix in their name as 'user:'
"""
rs_user = r.ft("idx:users_comma")
rs_user.create_index(
        fields=search_schema, 
        definition=IndexDefinition(
            prefix=["user:"], 
            index_type=IndexType.JSON
            )
        )
"""
Search for a prefix in a TextField. If exact word's presence is needed to be searched in a sentence replace * wildcard with exact word
"""
res=rs_user.search(Query("@name:Pau*").return_field("$.city")).docs
#print(res)

"""
Fuzzy search: Search that can guess the searched word, if left a typo of single character. If two characters are mismatched to the actual search word \
provide double %.  
"""
res=rs_user.search(Query("@name:%Pal%").return_field("$.name",as_field="name")).docs
#print(res)

"""
Search for a value within a range in NumericField. Sort it and display only the fields needed to be shown in the result. Then limit the number of output 
displayed from the required starting offset
"""
res=rs_user.search(Query("@age:[20 50]").sort_by("age").return_fields("$.name","AS","name","$.age","AS","age").paging(0,1))
#print(res)

"""
Search a value in a TagField.
"""
res=rs_user.search(Query("@city:{Tel*}").return_field("$.city", as_field="city")).docs
#print(res)

"""
Using AND
"""
res=rs_user.search(Query("Paul @city:{Tel*}")).docs
#print(res)

"""
Using OR
"""
res=rs_user.search(Query("Paul|@city:{Tel*}").return_field("$.name",as_field="name")).docs
#print(res)

"""
OR in the same field
"""
res=rs_user.search(Query("@city:{Tel*|Lon*}").return_field("$.name",as_field="name")).docs
# print(res)

"""
Using NOT 
"""
res=rs_user.search(Query("-Paul")).docs
#print(res)

"""
Using aggregation functions. Here Count aggregate function is used

FT.AGGREGATE index "query_expr" ...  GROUPBY n "field_1" .. "field_n" REDUCE AGG_FUNC m "@field_param_1" .. "@field_param_m" AS "aggregated_result_field"
"""
req = aggregations.AggregateRequest("*").load("name","city").group_by("@city", reducers.count().alias("count"))
print(rs_user.aggregate(req).rows)