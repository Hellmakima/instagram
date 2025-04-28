from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
try:
    from core.config import settings  # when used inside project
except ImportError:
    from config import settings  # when running directly
try:
    from main import client  # when used inside project
except ImportError:
    client = MongoClient(settings.MONGODB_URI)  # when running directly

def get_db():
    try:
        # The ismaster command is cheap and fast to run.
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except ConnectionFailure:
        print("Server not available")
        raise  # Re-raise the ConnectionFailure exception

    db = client[settings.MONGODB_DB]
    # DO NOT close the client here.
    return db

def test_db_connection():
    """
    Tests the database connection by performing a simple insert and query.
    """
    try:
        db = get_db()  # Get the database connection
        collection = db.test_collection  # Access a collection (or create if it doesn't exist)

        # 1. Insert a test document
        test_document = {"name": "Test User", "value": 123}
        insert_result = collection.insert_one(test_document)
        print(f"Inserted document with ID: {insert_result.inserted_id}")

        # 2. Query for the test document
        query_result = collection.find_one({"name": "Test User"})
        print(f"Query result: {query_result}")

        assert query_result["name"] == "Test User"  # Basic assertion to check data integrity
        print("Successfully inserted and retrieved data!")

        # 3. Clean up (optional, but good practice for testing)
        collection.delete_one({"name": "Test User"})
        print("Deleted the test document.")

    except ConnectionFailure as e:
        print(f"Connection test failed: {e}")
        #  The get_db() function now raises this, so you can handle it here.
    except Exception as e:
        # Catch any other exceptions during the test.
        print(f"An error occurred during the test: {e}")
    finally:
        if 'client' in locals(): #check if client was defined
            client.close() # Close connection

if __name__ == '__main__':
    test_db_connection()