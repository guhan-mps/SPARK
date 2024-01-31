# Spark application to cache data in Redis and ElasticSearch

This project is a Spark application that caches its read data into a redis cache and elasticsearch, this cache is used by a FastAPI API that fetches the data in redis through redis search queries and elasticsearch through its search queries.

## Description

This project aims at making data fetching faster by using Spark over Redis and ElasticSearch, both of which are distributed data processing layers which facilitate faster huge data retrival by a backendapi. The project consists of three directories. The purpose of them are:

* **backendapi:** This directory consists of a backend API written with FastAPI, that queries data cached in Redis and ElasticSearch. This API retrives the latest n shoes and can retrive the latest n shoes of the required color in the Redis and ElasticSearch's cached data.

* **data_processing:** This directory consists of the spark job. This spark job reads the data available as CSV's in the dataset directory parallely using mulithreading, converts the read dataframe to a list of RDDs and then writes the RDDs as json data to the redis cache and ElasticSearch cache. This also creates indices for the written data so as to facilitate search queries of redis and elasticsearch by the backendapi's search query.
* **deployment:** This directory consists of YAML files for deploying the redis, spark job and the API into the kubernetes as a service. This packaging makes the project available regardless of the platform being run. 

## Getting Started

### Dependencies

* Any OS is supported for this project

* redis==5.0.0
* fastapi==0.108.0
* pydantic>=2.5.3
* uvicorn==0.25.0
* greenlet==3.0.3
* pyspark==3.5.0
* elasticsearch==8.12.0
* python-dotenv==1.0.0
### Installing

* Get the source code using git clone https://github.com/guhan-mps/SPARK

* If you are running the code locally, install redis stack server following the guide <https://redis.io/docs/install/install-stack/linux/>
* If you are running locally install spark using the guide <https://phoenixnap.com/kb/install-spark-on-ubuntu>
* If you are running the code locally, change the host part of redis connection in config sub-directory in both backendapi and data_processing directories to localhost
* If you are runninf the code locally extract the zip files in **data_processing/dataset** directory
* If you are running on kubernetes, provide edit permissions to default:default service account by executing 
```
$ kubectl create clusterrolebinding default \
  --clusterrole=edit --serviceaccount=default:default --namespace=default
```
* If you are running locally set the environment variables ELASTIC_USER, ELASTIC_PASSWORD and CLOUD_ID to ElasticSearch username, ElasticSearch password and ElasticSearch deployment's cloud_id respectively.

### Executing program
* For **Executing locally**
    - Start the redis-stack-server service using
    ```
    $ service redis-stack-server start
    ```
    - Move to data_processing directory and run
    ```
    $ python data_load.py
    ```
    - Move to Spark directory and run
    ```
    $ uvicorn backendapi.app:app --reload --port 8000
    ```
    Now the API runs on port 8000 and can be accessed using SwaggerUI which runs on <http://127.0.0.1:8000/docs>

* For  **Execution using kubernetes**
    - Move to the deployment directory and run 
    ```
    $ minikube start
    $ helm install incubator/sparkoperator --namespace spark-operator --set sparkJobNamespace=test-ns
    $ kubectl apply -f volume.yaml
    $ kubectl apply -f elastic-secret.yaml
    $ kubectl apply -f redis-deployment.yaml
    $ kubectl apply -f redis-service.yaml
    $ kubectl apply -f spark-application.yaml
    $ kubectl apply -f fastapi-deployment.yaml
    $ kubectl apply -f fastapi-service.yaml
    ```
    Now the API runs on port 30009 and can be accessed using SwaggerUI running on 
    ```
    http://$(minikube ip):30009/docs
    ```
## Note
* You can increase or decrease the resources allocated to driver and executor according to your system capability in the spark-application.yaml. But makesure that you have not exceeded your system's resource capacity else the spark job cannot allocate resources to executors which inturn results in failure of sparkjob.

* Do not read after a write immediately in redis, as the newly created index takes time to apply the indices. If read immediately the output would be unstable.

* Redis search query basics <https://redis.io/docs/interact/search-and-query/>

* Providing multiple CSV's as list as Spark's read.csv() method fails to merge the matching columns if any of the CSV's schema is different from other. So multithreading is the solution to read data parallely using spark for datasets of differing schema