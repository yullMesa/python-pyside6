import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'AutoMetrics')))
from Conexion import MainDashboard
from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication([])
    win = MainDashboard('Administrativa')
    # Cargar Users page and force a random selection to trigger image load
    win.load_users_page()
    # Asegurarse de que vehiculos_marketing esté poblado para la selección
    try:
        win.vehiculos_marketing = win.db.obtener_lista_vehiculos()
    except Exception:
        win.vehiculos_marketing = []

    # Trigger random selection (this will print debug from mostrar_imagen_por_vin)
    win.seleccionar_vehiculo_azar()
    print('UI test executed; exiting.')
    # Do not exec app loop; just cleanup
    app.exit(0)
