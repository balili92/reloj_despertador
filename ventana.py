from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(360, 437)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout principal vertical para centralwidget
        self.layout_principal = QtWidgets.QVBoxLayout(self.centralwidget)
        self.layout_principal.setContentsMargins(20, 20, 20, 20)
        self.layout_principal.setSpacing(15)

        # Label "Hora actual"
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.layout_principal.addWidget(self.label)

        # Label para mostrar la hora actual
        self.reloj = QtWidgets.QLabel(self.centralwidget)
        self.reloj.setFrameShape(QtWidgets.QFrame.Box)
        self.reloj.setAlignment(QtCore.Qt.AlignCenter)
        self.reloj.setMinimumHeight(40)
        self.reloj.setObjectName("reloj")
        self.layout_principal.addWidget(self.reloj)

        # Widget para la selección de hora de alarma con layout vertical
        self.widget_hora_alarma = QtWidgets.QWidget(self.centralwidget)
        self.layout_hora_alarma = QtWidgets.QVBoxLayout(self.widget_hora_alarma)
        self.layout_hora_alarma.setContentsMargins(0, 0, 0, 0)

        self.hora_alarma = QtWidgets.QTimeEdit(self.widget_hora_alarma)
        self.hora_alarma.setDisplayFormat("HH:mm")
        self.hora_alarma.setObjectName("hora_alarma")
        self.layout_hora_alarma.addWidget(self.hora_alarma)
        self.layout_principal.addWidget(self.widget_hora_alarma)

        # Layout horizontal para botones
        self.widget_botones = QtWidgets.QWidget(self.centralwidget)
        self.layout_botones = QtWidgets.QHBoxLayout(self.widget_botones)
        self.layout_botones.setContentsMargins(0, 0, 0, 0)
        self.layout_botones.setSpacing(10)

        self.establecer_alarma = QtWidgets.QPushButton("Establecer alarma", self.widget_botones)
        self.establecer_alarma.setObjectName("establecer_alarma")
        self.borrar_alarma = QtWidgets.QPushButton("Borrar alarma", self.widget_botones)
        self.borrar_alarma.setObjectName("borrar_alarma")

        self.layout_botones.addWidget(self.establecer_alarma)
        self.layout_botones.addWidget(self.borrar_alarma)
        self.layout_principal.addWidget(self.widget_botones)

        # Label para mensajes (puede crecer verticalmente)
        self.label_mensaje = QtWidgets.QLabel(self.centralwidget)
        self.label_mensaje.setWordWrap(True)
        self.label_mensaje.setObjectName("label_mensaje")
        self.layout_principal.addWidget(self.label_mensaje)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Reloj Despertador"))
        self.label.setText(_translate("MainWindow", "Hora actual"))
        self.establecer_alarma.setText(_translate("MainWindow", "Establecer alarma"))
        self.borrar_alarma.setText(_translate("MainWindow", "Borrar alarma"))
        self.label_mensaje.setText(_translate("MainWindow", ""))  # Inicialmente vacío
