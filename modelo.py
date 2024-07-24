from conexionDB import DBConnection

class UserModel:
    def __init__(self):
        self.db_connection = DBConnection(host='localhost',port=3306, user='correos', password='l6hhtzZK]OPzkO1M', database='correosyury')
        self.db_connection.connect()
    #Login Listo
    def verify_user_credentials(self, username, password):
        query = "SELECT * FROM Usuarios WHERE correo = %s AND password = %s"
        result = self.db_connection.execute_query(query, (username, password))
        return result
    
    def get_user_profile(self, username):
        query = """
        SELECT t.correo_trabajador, t.contactos_emergencia, t.cargas_familiares
        FROM trabajadores t
        INNER JOIN usuarios u ON t.IdUsuario = u.id
        WHERE u.username = %s
        """
        result = self.db_connection.execute_query(query, (username,))
        return result[0] if result else None

    def edit_user_profile(self, username, nuevo_correo=None, nuevo_contacto=None, nueva_carga=None):
    # Construir la parte del SET de la consulta SQL dinámicamente según los valores proporcionados
        set_clause = []
        params = []

        if nuevo_contacto is not None:
            set_clause.append("contactos_emergencia = %s")
            params.append(nuevo_contacto)

        if nueva_carga is not None:
            set_clause.append("cargas_familiares = %s")
            params.append(nueva_carga)

        # Si no se proporciona nuevo_correo, no lo actualizamos
        if nuevo_correo is not None:
            set_clause.append("correo_trabajador = %s")
            params.append(nuevo_correo)

        # Asegurarse de que al menos uno de los campos se actualice
        if not set_clause:
            raise ValueError("No se proporcionaron valores para actualizar.")

        # Añadir la cláusula WHERE
        set_clause_str = ", ".join(set_clause)
        query = f"""
        UPDATE trabajadores 
        SET {set_clause_str} 
        WHERE IdUsuario = (SELECT id FROM usuarios WHERE username = %s)
        """
        params.append(username)

        affected_rows = self.db_connection.execute_update(query, tuple(params))
        return affected_rows > 0
    #listar listo
    def get_workers_list(self):
        query = "SELECT t.id, t.nombre, t.rut, f.estado, t.cargo, t.departamento FROM trabajadores t LEFT JOIN fichastrabajadores f ON t.id = f.id_trabajador"
        result = self.db_connection.execute_query(query)
        return result

    def filter_workers_by_department(self, department):
        query = "SELECT * FROM Trabajadores WHERE departamento = %s"
        result = self.db_connection.execute_query(query, (department,))
        return result

    def filter_workers_by_position(self, position):
        query = "SELECT * FROM Trabajadores WHERE cargo = %s"
        result = self.db_connection.execute_query(query, (position,))
        return result
    #Fichas pendientes Jefe rrhh
    def get_pending_forms(self):
        query = """SELECT 
                    fichastrabajadores.id AS id_ficha,
                    trabajadores.nombre AS nombre_trabajador,
                    fichastrabajadores.fecha_ingreso,
                    fichastrabajadores.estado
                FROM 
                    fichastrabajadores
                JOIN 
                    trabajadores ON fichastrabajadores.id_trabajador = trabajadores.id
                """
        result = self.db_connection.execute_query(query)
        return result
    
    #Ver fichas listo
    def get_user_forms(self):
        query = """ SELECT f.id, t.nombre, f.estado,f.fecha_ingreso,t.cargo, t.departamento FROM trabajadores t LEFT JOIN fichastrabajadores f ON t.id = f.id_trabajador""" 
        result = self.db_connection.execute_query(query)
        return result

    #actualizar estado fichas JEFE RRHH
    def update_form_status(self, form_id, new_status):
        query = "UPDATE Fichas SET estado = %s WHERE id = %s"
        params = (new_status, form_id)
        affected_rows = self.db_connection.execute_update(query, params)
        return affected_rows > 0
    #Agregar ficha trabajador
    def add_worker_form(self, nombre, rut, correo, cargo, departamento, cargas_familiares, contactos_emergencia, prevision, afp):
        # Verificar que contactos_emergencia y cargas_familiares son listas
        if not isinstance(contactos_emergencia, list):
            contactos_emergencia = []  # Definir como lista vacía si no es una lista
        if not isinstance(cargas_familiares, list):
            cargas_familiares = []  # Definir como lista vacía si no es una lista
        # Insertar en la tabla 'trabajadores'
        query_trabajadores = """
        INSERT INTO trabajadores (nombre, rut, correo_trabajador, cargo, departamento, prevision, afp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params_trabajadores = (nombre, rut, correo, cargo, departamento, prevision, afp)
        trabajador_id = self.db_connection.execute_update(query_trabajadores, params_trabajadores, return_last_insert_id=True)

        # Insertar en la tabla 'contactoemergencias'
        for contacto in contactos_emergencia:
            nombre_contacto = contacto['nombre']
            telefono = contacto['telefono']
            query_contactos = "INSERT INTO contactoemergencias (nombre, telefono) VALUES (%s, %s)"
            params_contactos = (nombre_contacto, telefono)
            contacto_id = self.db_connection.execute_update(query_contactos, params_contactos, return_last_insert_id=True)

        # Insertar en la tabla 'fichastrabajadores'
        query_ficha = "INSERT INTO fichastrabajadores (id_trabajador, estado) VALUES (%s, 'pendiente')"
        self.db_connection.execute_update(query_ficha, (trabajador_id,))

        # Insertar en la tabla 'parentesco'
        for carga in cargas_familiares:
            nombreFamiliar = carga['nombreFamiliar']
            parentesco = carga['parentesco']
            sexo = carga['sexo']
            query_parentesco = "INSERT INTO parentesco (nombreFamiliar, parentesco, sexo) VALUES (%s, %s, %s)"
            params_parentesco = (nombreFamiliar, parentesco, sexo)
            self.db_connection.execute_update(query_parentesco, params_parentesco)
