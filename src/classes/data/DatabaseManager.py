from pymongo.errors import DuplicateKeyError, PyMongoError
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from cryptography.fernet import Fernet
from datetime import datetime, date
from dotenv import load_dotenv
import os

load_dotenv()


class DatabaseManager:
    def __init__(self):
        self.uri = f"mongodb+srv://{os.getenv('MONGODB_USERNAME')}:{os.getenv('MONGODB_PASSWORD')}@cluster.gjrxpav.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
        self.encryption_key = os.getenv("ENCRYPTION_KEY")
        self.fernet = Fernet(self.encryption_key)
        self.client = self.get_database_client()

    def get_database_client(self):
        try:
            client = MongoClient(self.uri, server_api=ServerApi('1'))
            return client
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            return None

    def insert_data(self, collection_name, data):
        try:
            if self.client:
                db = self.client.get_database('iis')
                collection = db.get_collection(collection_name)
                collection.insert_one(data)
                print("Data inserted successfully!")
        except DuplicateKeyError:
            print("Data with the same _id already exists!")
        except Exception as e:
            print(f"An error occurred: {e}")

    def insert_token(self, collection_name, token_type, token):
        try:
            if self.client:
                db = self.client.get_database('iis')
                collection = db.get_collection(collection_name)

                encrypted_token = self.fernet.encrypt(token.encode())

                data = {
                    'type': token_type,
                    'token': encrypted_token,
                    'added': datetime.now(),
                }

                collection.insert_one(data)
                print("Data inserted successfully!")
        except DuplicateKeyError:
            print("Data with the same _id already exists!")
        except Exception as e:
            print(f"An error occurred: {e}")

    def fetch_latest_tokens(self):
        try:
            if self.client:
                db = self.client.get_database('iis')
                collection = db.get_collection('tokens')

                # Fetch the most recent access token
                latest_access_token = collection.find_one(
                    {'type': 'access'},
                    sort=[('added', -1)]
                )

                # Fetch the most recent refresh token
                latest_refresh_token = collection.find_one(
                    {'type': 'refresh'},
                    sort=[('added', -1)]
                )

                # Convert Binary token to bytes and decrypt
                if latest_access_token:
                    access_token_bytes = latest_access_token['token']
                    latest_access_token['token'] = self.fernet.decrypt(access_token_bytes).decode()

                if latest_refresh_token:
                    refresh_token_bytes = latest_refresh_token['token']
                    latest_refresh_token['token'] = self.fernet.decrypt(refresh_token_bytes).decode()

                return latest_access_token['token'], latest_refresh_token['token']
        except PyMongoError as e:
            print(f"An error occurred while fetching tokens: {e}")
            return None, None

    def fetch_data(self, collection_name, query=None, projection=None, sort_field=None, sort_order=1):
        if query is None:
            query = {}

        try:
            if self.client:
                db = self.client.get_database('iis')
                collection = db.get_collection(collection_name)

                if projection:
                    documents = collection.find(query, projection)
                else:
                    documents = collection.find(query)

                if sort_field:
                    documents = documents.sort(sort_field, sort_order)

                # Convert ObjectId to string for JSON serialization
                result = []
                for doc in documents:
                    doc['_id'] = str(doc['_id'])
                    result.append(doc)

                return result
        except PyMongoError as e:
            print(f"An error occurred while fetching data: {e}")
            return None

    def fetch_predictions_from_today(self):
        try:
            if self.client:
                db = self.client.get_database('iis')
                collection = db.get_collection('predictions')

                # Define start and end of today
                start_of_day = datetime.combine(date.today(), datetime.min.time())
                end_of_day = datetime.combine(date.today(), datetime.max.time())

                # Query for predictions from today for the specified station
                predictions_today = collection.find({
                    'datetime': {'$gte': start_of_day, '$lte': end_of_day}
                })

                return list(predictions_today)
        except Exception as e:
            print(f"An error occurred: {e}")
