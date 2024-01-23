FROM gcr.io/datamechanics/spark:platform-3.3.0-hadoop-3.3.2-java-8-scala-2.12-python-3.8-dm18-dev
ENV PYSPARK_MAJOR_PYTHON_VERSION=3
ENV PYSPARK_SUBMIT_ARGS="--master local[3] pyspark-shell"
WORKDIR /data_processing
COPY ./requirements.txt /data_processing/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /data_processing/requirements.txt
COPY . /data_processing
