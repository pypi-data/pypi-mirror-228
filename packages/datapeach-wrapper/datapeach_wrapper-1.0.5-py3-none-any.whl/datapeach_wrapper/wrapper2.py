# wrapper.py
import os
import asyncio
import json
import sys
import logging
import pulsar
import random
import string
from functools import wraps
import queue
import nest_asyncio
import requests


class NotebookQueue:
    """Using a queue to keep data"""

    def __init__(self):
        self.current_queue = queue.Queue()

    def get(self):
        return self.current_queue.get()

    def put(self, data):
        return self.current_queue.put(data)

    def size(self):
        return self.current_queue.qsize()


host_name = "192.168.10.18"
port = "9000"
wrapper_config = "wrapper_config.json"


def get_dt_config(url) -> dict:
    try:
        current_directory = (
            os.path.abspath(os.path.join(os.path.dirname("")))
            + "/datapeach_cli_config.json"
        )
        if os.path.exists(current_directory):
            return
        response = requests.get(url)
        response.raise_for_status()
        return json.loads(response.content.decode())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return None


class StreamReader:
    """
    * Perform the main logic of the function on the input dataset.
    * @param url - url get pipeline in the DataPeach.
    * @param udf - custom function.
    * @param para - parameter of the udf
    """

    def __init__(self, datapeach_config: dict, udf, para, dry_mode=False):
        self.udf = udf
        # refactor, instead of conf file, dict of conf
        host = datapeach_config.get("host")
        port = datapeach_config.get("port")
        pipeline_id = datapeach_config.get("pipeline_id")
        url = f"http://{host}:{port}/api/v1/pipelines/etl_pipline/{pipeline_id}"
        self.dt_config = get_dt_config(url)
        print(self.dt_config)
        self.dry_mode = dry_mode
        self.para = para
        self.queue = asyncio.Queue()

    def connect_to_datasource(self):
        if self.dt_config is None:
            return
        """
        ESTABLISH CONNECTOR TO PULSAR - GENERIC
        """
        logging.info(f'Connect to pulsar {self.dt_config["source"]}')

        source = self.dt_config["source"]

        broker = f'pulsar://{source["hostname"]}:{source["port"]}'

        self.client = pulsar.Client(broker)
        """
        CONSUME the right data, known the schema
        """
        print(self.dt_config["source"]["topic"])
        subcription = "".join(random.choice(string.ascii_lowercase) for i in range(10))
        self.consumer = self.client.subscribe(
            self.dt_config["source"]["topic"], subcription
        )

    def _batch_pull_data(self, size=1, type="pandas", async_mode=False):
        # return an array of records or pandas
        if self.dry_mode == False:
            values = []
            for i in range(size):
                msg = self.consumer.receive()
                data = msg.data().decode("utf-8")
                value = json.loads(data)
                print("message value receive", value)
                values.append(value)
            return values
        return None

    # ufd: user define function
    async def _batch_process(self, result_queue, udf, n, type="pandas"):
        # current_queue = NotebookQueue()

        # input_data=self._batch_pull_data(n,type=type)

        msg = self.consumer.receive()
        # input_data=msg.value()
        data = msg.data().decode("utf-8")
        input_data = json.loads(data)

        # print("message value receive", input_data)
        # operators = self.dt_config["build_operation"]["ops"]
        # for op in operators:
        result = udf(input_data, **self.para)
        result_queue.put(result)
        # return current_queue

    def batch_process(self, n=1, type="pandas"):
        if self.dt_config is None:
            return
        nest_asyncio.apply()
        current_queue = NotebookQueue()
        """
        input_data=await self._batch_pull_data(n,type=type)              
        result=self.udf(input_data)
        current_queue.put(result)
        """
        # using asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._batch_process(current_queue, self.udf, n, type))
        # asyncio.run(self._batch_process(current_queue,self.udf,n,type))
        return current_queue


def source_config(dict_pulsar):
    hostname = dict_pulsar["hostname"]
    port = dict_pulsar["port"]
    topic = dict_pulsar["topic"]

    conection = f"pulsar://{hostname}:{port}"
    logging.info("Connecting Pulsar:" + conection)
    client = pulsar.Client(conection)
    """
    CONSUME the right data, known the schema
    """
    logging.info("Pulsar connected")
    subcription = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    consumer = client.subscribe(topic, subcription)

    sys.modules["datapeach.consumer"] = consumer


def sink_config(dict_cnn, sql):
    sys.modules["datapeach.sinkconfig"] = dict_cnn
    sys.modules["datapeach.sql"] = sql
    cfg = sys.modules["datapeach.sinkconfig"]


def dp_function(**kw):
    def decorator(original_func):
        @wraps(original_func)
        def wrapper(records: dict | list[dict], **kwargs):
            return original_func(records, **kwargs)

        """add attribute cto check decorator use dp_function"""
        wrapper.dp_function = True

        return wrapper

    return decorator


def dp_import(func):
    @wraps(func)
    def wrapper(*arg):
        return func(*arg)

    wrapper.dp_import = True
    return wrapper
