import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ... otras importaciones ...
from PySide6.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox,QVBoxLayout
)

# 1. Importa la clase del diseño generado por Qt Designer para el Diálogo de Inicio
from pyside6.AutoInterfaz.ui_Main import Ui_Dialog 
from PySide6.QtCore import Qt 
from pyside6.AutoInterfaz.ui_dashboard import Ui_MainWindow
from PySide6.QtWidgets import QButtonGroup
from db_manager import DatabaseManager
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure




2. #DEFINICIÓN DE LA FUNCIÓN CARGAR_ESTILOS_QSS (Debe ir aquí)
def cargar_estilos_qss(app, ruta_qss):
    """Carga el archivo QSS y lo aplica a la QApplication."""
    try:
        with open(ruta_qss, "r",encoding='utf-8') as file:
            app.setStyleSheet(file.read())
            print("Estilos QSS cargados correctamente.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de estilos en la ruta: {ruta_qss}")

class MainDashboard(QMainWindow, Ui_MainWindow):
    # Por ahora, solo tendrá un mensaje de bienvenida
    def __init__(self, rol_seleccionado):
        super().__init__()
      
        self.setupUi(self)
        self.rol = rol_seleccionado
        self.setWindowTitle(f"AutoMetrics - Dashboard de {self.rol}")
        self.statusBar().showMessage(f"Acceso con rol: {self.rol}")
                
                # ⭐️ LÓGICA CLAVE: Configurar la vista interna según el rol
        # ⭐️ 2. ASIGNAR LA VARIABLE 'rol_seleccionado' AL OBJETO (¡ESTO ES VITAL!)
        self.rol_seleccionado = rol_seleccionado
        self.configurar_dashboard_por_rol(self.rol_seleccionado)
        #

        # ... (setup y otras inicializaciones)
        # <-- LLAMA LA FUNCIÓN PARA OBTENER EL OBJETO DE CONEXIÓN# Guarda la conexión para usarla en los métodos CRUD
        self.rol = rol_seleccionado
        self.Ingebuton_4.clicked.connect(self.mostrar_grafica_reparacion)
        # EN Conexion.py (Dentro de __init__ o en un setup_connections())
        self.Ingeline.editingFinished.connect(self.cargar_datos_vehiculo)
        self.db = DatabaseManager(host='127.0.0.1', user='root',
                                password='Yull123', # O la clave que definiste para el nuevo usuario
                                database='autometrics')
        # ...
 
        # En Conexion.py, dentro de tu clase MainDashboard
        self.setup_navigation() # ⭐️ LLAMA A LA NUEVA FUNCIÓN AQUÍ ⭐️

        # Conectar el botón de la vista de Empleados a la función de manejo
        self.btnConfirmarCRUD.clicked.connect(self.manejar_confirmar_empleado,self.manejar_confirmar_vehiculo)
       
        self.inicializar_vista_visual()

    def handle_navigation(self, button,indice_de_pagina):
        # ... (Otros botones)

        try:
            self.btnConfirmarCRUD.clicked.disconnect()
        except TypeError:
            # Esto ocurre si no había ninguna conexión previa, es seguro ignorarlo.
            pass

        # 3. Conectar la acción específica según el índice
        if indice_de_pagina == 0:  # Administrador
            self.btnConfirmarCRUD.clicked.connect(self.manejar_confirmar_empleado)
            self.btnConfirmarCRUD.setVisible(True) # Si la vista lo usa
        
        elif indice_de_pagina == 3: # Ingeniería (Asumo que ahora es 3)
            # Conecta la función de editar vehículo o la principal de Ingeniería
            self.btnConfirmarCRUD.clicked.connect(self.manejar_editar_estado_vehiculo)
            self.btnConfirmarCRUD.setVisible(True)
        
        elif indice_de_pagina == 5: # Usuarios (No debería tener la misma visual de Ingeniería)
            # Aquí no haces nada, o conectas la función de CRUD de Usuarios
            self.btnConfirmarCRUD.setVisible(False) # Ocultarlo si no lo usas en esta vista
            
        else:
            # Para todas las demás vistas (Visual, Marketing, etc.)
            self.btnConfirmarCRUD.setVisible(False)
        
        if button.objectName() == "btnVehicles":

            self.stackedWidget.setCurrentIndex(3)
                # ⭐️ LLAMAR A LA FUNCIÓN DINÁMICA DE GRÁFICOS
            self.load_visual_analytics(self.rol_seleccionado) # Usamos el rol guardado

    def load_visual_analytics(self, rol):
        # 1. Limpiar el contenido anterior (CRUCIAL)
        # Debes encontrar el QWidget específico de la vista 'Visual'
        # Si la página Visual es self.stackedWidget.widget(3), entonces:
        visual_page = self.stackedWidget.widget(3)
        
        # Busca el Layout (el QVBoxLayout que creaste en Designer)
        layout = visual_page.layout()
        if layout is not None:
            # Elimina widgets existentes para reemplazarlos con el nuevo gráfico
            while layout.count():
                item = layout.takeAt(0)
                if item.widget() is not None:
                    item.widget().deleteLater()
                
        # Si no tiene layout, lo creamos (para el ejemplo, lo crearemos si no existe)
        if layout is None:
            layout = QVBoxLayout(visual_page)
            
        # 2. Generar y Añadir el Gráfico según el Rol
        if rol == "Administrador":
            title = "Administrador: Distribución de Empleados por Género"
            chart_canvas = self.create_simple_chart(title, [10, 20], ['Hombres', 'Mujeres'])
            layout.addWidget(chart_canvas)
            
        elif rol == "Logistica":
            title = "Logística: Estado Actual de la Flota (Activo vs. Mantenimiento)"
            chart_canvas = self.create_simple_chart(title, [80, 20], ['Activos', 'Mantenimiento'])
            layout.addWidget(chart_canvas)
            
        # En load_visual_analytics(self, rol)
        frame_contenedor = self.frameGraficos 
        layout = frame_contenedor.layout() 
        # ...
        layout.addWidget(chart_canvas) # El QVBoxLayout inserta el gráfico aquí


    def create_simple_chart(self, title, data, labels):
        """Función auxiliar que crea un gráfico de Matplotlib y lo devuelve como un QWidget."""
        
        # 1. Crear la Figura de Matplotlib
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # 2. Generar un Gráfico de Barras Simple
        ax.bar(labels, data, color=['#9c27b0', '#5e35b1']) # Colores Morados/Azules oscuros
        ax.set_title(title, color='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        fig.patch.set_facecolor('#1e1e1e') # Fondo oscuro de la figura
        ax.set_facecolor('#1e1e1e') # Fondo oscuro del área de plot
        
        # 3. Convertir la figura en un widget PySide6
        canvas = FigureCanvas(fig)
        return canvas
    
    # En Conexion.py (dentro de la clase MainDashboard)

    def inicializar_vista_visual(self):
        """Crea los gráficos y los añade a la página de Visual."""
        
            # 1. Obtener el widget de la página Visual
        visual_page_widget = self.stackedWidget.widget(2) # <-- Revisa si 3 es el índice correcto

        # 2. Verificar y Crear el Layout si es necesario
        if visual_page_widget.layout() is None:
            # Si no hay Layout, creamos un QVBoxLayout para organizar el gráfico
            layout = QVBoxLayout(visual_page_widget)
            visual_page_widget.setLayout(layout) # Establecer el layout
        
        # Ahora, podemos acceder al layout de forma segura
        layout = visual_page_widget.layout()

        if visual_page_widget is None:
            print("Error: El índice 2 del QStackedWidget está vacío. Asegúrate de tener un QWidget en esa posición.")
            return # Salir para evitar el error
        
        # 3. Limpiar la página antes de agregar (útil si se llama más de una vez)
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        resultados = self.db.get_distribucion_empleados()
                
        # 4. Crear el gráfico y agregarlo
        # 2. Procesar los resultados para el gráfico
        labels = [row[0] for row in resultados] # Nombres de los cargos (Admin, Logistica, etc.)
        datos = [row[1] for row in resultados]  # Conteo de empleados (1, 2, etc.)
        
        # Si la tabla está vacía, 'resultados' estará vacío. Usamos datos por defecto para evitar errores.
        if not datos:
            labels = ["Sin Datos"]
            datos = [0]
        
        # ... (El resto del código de la vista visual, incluyendo la verificación del Layout) ...
        
        # 3. Crear el gráfico usando los datos REALES
        canvas = self.create_simple_chart(
            "Distribución de Empleados por Rol (DB)", 
            datos, 
            labels
        )
        layout.addWidget(canvas)

    def navegar_a(self, indice_de_pagina):
        """
        Función que cambia la vista visible del QStackedWidget.
        """
        # Asume que tu QStackedWidget generado en ui_dashboard.py se llama 'stackedWidget'
        self.stackedWidget.setCurrentIndex(indice_de_pagina)
            # Lógica de navegación del stackedWidget
        
        # ----------------------------------------------------
        # Lógica de Reconexión del Botón Confirmar
        # ----------------------------------------------------
        
        # Paso 1: Resetear la conexión previa
        self.desconectar_btn_confirmar() 
        # 1. Desconecta (ya tienes esta parte)
        self.btnConfirmarCRUD.clicked.disconnect() 

        # 2. Conecta con el nombre CORRECTO
        self.btnConfirmarCRUD.clicked.connect(self.manejar_confirmar_vehiculo)
        # 2. Navegar a la página
        self.stackedWidget.setCurrentIndex(indice_de_pagina)

        # Paso 2: Conectar la función específica según el índice de la vista
        if indice_de_pagina == 0:  # Vista de Administración (Gestión Humana/Empleados)
            self.btnConfirmarCRUD.clicked.connect(self.manejar_confirmar_empleado)
            self.btnConfirmarCRUD.setVisible(True)
            
        elif indice_de_pagina == 1:  # Vista de Vehículos (Logística)
            # Debes tener una función CRUD específica para vehículos
            self.btnConfirmarCRUD.clicked.connect(self.manejar_confirmar_vehiculo)
            self.btnConfirmarCRUD.setVisible(True)

        elif indice_de_pagina == 3: # Ingeniería
            self.btnConfirmarCRUD.setVisible(True)
            self.btnConfirmarCRUD.clicked.connect(self.manejar_confirmar_ingenieria)
        
        else:
            # En el caso de "Usuarios" (índice 7) o "Visual", oculta y no conecta.
            self.btnConfirmarCRUD.setVisible(False)
            
        # Agrega aquí la lógica para otros índices (1, 4, 5, etc.)
        # elif index == 4: # Vista de Ingeniería
        #    self.btnConfirmar.clicked.connect(self.manejar_confirmar_ingenieria)

    def navegar_principal(self, indice_de_pagina):
        """Navega entre las vistas principales (Administrativo, Logistica, etc.)."""
        self.stackedWidget.setCurrentIndex(indice_de_pagina)

    def navegar_admin(self, indice_de_pagina):
        """Navega entre las vistas secundarias de la página Administrativo (View All, Add New)."""
        # Asume que el QStackedWidget secundario se llama 'stackedAdminPages' en ui_dashboard.py
        self.stackedAdminPages.setCurrentIndex(indice_de_pagina)
        

    # 1. Crear el grupo de botones
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True) # Solo uno puede estar chequeado a la vez
        
        # 2. Añadir todos los botones de la barra lateral al grupo
        self.button_group.addButton(self.btnAdministrativo)
        self.button_group.addButton(self.btnLogistico)
        self.button_group.addButton(self.btnVehiculos)
        # ... añade todos los demás botones (Ingenieria, Marketing, Usuarios)
        
        # 3. Conectar la señal a la navegación
        # Cada vez que un botón cambia su estado, llamamos a la función
        self.button_group.buttonClicked.connect(self.handle_navigation)

        # 4. Establecer el primer botón como seleccionado por defecto
        self.btnAdministrativo.setChecked(True) # O el botón que quieras que sea la vista inicial
        # ...
        
    def handle_navigation(self, button):
        """Maneja la navegación cuando un botón es clickeado y chequeado."""
        if button.isChecked():
            # Aquí iría tu lógica de QStackedWidget.setCurrentIndex()
            
            # Ejemplo: si el botón se llama btnAdministrativo, navega al índice 0
            if button.objectName() == "btnAdministrativo":
                self.stackedWidget.setCurrentIndex(0) 
            elif button.objectName() == "btnLogistico":
                self.stackedWidget.setCurrentIndex(1)
            # ... y así sucesivamente para cada botón.

    def configurar_dashboard_por_rol(self,rol):
        # Aquí implementarás la lógica para mostrar el contenido correcto.
        # Por ejemplo, usando un QStackedWidget o un mensaje inicial:
        print(f"Configurando vista para el rol: {self.rol}")
        
        rol = self.rol_seleccionado

        rol_mapeo = {
        "Administrativa": {
            "botones": [
                self.btnAdministrador, 
                self.btnIngenieria, 
                self.btnLogistico, 
                self.btnMarketing, 
                self.btnUsers, 
                self.btnVehicles
            ],
            "vista_inicial": 0 # Índice 0: Vista de Administrador/Empleados
        },
        "Ingeniería": {
            "botones": [
                self.btnIngenieria,
                self.btnVehicles # Asumo que Ingeniería puede ver la gestión de vehículos
            ],
            "vista_inicial": 3 # Asumo que la vista 4 es para Ingeniería
        },
        "Logística": { # Cuidado con el nombre, debe coincidir con el valor de la base de datos
            "botones": [
                self.btnLogistico, 
                self.btnVehicles
            ],
            "vista_inicial": 1 # Asumo que la vista 1 es para Logística
        },
        # Añade aquí los demás roles: "Marketing", "Cliente", etc.
        "Marketing": {
            "botones": [self.btnMarketing],
            "vista_inicial": 4 # Vista de Marketing
        },
        "Cliente": {
            "botones": [self.btnVehicles, self.btnUsers],
            "vista_inicial": 5 # Vista de Cliente
        }
        }

        # 2. Obtener TODOS los botones de navegación
        # Nota: Estos nombres los saco de tu setup_navigation
        botones_navegacion = [
            self.btnAdministrador, 
            self.btnLogistico,
            self.btnVehicles, 
            self.btnIngenieria, 
            self.btnMarketing, 
            self.btnUsers, 
            
        ]

        # 3. Aplicar la lógica de visibilidad y navegación
        if rol in rol_mapeo:
            config = rol_mapeo[rol]
            botones_permitidos = config["botones"]
            
            # Ocultar todos los botones primero
            for boton in botones_navegacion:
                boton.setVisible(False)
                
            # Mostrar solo los botones permitidos
            for boton in botones_permitidos:
                boton.setVisible(True)

            # Establecer la vista inicial
            self.stackedWidget.setCurrentIndex(config["vista_inicial"])
            
            # Seleccionar el primer botón del rol (para que aparezca resaltado)
            if botones_permitidos:
                botones_permitidos[0].setChecked(True)
        
        else:
            # Lógica de seguridad si el rol es desconocido (ocultar todo)
            for boton in botones_navegacion:
                boton.setVisible(False)
            # Opcional: mostrar un mensaje de error o una vista vacía
            # self.stackedWidget.setCurrentIndex(índice_vista_error)

           
    
    def manejar_confirmar_empleado(self):
        """
        Recupera datos de la interfaz, valida campos obligatorios 
        y guarda el nuevo empleado en la base de datos.
        """
        
        # ⭐️ 1. RECUPERAR DATOS DE LOS CAMPOS DE TEXTO
        nombre = self.txtNombre.text().strip()
        email = self.txtEmail.text().strip()
        telefono = self.txtTelefono.text().strip()
        cargo = self.txtCargo.text().strip()
        
        # Datos opcionales (si están vacíos, se manejan)
        id_empleado = self.txtIdEmpleado.text().strip() if self.txtIdEmpleado.text().strip() else 'N/A' 
        anio_ingreso = self.txtAnioIngreso.text().strip() if self.txtAnioIngreso.text().strip() else None
        genero = self.txtGenero.text().strip() if self.txtGenero.text().strip() else None
        
        # ⭐️ 2. VALIDACIÓN DE CAMPOS OBLIGATORIOS
        if not all([nombre, email, telefono, cargo]):
            # Muestra una advertencia si falta algún campo obligatorio
            QMessageBox.warning(self, "Error de Validación", 
                                "Los campos Nombre, Email, Teléfono y Cargo son obligatorios.")
            return

        # ⭐️ 3. PREPARAR Y GUARDAR DATOS
        
        # Si ID Empleado es obligatorio, la validación debe ir arriba.
        # Usaremos 'N/A' si el ID opcional se deja vacío. Si la DB requiere un ID único,
        # debemos generar uno si el campo está vacío.
        
        datos_empleado = (
            nombre,         # Valor 1: Se inserta en la columna 1 (nombre)
            email,          # Valor 2: Se inserta en la columna 2 (email)
            telefono,
            id_empleado,       # Valor 3: Se inserta en la columna 3 (telefono)
            cargo,          # Valor 4: ...
            anio_ingreso,
            genero   # <--- Asegúrate de tener esta variable si existe en tu tabla
            
        )
        
        if self.db.add_empleado(datos_empleado):
            QMessageBox.information(self, "Éxito", "Empleado registrado correctamente.")
            self.limpiar_campos_empleado()
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar el empleado. Verifique la base de datos o si el email ya existe.")

    def limpiar_campos_empleado(self):
        """Función para limpiar los campos después de una inserción exitosa."""
        self.txtNombre.clear()
        self.txtEmail.clear()
        self.txtTelefono.clear()
        self.txtIdEmpleado.clear()
        self.txtCargo.clear()
        self.txtAnioIngreso.clear()
        self.txtGenero.clear()

   # En Conexion.py (dentro de la clase MainDashboard)

    def manejar_confirmar_vehiculo(self):
        """Recupera datos de la interfaz de Vehículos y los guarda en la tabla 'vehiculos'."""
        
        # 1. RECUPERAR DATOS DE LOS CAMPOS DE TEXTO
        # IMPORTANTE: Usamos el nombre del campo en la UI, que es el VIN/Serial No (llave primaria)
        vin_serial_no = self.txtVINSerialNo.text().strip()  # <-- ASUME que el campo se llama 'self.txtVINSerialNo'
        marca = self.txtMarca.text().strip()
        modelo = self.txtModelo.text().strip()
        anio = self.txtAnio.text().strip()
        
        # Recuperar el resto de campos (Ajusta los nombres de los objetos QLineEdit)
        engine_type = self.txtEngineType.text().strip() 
        transmision = self.txtTransmision.text().strip()
        kilometraje = self.txtKilometraje.text().strip()
        estado = self.txtEstado.text().strip() 
        ultimo_mantenimiento = self.txtUltimoMantenimiento.text().strip() 

        # 2. VALIDACIÓN de campos obligatorios (NOT NULL: vin_serial_no, marca, modelo)
        if not all([vin_serial_no, marca, modelo]):
            QMessageBox.warning(self, "Error de Validación", "El VIN/Serial NO, Marca y Modelo son obligatorios para Vehículos.")
            return
        if not kilometraje:
            kilometraje = None
    
        if not ultimo_mantenimiento:
            ultimo_mantenimiento = None
            
        # 3. PREPARAR LOS DATOS (El orden es crucial y debe coincidir con la consulta SQL)
        datos_vehiculo = (
            vin_serial_no,
            marca, 
            modelo, 
            anio,
            engine_type,
            transmision,
            kilometraje,
            estado,
            ultimo_mantenimiento
        )

        # Llama al método add_vehiculo en db_manager
        if self.db.add_vehiculo(datos_vehiculo): 
            QMessageBox.information(self, "Éxito", "Vehículo registrado correctamente.")
            # self.limpiar_campos_vehiculo() # Si tienes un método de limpieza, úsalo aquí
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar el vehículo. Verifique la base de datos o si el VIN ya existe.")

        # En Conexion.py (dentro de la clase MainDashboard)
    def limpiar_campos_vehiculo(self):
        """Limpia todos los campos de entrada de la sección de vehículos."""
        self.txtVinSerialNo.setText("")
        self.txtMarca.setText("")
        self.txtModelo.setText("")
        self.txtAnio.setText("")
        self.txtEngineType.setText("")
        self.txtTransmision.setText("")
        self.txtKilometraje.setText("")
        self.txtEstado.setText("")
        self.txtUltimoMantenimiento.setText("")

    # En Conexion.py (Nueva Función)

    def manejar_editar_estado_vehiculo(self):
        # 1. Recuperar datos
        vin_serial_no = self.Ingebuton_2.text().strip() # Asumo que este es el LineEdit
        
        # Asumo que tienes un QComboBox para el estado, por ejemplo: self.cmbEstadoVehiculo
        nuevo_estado = self.Ingeline.text().strip()
        accion_seleccionada=self.Ingebox.currentText()
        

        if not vin_serial_no or not nuevo_estado:
            QMessageBox.warning(self, "Validación", "El ID del vehículo y el nuevo estado son obligatorios.")
            return

        # 2. Llamar al método de actualización en db_manager
        if self.db.obtener_estado_vehiculo(vin_serial_no, nuevo_estado,accion_seleccionada):
            QMessageBox.information(self, "Éxito", f"Estado del vehículo {vin_serial_no} actualizado a '{nuevo_estado}'.")
        else:
            QMessageBox.critical(self, "Error", "No se pudo actualizar el estado. Verifique el ID.")

    def manejar_confirmar_ingenieria(self):
        """
        Gestiona la lógica del botón Confirmar para la vista de Ingeniería.
        """
        QMessageBox.information(self, "Mensaje", "Lógica de Confirmar Ingeniería ejecutada.")
        #
        # Lógica real: Recuperar datos de los QLineEdit/QComboBox de Ingeniería
        # ...
        pass

        """
        Función CRUD para la vista de Ingeniería:
        1. Recupera el ID del vehículo (Ingeline/Ingeline_2).
        2. Recupera el tipo de acción/estado (Ingebox).
        3. Recupera el tiempo de reparación (Ingeline/Ingeline_2 - si aplica).
        4. Llama a un método en DatabaseManager para actualizar la tabla 'Vehiculos' o 'Reparaciones'.
        """
        vin = self.Ingebuton_2.text().strip()              # ID del vehículo
        accion_seleccionada = self.Ingebox.currentText()  # Qué desea?
        tiempo_reparacion = self.Ingeline.text().strip()

        # 2. Validación básica
        
        if not vin:
            QMessageBox.warning(self, "Error", "El VIN del vehículo es obligatorio.")
            return

        # Lógica de actualización usando el VIN
        if self.db.actualizar_estado_vehiculo(vin, accion_seleccionada, tiempo_reparacion): # <<-- ¡CORREGIDO!
            print('funciono')
        else:
            QMessageBox.critical(self, "Error", "No se pudo actualizar el estado del vehículo.")
        

        # EN Conexion.py (Dentro de class MainDashboard)

    def mostrar_grafica_reparacion(self):
        """Genera y muestra una gráfica de datos de reparación para el vehículo seleccionado."""
        vin = self.Ingeline.text().strip()
        
        if not vin:
            QMessageBox.warning(self, "Error", "Ingrese un ID de vehículo para ver la gráfica.")
            return
            
        # 1. Obtener datos de reparación
        # (Necesitarás crear un método en db_manager.py, ej: db.obtener_datos_reparacion(vehiculo_id))
        datos_reparacion = self.db.obtener_datos_reparacion(vin)
        
        if not datos_reparacion:
            QMessageBox.information(self, "Error", "No se encontraron datos de reparación para este vehículo.")
            return

        # 2. Crear la gráfica (reutilizando tu método create_simple_chart)
        # (Ajusta los datos y etiquetas según la estructura que devuelva tu DB)
        datos = [d[1] for d in datos_reparacion] # Ejemplo: solo la columna de valor
        labels = [d[0] for d in datos_reparacion] # Ejemplo: solo la columna de etiqueta
        
        canvas = self.create_simple_chart(
            f"Historial de Reparación de {vin}",
            datos,
            labels
        )

        # 3. Mostrar la gráfica en un diálogo o en una sección de la página
        # (Aquí puedes usar un QDialog o un QStackedWidget secundario)
        
        # Ejemplo con un diálogo (más simple):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Gráfica de Reparación")
        layout = QVBoxLayout(dialogo)
        layout.addWidget(canvas)
        dialogo.exec()


    def cargar_datos_vehiculo(self):
        """Consulta el estado del vehículo y actualiza los campos de Ingeniería."""
        vin = self.Ingeline.text().strip()
        
        if not vin:
            self.Ingebuton_2.clear() # Limpia el campo de tiempo
            return

        # 1. Obtener el estado del vehículo
        # (Necesitarás un método en db_manager.py, ej: db.obtener_estado_vehiculo(vehiculo_id))
        estado = self.db.obtener_estado_vehiculo(vin) 
        
        if estado == "En reparación":
            # Puedes obtener el tiempo si ya existe o dejarlo vacío para que lo ingrese
            self.Ingebuton_2.setText("") 
            self.Ingebox.setCurrentText("Reparado") # Sugiere el siguiente estado
        else:
            # El carro está bien ("Operativo", "Terminado", etc.)
            pass

    def setup_navigation(self):
        """Inicializa el grupo de botones y conecta la señal de navegación."""
            
        # Crea un grupo de botones para gestionar todos los botones de la barra lateral
        self.button_group = QButtonGroup(self) 
        self.button_group.setExclusive(True) # Opcional: solo un botón puede estar "chequeado" a la vez
            
        # 1. Añadir todos los botones al grupo
        self.button_group.addButton(self.btnAdministrador)
        self.button_group.addButton(self.btnLogistico)
        self.button_group.addButton(self.btnIngenieria)
        self.button_group.addButton(self.btnMarketing)
        self.button_group.addButton(self.btnUsers)
        self.button_group.addButton(self.btnVehicles) # El botón 'Visual'
            
        # 2. Conectar la señal de click de CUALQUIER botón del grupo
        self.button_group.buttonClicked.connect(self.handle_navigation)

        # 3. Establecer el primer botón como seleccionado (opcional, pero útil)
        self.btnAdministrador.setChecked(True)
        # Esto llamará automáticamente a handle_navigation y establecerá el índice 0.
        
        self.btnAdministrador.clicked.connect(lambda: self.navegar_a(0))
        self.btnLogistico.clicked.connect(lambda: self.navegar_a(1))
        self.btnVehicles.clicked.connect(lambda: self.navegar_a(2)) 
        self.btnIngenieria.clicked.connect(lambda: self.navegar_a(3)) 
        self.btnMarketing.clicked.connect(lambda: self.navegar_a(4)) 
        self.btnUsers.clicked.connect(lambda: self.navegar_a(5)) 


    # En Conexion.py (en algún lugar donde manejas la navegación, ej: handle_navigation o una función auxiliar)

    def configurar_acciones_por_vista(self, indice_de_vista):
        # 1. Limpiar cualquier conexión previa del botón Confirmar
        self.btnConfirmarCRUD.clicked.disconnect() 
        
        # 2. Conectar la acción específica según la vista
        if indice_de_vista == 0: # Vista de Administrador/Empleados
            self.btnConfirmarCRUD.clicked.connect(self.manejar_confirmar_empleado)
        
        # Si la vista es Ingeniería (Índice 4)
        elif indice_de_vista == 4: 
            # ⭐ NUEVA FUNCIÓN: Manejar la edición del estado del vehículo
            self.btnConfirmarCRUD.clicked.connect(self.manejar_editar_estado_vehiculo)
            
        # Agrega la lógica para otras vistas si usan el botón Confirmar.
        


    def desconectar_btn_confirmar(self):
        """Desconecta todas las señales previas del botón Confirmar."""
        try:
        # Asegúrate de que el botón existe y tiene la señal 'clicked'
            self.btnConfirmarCRUD.clicked.disconnect()
        except TypeError:
        # Esto ignora el error si no hay ninguna conexión activa, 
        # permitiendo que el código continúe.
            pass
        except AttributeError:
        # Maneja el caso en que el objeto self.btnConfirmarCRUD no está listo
            pass

    

              

class DialogoInicio(QDialog,Ui_Dialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setObjectName("DialogoInicio")
        self.setFixedSize(1020, 850)

        
        #self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAutoFillBackground(False)

        self.labelBienvenido.setAutoFillBackground(False)

        self.pushButton.setAutoFillBackground(False)
        # CONEXIONES
        self.pushButton.clicked.connect(self.manejar_confirmacion)
        
        # ⭐️ Solución para la repetición: Limpiar el ComboBox antes de añadir
        self.comboBox.clear() # <--- ¡Añade esta línea!
        
        # Agrega los roles al ComboBox
        self.comboBox.addItems([
            "Seleccione Su Rol", # Opción por defecto
            "Administrativa",
            "Logística",
            "Ingeniería",
            "Marketing",
            "Cliente",
            
        ])
        
        # Opcional: Para que "Seleccione Su Rol" sea el texto inicial, pero no una opción seleccionable
        self.comboBox.setCurrentText("Seleccione Su Rol")
        #self.comboBox.setItemData(0, False, Qt.ItemIsEnabled) # Deshabilita la primera opción (más avanzado)
        self.comboBox.model().item(0).setEnabled(False)
        
        # ... (resto del init) ...
        self.main_window = None
        self.pushButton.clicked.connect(self.manejar_confirmacion)

    def manejar_confirmacion(self):
        rol = self.comboBox.currentText()
        
        if rol == "Seleccione Su Rol":
            # Si no ha seleccionado nada, muestra una advertencia
            QMessageBox.warning(self, "Error de Selección", 
                                "Por favor, seleccione un rol para continuar.")
            return
        
        # 1. Almacenar el rol seleccionado en una propiedad del diálogo:
        self.rol_seleccionado = rol

        # 2. ⭐️ CERRAR el diálogo con ÉXITO (QDialog.Accepted):
    # Esto hace que el bloque 'if ventana_inicio.exec() == QDialog.Accepted' sea verdadero.
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    RUTA_DEL_ESTILO = os.path.join(BASE_DIR, "CarStyle.qss")
    cargar_estilos_qss(app, RUTA_DEL_ESTILO)
    
    # 1. Lanzar el Diálogo de Inicio
    ventana_inicio = DialogoInicio()
    
    # Variable para almacenar el rol, si es aceptado
    rol_seleccionado = None
    
    # exec() detiene la ejecución hasta que el diálogo se cierra
    if ventana_inicio.exec() == QDialog.Accepted:
        # Si el diálogo se cierra con self.accept(), guardamos el rol
        rol_seleccionado = ventana_inicio.rol_seleccionado
        
    # La ventana de inicio se cierra aquí.
    
    # ⭐️ 2. VERIFICAR ROL Y LANZAR EL DASHBOARD
    if rol_seleccionado:

        main_app = MainDashboard(rol_seleccionado)
        main_app.show()
        # ⭐️ 3. Ejecutamos el bucle de eventos SOLO AHORA.
        sys.exit(app.exec())
    
    else:
        # Si el usuario canceló el diálogo (rol_seleccionado es None), 
        # cerramos la aplicación inmediatamente.
        sys.exit(0)

    def get_distribucion_empleados(self):
        """Obtiene el conteo de empleados por cargo."""
        # Nota: Usamos 'cargo' basado en la columna visible en MySQL
        query = "SELECT cargo, COUNT(*) FROM Empleados GROUP BY cargo"
        
        # Esto retorna una lista de tuplas: [('admin', 1), ('logistica', 2), ...]
        return self.execute_read_query(query) # Asume que tienes un método para leer consultas



# ⭐️ 1. Inicializar la Base de Datos ⭐️
DB = DatabaseManager()

# ... (El resto del código de lanzamiento de la ventana)
# En la línea 138 (o similar) al lanzar el dashboard:
main_app = MainDashboard(rol_seleccionado, db_instance=DB)
main_app.show()
app.exec()