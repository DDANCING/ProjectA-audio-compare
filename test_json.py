import psycopg2

try:
    connection = psycopg2.connect(
        host="autorack.proxy.rlwy.net",
        user="postgres",
        password="ajZvevKqNTZcYVFFBKzPBXTNWshKsYny",
        dbname="railway",
        port=17720, 
        sslmode='require' 
    )
    print("Conexão bem-sucedida!")
except psycopg2.OperationalError as e:
    print("Erro de conexão:", e)
finally:
    if 'connection' in locals():
        connection.close()