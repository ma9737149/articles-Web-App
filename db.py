from mysql.connector.pooling import MySQLConnectionPool
from dotenv import load_dotenv
import os 


load_dotenv()


class DB:
    _pool = None

    @classmethod
    def init_pool(cls):
        cls._pool = MySQLConnectionPool(
            pool_size=20,
            pool_name='articles_web_app',
            connection_timeout=20,
            host=os.getenv('HOST'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            database='articles_web_app',
        )

        return cls._pool


    @classmethod
    def get_connection(cls):
        if cls._pool is None:
            cls.init_pool()
        try:

            return cls._pool.get_connection()
            
        except Exception as e:
            raise e

db = DB()