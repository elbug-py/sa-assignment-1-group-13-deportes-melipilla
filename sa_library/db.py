import mongoengine

def connect_db():
    mongoengine.connect(
        db="library_db",
        host="mongodb://mongo:27017/library_db"
    )