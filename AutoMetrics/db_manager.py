import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self, host, database, user, password):
        # ⭐️ Configuración de la conexión ⭐️
        self.connection = None
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connect()

    def connect(self):
        """Intenta establecer la conexión con la base de datos."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Conexión a MySQL exitosa.")
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")

    def execute_query(self, query, params=None):
        """Función genérica para ejecutar una consulta (INSERT, UPDATE, DELETE)."""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    # --- MÉTODOS CRUD (CREAR) ---
    def add_empleado(self, data):
        """Agrega un nuevo empleado a la tabla Empleados."""
        query = ("INSERT INTO Empleados "
                 "(nombre, email, telefono, id_empleado, cargo, anio_ingreso, genero) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        
        # 'data' debe ser una tupla con los valores en el orden de la query
        return self.execute_query(query, data)

    # --- MÉTODOS CRUD (LEER - Obtener un registro) ---
    def get_empleado_by_id(self, id_sistema):
        """Obtiene la información de un empleado por su ID de sistema."""
        query = "SELECT * FROM Empleados WHERE id_empleado_sistema = %s"
        cursor = self.connection.cursor(dictionary=True) # Retorna como diccionario
        cursor.execute(query, (id_sistema,))
        record = cursor.fetchone()
        cursor.close()
        return record

    # Aquí irían los métodos update_empleado y delete_empleado...
    # En db_manager.py (dentro de la clase DatabaseManager)

    def add_vehiculo(self, data):
        """Agrega un nuevo vehículo a la tabla 'vehiculos'."""
        # Las columnas en la consulta deben coincidir EXACTAMENTE con las de tu tabla
        # y con el orden de la tupla 'data'
        query = """
        INSERT INTO vehiculos (
            vin_serial_no, marca, modelo, anio, engine_type, 
            transmision, kilometraje, estado, ultimo_mantenimiento
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # 'data' debe ser una tupla con 9 valores
        return self.execute_query(query, data)
    
    def get_reporte_mantenimiento(self):
        """Cuenta vehículos por estado (reparado, mantenido, reciclaje)."""
        # Si la columna se llama 'estado' en la DB
        query = """
        SELECT 
            estado, 
            COUNT(*) 
        FROM Vehiculos 
        GROUP BY estado
        """
        # Esto devolverá algo como: [('reparado', 5), ('mantenido', 10), ('reciclaje', 2)]
        return self.execute_read_query(query)
    
    def update_estado_vehiculo(self, vin_serial_no, nuevo_estado):
        query = "UPDATE Vehiculos SET estado = %s WHERE vin_serial_no = %s"
        data = (nuevo_estado, vin_serial_no)
        
        # Retorna True si la consulta se ejecuta con éxito
        return self.execute_query(query, data)
    

    # Debes añadir esta función
    def get_connection(self):
        """Retorna un nuevo objeto de conexión a MySQL."""
        try:
            # Usa la biblioteca mysql.connector
            import mysql.connector
            
            # ⭐ Asegúrate de que las credenciales (host, user, password, database) 
            #    estén definidas como atributos de la clase (self.host, etc.) o pasadas.
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Exception as e:
            print(f"Error al obtener la conexión: {e}")
            return None
        

    def obtener_estado_vehiculo(self, vin): 
        """Obtiene el estado actual de un vehículo por su VIN."""
        # La columna de la llave primaria en la tabla es 'vin_serial_no'
        query = "SELECT estado FROM Vehiculos WHERE vin_serial_no = %s" # <-- ¡Debe tener solo un %s!
        
        
        # Ejemplo asumiendo que execute_read_query acepta data como segundo argumento:
        resultados = self.execute_read_query(query, (vin,)) 
        
        if resultados:
            return resultados[0][0] # Retorna el estado (el primer valor de la primera tupla)
        return "No encontrado" # Si no hay resultados
    

    # EN db_manager.py (Modificar la función de actualización de estado)

    def actualizar_estado_vehiculo(self, vin, nuevo_estado, tiempo_reparacion_horas):
        # 1. ACTUALIZAR la tabla Vehiculos
        query_update = "UPDATE Vehiculos SET estado = %s WHERE vin_serial_no = %s"
        data_update = (nuevo_estado, vin)
        
        # 2. INSERTAR el registro en Registros_Ingenieria (la tabla de historial)
        query_insert = """
        INSERT INTO Registros_Ingenieria 
        (vin_serial_no, estado_nuevo, tiempo_reparacion_horas) 
        VALUES (%s, %s, %s)
        """
        data_insert = (vin, nuevo_estado, tiempo_reparacion_horas)
        
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Ejecutar ambas consultas
            cursor.execute(query_update, data_update)
            cursor.execute(query_insert, data_insert)
            
            connection.commit() # ¡CONFIRMAR AMBAS OPERACIONES!
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            # En caso de error, deshacer todo y reportar
            if 'connection' in locals():
                connection.rollback()
            print(f"Error al actualizar y registrar estado del vehículo: {e}")
            return False
        
        
    
    def execute_read_query(self, query, data=None): # <<-- CORRECCIÓN AQUÍ
        """Ejecuta una consulta SELECT y retorna los resultados como una lista de tuplas."""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # 2. Ejecutar la consulta
            if data:
                cursor.execute(query, data) # Ahora acepta la tupla (vin,)
            else:
                cursor.execute(query) # Consulta simple
                
            resultados = cursor.fetchall()
            cursor.close()
            connection.close()
            return resultados
        except Exception as e:
            # Aquí puedes dejar tu lógica de manejo de errores
            print(f"Error al leer la base de datos: {e}") 
            return []
        
    def get_distribucion_empleados(self):
    # La columna del rol se llama 'cargo' en tu esquema
        query = "SELECT cargo, COUNT(*) FROM Empleados GROUP BY cargo"
        
        # Llama a la función de lectura de datos
        return self.execute_read_query(query)
    
    def obtener_lista_vehiculos(self):
        """Obtiene el VIN, marca y modelo de TODOS los vehículos."""
        query = "SELECT vin_serial_no, marca, modelo FROM Vehiculos"
        # Reutiliza tu función de lectura que ya debería aceptar solo el query si no hay 'data'
        resultados = self.execute_read_query(query) 
        return resultados
    

    def obtener_datos_reparacion(self, vin):

        query = """
        SELECT 
            estado_nuevo, 
            SUM(tiempo_reparacion_horas) 
        FROM Registros_Ingenieria
        WHERE vin_serial_no = %s
        GROUP BY estado_nuevo
        ORDER BY SUM(tiempo_reparacion_horas) DESC
    """
        return self.execute_read_query(query, (vin,))
    

    def guardar_feedback_marketing(self, vin, nombre_anuncio, gusto):
        """Guarda si al usuario le gustó o no el anuncio en la tabla feedback."""
        # Insertar sin fecha_registro; MySQL asignará NOW() automáticamente si tiene DEFAULT
        query = """
        INSERT INTO feedback (vin_serial_no, nombre_anuncio, gusta)
        VALUES (%s, %s, %s)
        """
        data = (vin, nombre_anuncio, gusto)
        return self.execute_query(query, data)

    
    
