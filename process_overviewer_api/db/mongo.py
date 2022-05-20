import configparser
import logging
from multiprocessing import connection
from os import path
from typing import Dict, List, Any

from pymongo import MongoClient
from jsonschema import validate, ValidationError

from process_schema import process_schema


class Mongo:

    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def add_process(self, process: Dict[str, Any]) -> str:
        try:
            validate(process_schema, process)
            with MongoClient(connection_string) as client:
                db = client["process_overviewer"]
                collection = db.processes

                if collection.count_documents({"name": process["name"]},
                                              limit=1) > 0:
                    logging.warn(
                        f"Tried to store document with name {process['name']}, but already exists and was rejected."
                    )
                    return "REJECT:ALREADY_TAKEN"

                collection.insert_one(process)
            return "OK"
        except ValidationError as ve:
            logging.error(
                f"Process could not be veryfied against the process schema.")
            logging.debug(f"The original error message: \n {ve}")
            return "ERROR"
        except Exception as e:
            logging.error(
                f"Something went wrong with writing the process to the database."
            )
            logging.debug(f"The original error message: \n {e}")
            return "ERROR"

    @staticmethod
    def get_connection_string(config_path: str = "variables.ini"):
        config = configparser.ConfigParser()
        config.read(path.abspath(config_path))

        host_url = config.get("mongo", "host_url")
        port = config.get("mongo", "port")

        connection_string = (f"mongodb://{host_url}:{port}")

        return connection_string


if __name__ == "__main__":
    connection_string = Mongo.get_connection_string()
    mongo = Mongo(connection_string)

    test_process_1 = {
        "name": "spieleabend",
        "participants": ["it center"],
        "purpose": "socializing",
        "turnus": "monthly"
    }

    mongo.add_process(test_process_1)
