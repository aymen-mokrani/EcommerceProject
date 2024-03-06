import psycopg2
from dotenv import load_dotenv
import os

def init_connection() :
    load_dotenv(".env")

    con = psycopg2.connect(
        user=os.environ["MYUSER"],
        host=os.environ["HOST"],
        dbname=os.environ["DATABASE"],
        password=os.environ["PASSWORD"],
        port=os.environ["PORT"]
    )

    return con

