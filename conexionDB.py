import mysql.connector

class DBConnection:
    def __init__(self, host='localhost', port=3306, user='correos', password='l6hhtzZK]OPzkO1M', database='correosyury'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Conexión a la base de datos MySQL establecida correctamente.")
        except mysql.connector.Error as e:
            print(f"Error al conectar a MySQL: {e}")

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión a la base de datos MySQL cerrada correctamente.")


    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
            print("Consulta ejecutada correctamente.")
            return result
        except mysql.connector.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
        
    def execute_update(self, query, params=None, return_last_insert_id=False):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            if return_last_insert_id:
                return cursor.lastrowid
            self.connection.commit()
