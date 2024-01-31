from ..config.elasticConnection import elastic_connect

def read_latest(n:int)->list[str]:
    """
    Returns the latest n shoes 
    """
    r1 = elastic_connect()
    res=r1.search(index="shoes",from_=0,size=n,sort=[{"dateUpdatedInt":"desc"}],fields=["name","colors","dateUpdated"])
    list_res=[]
    for i in res["hits"]["hits"]:
        list_res.append({i:str(j[0]) for i,j in i["fields"].items() })
    return list_res

def read_latest_by_color(color:str,n:int)->list[str]:
    """
    Returns the latest n shoes of the provided color
    """
    r1 = elastic_connect()
    res=r1.search(index="shoes",from_=0,size=n,sort=[{"dateUpdatedInt":"desc"}],fields=["name","colors","dateUpdated"],query={"query_string":{"query":"colors:*{color}*".format(color=color)}})
    list_res=[]
    for i in res["hits"]["hits"]:
        list_res.append({i:str(j[0]) for i,j in i["fields"].items() })
    return list_res