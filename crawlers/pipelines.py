# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


import pymongo


class JusBRMongoPipeline(object):

    collection_name = "default_collection"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        keys = {
            "numero": item.get("numero") if item.get("numero") else spider.numero,
            "instancia": item.get("instancia"),
            "classe": item.get("classe"),
            "data_distribuicao": item.get("data_distribuicao"),
        }
        self.db[self.collection_name].update_one(
            keys,
            {"$set": dict(item)},
            upsert=True,
        )
        spider.items.append(item)

        return item
