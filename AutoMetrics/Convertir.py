import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

def convertir_csv_a_xlsx():
    """
    Abre un diálogo de selección de archivo para elegir un CSV, 
    y lo convierte a un archivo XLSX en la misma ubicación.
    """
    
    # 1. Configurar Tkinter para el diálogo de selección (se ejecuta en segundo plano)
    root = tk.Tk()
    root.withdraw() # Oculta la ventana principal de Tkinter

    # 2. Abrir el diálogo para seleccionar el archivo CSV de entrada
    ruta_csv = filedialog.askopenfilename(
        title="Selecciona el archivo CSV a convertir",
        filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*"))
    )

    if not ruta_csv:
        print("\n❌ Operación cancelada: No se seleccionó ningún archivo.")
        return

    print(f"\n✅ Archivo CSV seleccionado: {ruta_csv}")

    try:
        # 3. Leer el CSV
        # Usamos el separador ';' y encoding 'latin1' basado en las necesidades de tu proyecto
        df = pd.read_csv(ruta_csv, sep=',', encoding='latin1')
        print(f"   CSV leído. Total de filas: {len(df)}")

        # 4. Crear la ruta del archivo XLSX de salida
        # Reemplazamos la extensión .csv con .xlsx en la misma ubicación
        ruta_xlsx = ruta_csv.replace(".csv", ".xlsx")
        
        # Si el archivo CSV tenía la extensión en mayúsculas (.CSV), lo manejamos
        if ruta_xlsx == ruta_csv:
             ruta_xlsx = os.path.splitext(ruta_csv)[0] + ".xlsx"

        # 5. Escribir el DataFrame al archivo XLSX
        # Usamos ExcelWriter para escribir la hoja (que tendrá el nombre 'Hoja1' por defecto)
        with pd.ExcelWriter(ruta_xlsx, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Hoja_Exportada', index=False)
        
        print(f"🎉 ¡Conversión Exitosa!")
        print(f"   Archivo XLSX guardado en: {ruta_xlsx}")

    except Exception as e:
        print(f"\n❌ Ocurrió un error durante la conversión: {e}")
        print("   Asegúrate de que el CSV esté correctamente formateado (separador ';').")



if __name__ == "__main__":
    convertir_csv_a_xlsx()