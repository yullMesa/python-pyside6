#!/usr/bin/env python3
"""
Script para lanzar AutoMetrics con rol Cliente para pruebas de UI.
Permite visualizar:
- label_18 con imagen del carro
- label_19 con gráfica de ingeniería
- btnLista para seleccionar VIN aleatorio
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'AutoMetrics')))

from AutoMetrics.Conexion import MainDashboard
from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Crear y mostrar MainDashboard con rol Cliente
    print("[LAUNCHER] Iniciando AutoMetrics con rol Cliente...")
    window = MainDashboard('Cliente')
    window.show()
    
    print("[LAUNCHER] Ventana mostrada. Presiona Ctrl+C o cierra la ventana para salir.")
    sys.exit(app.exec())
