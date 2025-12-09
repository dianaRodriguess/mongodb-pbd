import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()


class Database:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def connect(self):
        if self._client is None:
            try:
                host = os.getenv("MONGO_HOST", "localhost")
                port = int(os.getenv("MONGO_PORT", 27017))
                user = os.getenv("MONGO_USER", "admin")
                password = os.getenv("MONGO_PASSWORD", "senha123")
                db_name = os.getenv("MONGO_DB", "gestaoAtt")

                connection_string = f"mongodb://{user}:{password}@{host}:{port}/"

                self._client = MongoClient(
                    connection_string, serverSelectionTimeoutMS=5000
                )

                self._client.admin.command("ping")

                self._db = self._client[db_name]

                print(f"Conectado-se ao banco: {db_name}")

            except ConnectionFailure as e:
                print(f"Erro ao conectar ao banco: {e}")
                raise
            except Exception as e:
                print(f"Erro inesperado: {e}")
                raise

        return self._db

    def get_database(self):
        if self._db is None:
            return self.connect()
        return self._db

    def close(self):
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            print("Conexão com banco fechada")


db_instance = Database()


def get_db():
    return db_instance.get_database()
