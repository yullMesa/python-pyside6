import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'AutoMetrics')))
from Conexion import MainDashboard
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

if __name__ == '__main__':
    app = QApplication([])
    
    # Crear MainDashboard con rol Cliente
    print("[INIT] Iniciando MainDashboard con rol Cliente...")
    win = MainDashboard('Cliente')
    
    # Ejecutar tests después de que se renderice
    def run_tests():
        print("\n=== VERIFICACIÓN DE USUARIOS PAGE ===")
        print(f"✓ vehiculos_users: {len(win.vehiculos_users)} vehículos")
        print(f"✓ Primer VIN: {win.vehiculos_users[0][0]}")
        print(f"✓ label_18 visible: {win.label_18.isVisible() if hasattr(win, 'label_18') else 'N/A'}")
        print(f"✓ label_19 visible: {win.label_19.isVisible() if hasattr(win, 'label_19') else 'N/A'}")
        print(f"✓ btnLista visible: {win.btnLista.isVisible() if hasattr(win, 'btnLista') else 'N/A'}")
        
        # Simular clic en btnLista (seleccionar VIN aleatorio)
        print("\n=== SIMULANDO CLIC EN btnLista ===")
        if hasattr(win, 'btnLista') and win.btnLista:
            win.seleccionar_vehiculo_azar()
            print(f"✓ btnLista.clicked() ejecutado")
        
        print("\n[DONE] Test completado. Closing...")
        app.quit()
    
    # Ejecutar tests después de 200ms
    QTimer.singleShot(200, run_tests)
    app.exec()
