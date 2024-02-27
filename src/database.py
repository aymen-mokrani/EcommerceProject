import psycopg2
from dotenv import dotenv_values


config = dotenv_values(".env")

con = psycopg2.connect(
    user=config["USER"],
    host=config["HOST"],
    dbname=config["DATABASE"],
    password=config["PASSWORD"],
    port=config["PORT"]
)
