from redis import Redis
from redis.commands.search.query import Query


def read_latest(n:int):
    r1 = Redis()
    res=r1.ft("idx:shoes_index")\
          .search(Query("*")\
          .sort_by("dateUpdatedInt",asc=False)\
          .return_fields("$.name","AS","name","$.colors","AS","colors","$.dateUpdated","AS","dateUpdated").paging(0,n))\
          .docs
    return res


def read_latest_by_color(color:str,n:int):
    r1 = Redis()
    res=r1.ft("idx:shoes_index").search(Query("@colors:*{color}*".format(color=color))\
          .sort_by("dateUpdatedInt",asc=False)\
          .return_fields("$.name","AS","name","$.colors","AS","colors","$.dateUpdated","AS","dateUpdated")\
          .paging(0,n))\
          .docs
    return res