import psycopg2

try:
    connection = psycopg2.connect(
    host="isabelle.db.elephantsql.com",
    user="jngfozzr",
    password="9LtMBayHNIJJ-iXrVlI1Ow3C3EgXElLd",
    database="jngfozzr",
    connect_timeout=100  # Aumente o timeout para 10 segundos
)
    print("Conexão bem-sucedida!")
except psycopg2.OperationalError as e:
    print("Erro de conexão:", e)
finally:
    if 'connection' in locals():
        connection.close()