import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'AutoMetrics')))
from Conexion import MainDashboard
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

if __name__ == '__main__':
    app = QApplication([])
    print('[TEST] Iniciando MainDashboard con rol Ingeniería')
    win = MainDashboard('Ingeniería')

    def check():
        print('[TEST] stacked index =', win.stackedWidget.currentIndex())
        fg = getattr(win, 'frameGraficos', None)
        if fg is None:
            print('[TEST] No existe frameGraficos en la UI')
        else:
            layout = fg.layout()
            if layout is None:
                print('[TEST] frameGraficos no tiene layout')
            else:
                print('[TEST] frameGraficos widgets count =', layout.count())
                for i in range(layout.count()):
                    item = layout.itemAt(i)
                    w = item.widget()
                    print(' - widget:', type(w))
        # Revisar la página visual (stacked index 3) directamente
        visual_page = win.stackedWidget.widget(3)
        if visual_page is None:
            print('[TEST] visual_page (index 3) es None')
        else:
            vl = visual_page.layout()
            if vl is None:
                print('[TEST] visual_page no tiene layout')
            else:
                print('[TEST] visual_page layout widgets count =', vl.count())
                for i in range(vl.count()):
                    item = vl.itemAt(i)
                    w = item.widget()
                    print(' - visual widget:', type(w))
        app.quit()
    QTimer.singleShot(300, check)
    app.exec()