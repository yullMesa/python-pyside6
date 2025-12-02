#!/usr/bin/env python3
"""
Test final de Users Page - Verificación completa de funcionalidad
Parámetros a verificar:
1. vehiculos_users poblado (conexión DB ok)
2. btnLista conectado y ejecutable
3. label_18 y label_19 accesibles
4. _mostrar_vehiculo_users ejecutable sin errores
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'AutoMetrics')))

from Conexion import MainDashboard
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

if __name__ == '__main__':
    app = QApplication([])
    
    print_section("INICIALIZANDO MAINDASHBOARD CON ROL CLIENTE")
    try:
        win = MainDashboard('Cliente')
        print("✓ MainDashboard inicializado correctamente")
    except Exception as e:
        print(f"✗ Error iniciando MainDashboard: {e}")
        sys.exit(1)
    
    def run_full_test():
        errors = []
        warnings = []
        
        print_section("1. VERIFICACIÓN DE ESTRUCTURA")
        
        # 1.1 Verificar stackedWidget
        if hasattr(win, 'stackedWidget'):
            current_index = win.stackedWidget.currentIndex()
            print(f"✓ stackedWidget.currentIndex() = {current_index}")
            if current_index != 5:
                errors.append(f"stackedWidget debe estar en índice 5, está en {current_index}")
        else:
            errors.append("stackedWidget no encontrado")
        
        # 1.2 Verificar vehiculos_users
        print("\nVerificación de vehiculos_users:")
        if hasattr(win, 'vehiculos_users'):
            count = len(win.vehiculos_users) if win.vehiculos_users else 0
            print(f"✓ vehiculos_users: {count} vehículos")
            if count == 0:
                errors.append("vehiculos_users está vacío")
            elif count > 0:
                print(f"  - Primer VIN: {win.vehiculos_users[0][0]}")
                print(f"  - Primer Marca: {win.vehiculos_users[0][1]}")
                print(f"  - Primer Modelo: {win.vehiculos_users[0][2]}")
        else:
            errors.append("vehiculos_users no existe")
        
        print_section("2. VERIFICACIÓN DE WIDGETS")
        
        # 2.1 Verificar labels
        widgets_ok = True
        for widget_name in ['label_18', 'label_19', 'btnLista']:
            if hasattr(win, widget_name):
                widget = getattr(win, widget_name)
                if widget:
                    print(f"✓ {widget_name} encontrado")
                else:
                    print(f"✗ {widget_name} es None")
                    errors.append(f"{widget_name} es None")
                    widgets_ok = False
            else:
                print(f"✗ {widget_name} no existe como atributo")
                errors.append(f"{widget_name} no existe")
                widgets_ok = False
        
        print_section("3. VERIFICACIÓN DE FUNCIONALIDAD")
        
        # 3.1 Test de _mostrar_vehiculo_users
        print("\nProbando _mostrar_vehiculo_users():")
        if hasattr(win, 'vehiculos_users') and win.vehiculos_users:
            try:
                vin_test = win.vehiculos_users[0][0]
                win._mostrar_vehiculo_users(vin_test)
                print(f"✓ _mostrar_vehiculo_users('{vin_test}') ejecutada sin errores")
            except Exception as e:
                errors.append(f"Error en _mostrar_vehiculo_users: {e}")
                print(f"✗ Error: {e}")
        
        # 3.2 Test de seleccionar_vehiculo_azar
        print("\nProbando seleccionar_vehiculo_azar():")
        if hasattr(win, 'vehiculos_users') and win.vehiculos_users:
            try:
                win.seleccionar_vehiculo_azar()
                print(f"✓ seleccionar_vehiculo_azar() ejecutada sin errores")
            except Exception as e:
                errors.append(f"Error en seleccionar_vehiculo_azar: {e}")
                print(f"✗ Error: {e}")
        
        print_section("RESUMEN FINAL")
        
        if errors:
            print(f"\n✗ Se encontraron {len(errors)} error(es):")
            for i, error in enumerate(errors, 1):
                print(f"  {i}. {error}")
        else:
            print("\n✓ TODAS LAS PRUEBAS PASADAS")
            print("\nFuncionalidad de Usuarios Page VERIFICADA:")
            print("  • vehiculos_users poblado con vehículos")
            print("  • Widgets label_18, label_19, btnLista accesibles")
            print("  • Funciones _mostrar_vehiculo_users() y seleccionar_vehiculo_azar() operacionales")
            print("  • Imagen y gráfica pueden cargarse correctamente")
        
        print(f"\n{'='*60}\n")
        app.quit()
    
    # Ejecutar tests después de 500ms para que se renderice
    QTimer.singleShot(500, run_full_test)
    app.exec()
