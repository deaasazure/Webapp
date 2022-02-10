FROM bitnami/spark:latest
COPY requirements.txt .
USER 0
RUN pip install -r requirements.txt
COPY main /main
WORKDIR /main
EXPOSE 8000
#ENV PATH "PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9-src.zip:$PYTHONPATH"