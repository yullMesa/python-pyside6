# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QLabel,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1169, 900)
        Dialog.setMinimumSize(QSize(1000, 900))
        Dialog.setMaximumSize(QSize(1243, 751))
        self.labelBienvenido = QLabel(Dialog)
        self.labelBienvenido.setObjectName(u"labelBienvenido")
        self.labelBienvenido.setGeometry(QRect(150, 80, 771, 151))
        self.labelBienvenido.setMaximumSize(QSize(100000, 1000))
        font = QFont()
        font.setPointSize(90)
        font.setBold(True)
        self.labelBienvenido.setFont(font)
        self.labelBienvenido.setStyleSheet(u"border-radius: 20px;\n"
"color: rgb(255, 255, 255);\n"
"\n"
"")
        self.labelBienvenido.setScaledContents(True)
        self.labelBienvenido.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.comboBox = QComboBox(Dialog)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(260, 540, 511, 91))
        font1 = QFont()
        font1.setPointSize(36)
        font1.setBold(True)
        self.comboBox.setFont(font1)
        self.comboBox.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        self.comboBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.comboBox.setStyleSheet(u"border-radius: 15px;\n"
"color: rgb(255, 255, 255);\n"
"")
        self.comboBox.setCurrentText(u"    Seleccione Su Rol")
        self.comboBox.setFrame(False)
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(340, 680, 401, 71))
        font2 = QFont()
        font2.setPointSize(24)
        font2.setBold(True)
        self.pushButton.setFont(font2)
        self.pushButton.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        self.pushButton.setStyleSheet(u"border-radius: 15px;\n"
"color: rgb(255, 255, 255);")

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
#if QT_CONFIG(tooltip)
        Dialog.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.labelBienvenido.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><img src=\":/newPrefix/carro.png\"/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelBienvenido.setText(QCoreApplication.translate("Dialog", u"Bienvenido a:", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"    Seleccione Su Rol", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Administrativo", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Dialog", u"Logistico", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Dialog", u"Ingenieria", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Dialog", u"Marketing", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("Dialog", u"Cliente", None))

        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Confirmar", None))
    # retranslateUi

