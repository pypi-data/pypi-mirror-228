#!/user/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/3 23:18
# @Author  : Leslie Wong
# @FileName: mongoutils.py
# @Software: PyCharm

import logging
from pymongo import MongoClient


class MongoUtils:
    """
    class for masterpiecesShot deployer,
    to deploy the json data to a MongoDB Atlas collection, ready for website implementation
    """

    def __init__(self):
        self.db = ""

    def create_mongodb_instance(self, url: str, database: str) -> bool:
        try:
            client = MongoClient(url)
            self.db = client[database]
            if self.db:
                return True
            else:
                return False
        except Exception as e:
            logging.error("Method create_mongodb_instance error!")
            logging.exception(e)

    def insert_one_record_to_mongodb(self, collection: str, record: dict) -> bool:
        try:
            print(record)
            result = self.db[collection].insert_one(record)
            if result.inserted_id:
                print(
                    f"Record inserts successfully: {str(result.inserted_id)}")
                return True
            else:
                return False
        except Exception as e:
            logging.error("Method insert_one_record_to_mongodb error!")
            logging.exception(e)

    def insert_many_records_to_mongodb(self, collection: str, records: list) -> bool:
        try:
            print(len(records))
            result = self.db[collection].insert_many(records)
            if result.acknowledged:
                print(f"Records insert successfully {str(result)}")
                return True
            else:
                return False
        except Exception as e:
            logging.error("Method insert_many_records_to_mongodb error!")
            logging.exception(e)

    def update_one_record_of_mongodb(self, collection: str, record_filter: dict, update_info: dict) -> bool:
        try:
            print(record_filter)
            updateDict = {"$set": update_info}
            result = self.db[collection].update_one(record_filter, updateDict)
            if result:
                print(f"Record updates successfully: {str(result)}")
                return True
            else:
                return False
        except Exception as e:
            logging.error("Method update_one_record_of_mongodb error!")
            logging.error(e)

    def get_one_record_from_mongodb(self, collection: str, filter: dict = {},  exclude: list = []) -> list:
        try:
            result = [self.db[collection].find_one(filter)]
            for doc in result:
                for i in exclude:
                    del doc[i]
            return result
        except Exception as e:
            logging.error("Method get_one_record_from_mongodb error!")
            logging.error(e)

    def delete_one_record_from_mongodb(self, collection: str, filter: dict = {}) -> list:
        try:
            result = self.db[collection].delete_one(filter)
            if result:
                print(f"Record deletes successfully: {str(result)}")
                return True
            else:
                return False
        except Exception as e:
            logging.error("Method delete_one_record_from_mongodb error!")
            logging.error(e)

    def get_many_records_from_mongodb(self, collection: str, filter: dict = {},
                                      limit: str = "10000", exclude: list = []) -> list:
        try:
            # result = [doc for doc in self.db[collection].find(
            #     filter).limit(int(limit))]

            # Prevent the same results most likely when fetching subsequently. See issue #35
            result = [doc for doc in self.db[collection].aggregate(
                [
                    {"$match": filter},
                    {"$sample": {"size": int(limit)}},
                ]
            )]
            for doc in result:
                for i in exclude:
                    del doc[i]
            return result
        except Exception as e:
            logging.error("Method get_many_records_from_mongodb error!")
            logging.error(e)

    def get_collection_count_from_mongodb(self, collection: str, filter: dict = {}) -> int:
        try:
            count = self.db[collection].count_documents(filter)
            return count
        except Exception as e:
            logging.error("Method get_collection_size_from_mongodb error!")
            logging.error(e)

    def get_search_results_from_mongodb(self, collection: str, query: str, index: str, limit: str = "10000", project: dict = {}) -> list:
        try:
            result = self.db[collection].aggregate([
                {
                    "$search": {
                        "index": index,
                        "text": {
                            "query": query,
                            "path": {"wildcard": "*"}
                        }
                    }
                }, {
                    "$limit": int(limit)
                }, {
                    "$project": project
                }
            ])
            real_result = []
            for i in result:
                real_result.append(i)
            return real_result
        except Exception as e:
            logging.error("Method get_search_results_from_mongodb error!")
            logging.error(e)
