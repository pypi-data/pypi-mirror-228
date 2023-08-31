# wrapper.py
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
import traceback
import requests
import sys


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


key_ignore_dp_config = "ignore_dp_config"


def set_ignore_dp_config(ignore: bool = False):
    sys.modules[key_ignore_dp_config] = ignore


def get_ignore_dp_config():
    return sys.modules.get(key_ignore_dp_config, False)


def get_dt_config(url) -> dict:
    if get_ignore_dp_config():
        return
    response = requests.get(url)
    response.raise_for_status()
    return json.loads(response.content.decode())


class DPConnector:
    def __init__(self, dp_connector_config):
        self.dp_config = None
        if get_ignore_dp_config():
            return
        self.dp_connector_config = dp_connector_config
        if self.dp_connector_config.get("path"):
            self.read_config_path()
        elif self.dp_connector_config.get("name"):
            self.call_api_config()

        if not self.dp_config:
            traceback.print_exc()
            print(f"Invalid connector: {self.dp_connector_config}")

    def read_config_path(self):
        try:
            with open(self.dp_connector_config["path"], "r") as conf_file:
                self.dp_config = json.load(conf_file)

        except:
            traceback.print_exc()
            print(f"We have a problem to reading path: {self.dp_connector_config}")

    def call_api_config(self) -> dict:
        try:
            host = self.dp_connector_config["datapeach_config"]["host"]
            port = self.dp_connector_config["datapeach_config"]["port"]
            connector_name = self.dp_connector_config["name"]
            url = f"http://{host}:{port}/api/v1/connections/connection_id/{connector_name}"
            data_response = get_dt_config(url)
            meta_connection = data_response["result_obj"]["meta_connection"]
            self.dp_config = {
                "hostname": meta_connection["hostname"],
                "port": meta_connection["port"],
                "tenant": meta_connection["tenant"],
                "namespace": meta_connection["namespace"],
            }
        except:
            traceback.print_exc()
            print(f"We have a problem to calling api: {self.dp_connector_config}")


class DPStreamReader:
    """
    * Perform the main logic of the function on the input dataset.
    * @param url - url get pipeline in the DataPeach.
    * @param udf - custom function.
    * @param para - parameter of the udf
    """

    def __init__(self, dp_connector: DPConnector, udf, dry_mode=False):
        self.connected = False
        if not dp_connector.dp_config:
            return
        self.udf = udf
        # refactor, instead of conf file, dict of conf
        self.dp_connector = dp_connector
        self.dry_mode = dry_mode
        self.queue = asyncio.Queue()
        self.connect_to_datasource()

    def connect_to_datasource(self):
        if self.dp_connector.dp_config is None:
            return
        """
        ESTABLISH CONNECTOR TO PULSAR - GENERIC
        """
        source = self.dp_connector.dp_config
        logging.info(f"Connect to pulsar {source}")

        broker = f'pulsar://{source["hostname"]}:{source["port"]}'

        self.client = pulsar.Client(broker)
        """
        CONSUME the right data, known the schema
        """
        subcription = "".join(random.choice(string.ascii_lowercase) for i in range(100))
        self.consumer = self.client.subscribe(
            self.dp_connector.dp_connector_config["topic"], subcription
        )
        self.connected = True

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
    async def call_back_process(self, result_queue, udf, parameter: dict):
        msg = self.consumer.receive()
        data = msg.data().decode("utf-8")
        input_data = json.loads(data)

        result = udf(input_data, **parameter)
        result_queue.put(result)

    def batch_process(self, parameter: dict):
        if not self.connected:
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
        loop.run_until_complete(
            self.call_back_process(current_queue, self.udf, parameter)
        )
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
