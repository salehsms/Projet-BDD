import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="recette",
        user="postgres",
        password="123456789",
        host="localhost",
        port="5432"
    )