import psycopg2
from config import *

def connect():
    con = psycopg2.connect(host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD)
    cur = con.cursor()
    return con, cur