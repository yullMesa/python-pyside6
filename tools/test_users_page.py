import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'AutoMetrics')))
from Conexion import MainDashboard
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

if __name__ == '__main__':
    app = QApplication([])
    win = MainDashboard('Cliente')
    
    # NO mostrar la ventana, solo procesar evento loop
    # win.show()  # Comentado
    
    # Usamos un timer para ejecutar el test después de que la UI se renderice
    def run_tests():
        print("[TEST] MainDashboard iniciado con rol Cliente")
        print(f"[TEST] stackedWidget.currentIndex() = {win.stackedWidget.currentIndex()} (debe ser 5)")
        print(f"[TEST] btnUsers.isVisible() = {win.btnUsers.isVisible()} (debe ser True)")
        print(f"[TEST] btnAdministrador.isVisible() = {win.btnAdministrador.isVisible()} (debe ser False)")
        
        # Verificar que los labels existen
        if hasattr(win, 'label_18') and win.label_18:
            print(f"[TEST] label_18 encontrado: {win.label_18.objectName()}")
        else:
            print("[TEST] ERROR: label_18 NO encontrado")
        
        if hasattr(win, 'label_19') and win.label_19:
            print(f"[TEST] label_19 encontrado: {win.label_19.objectName()}")
        else:
            print("[TEST] ERROR: label_19 NO encontrado")
        
        # Verificar que vehiculos_users está poblado
        if hasattr(win, 'vehiculos_users') and win.vehiculos_users:
            print(f"[TEST] vehiculos_users poblado: {len(win.vehiculos_users)} vehículos")
            print(f"[TEST] Primer vehículo VIN: {win.vehiculos_users[0][0]}")
        else:
            print("[TEST] ERROR: vehiculos_users NO poblado")
        
        # Verificar que btnLista está conectado
        if hasattr(win, 'btnLista') and win.btnLista:
            print(f"[TEST] btnLista encontrado: {win.btnLista.objectName()}")
            print(f"[TEST] btnLista.isVisible(): {win.btnLista.isVisible()}")
        else:
            print("[TEST] ERROR: btnLista NO encontrado")
        
        print("[TEST] Todas las verificaciones completadas.")
        app.quit()
    
    # Ejecutar tests después de 100ms
    QTimer.singleShot(100, run_tests)
    app.exec()
