# db/mock_mongo.py

class MockCollection:
    def __init__(self):
        self._data = {}
    
    def insert_one(self, document):
        _id = document.get("_id")
        if not _id:
            _id = str(len(self._data) + 1)
            document["_id"] = _id
        self._data[_id] = document
        return type("InsertOneResult", (), {"inserted_id": _id})()
    
    def find_one(self, filter):
        for doc in self._data.values():
            if all(doc.get(k) == v for k, v in filter.items()):
                return doc
        return None
    
    def find(self, filter=None):
        filter = filter or {}
        return [doc for doc in self._data.values() if all(doc.get(k) == v for k, v in filter.items())]
    
    def update_one(self, filter, update):
        doc = self.find_one(filter)
        if not doc:
            return type("UpdateResult", (), {"modified_count": 0})()
        for k, v in update.get("$set", {}).items():
            doc[k] = v
        return type("UpdateResult", (), {"modified_count": 1})()
    
    def delete_one(self, filter):
        doc = self.find_one(filter)
        if not doc:
            return type("DeleteResult", (), {"deleted_count": 0})()
        del self._data[doc["_id"]]
        return type("DeleteResult", (), {"deleted_count": 1})()

class MockMongoDB:
    def __init__(self):
        self.dishes = MockCollection()
        self.ingredients = MockCollection()
        self.kitchen_tasks = MockCollection()
        self.cooks = MockCollection()

db = MockMongoDB()
