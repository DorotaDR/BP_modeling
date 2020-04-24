# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_v2.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import os

import pandas as pd

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(1200, 650)
        MainWindow.setWindowTitle("BPMN")


        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(5, -1, -1, -1)


        self.gridLayout = QtWidgets.QGridLayout()
        self.comboBox_alg = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_alg.addItem("")
        self.comboBox_alg.addItem("")
        self.comboBox_alg.setMaximumSize(QtCore.QSize(100, 16777215))


        self.gridLayout.addWidget(self.comboBox_alg, 3, 0, 1, 1)
        self.label_param = QtWidgets.QLabel(self.centralwidget)

        self.gridLayout.addWidget(self.label_param, 4, 0, 1, 1)
        self.doubleSpinBox_paramerer = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_paramerer.setDecimals(2)
        self.doubleSpinBox_paramerer.setMaximum(1.0)
        self.doubleSpinBox_paramerer.setSingleStep(0.1)
        self.doubleSpinBox_paramerer.setMaximumSize(QtCore.QSize(50, 16777215))


        self.gridLayout.addWidget(self.doubleSpinBox_paramerer, 4, 1, 1, 1)
        self.label_log_file_2 = QtWidgets.QLabel(self.centralwidget)

        self.gridLayout.addWidget(self.label_log_file_2, 5, 0, 1, 1)
        self.label_log_file = QtWidgets.QLabel(self.centralwidget)

        self.gridLayout.addWidget(self.label_log_file, 0, 0, 1, 1)
        self.lineEdit_filename = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_filename.setReadOnly(True)
        self.lineEdit_filename.setMaximumSize(QtCore.QSize(200, 16777215))


        self.gridLayout.addWidget(self.lineEdit_filename, 1, 0, 1, 1)
        self.pushButton_choose_file = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_choose_file.clicked.connect(self.file_open)
        self.pushButton_choose_file.setMaximumSize(QtCore.QSize(50, 16777215))


        self.gridLayout.addWidget(self.pushButton_choose_file, 1, 1, 1, 1)
        self.label_alg = QtWidgets.QLabel(self.centralwidget)

        self.gridLayout.addWidget(self.label_alg, 2, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setMaximumSize(QtCore.QSize(300, 16777215))


        self.verticalLayout_2.addWidget(self.textBrowser)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView = QtWidgets.QGraphicsView(self.scene, self.centralwidget)

        self.horizontalLayout.addWidget(self.graphicsView)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 734, 21))

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.MainWindow = MainWindow


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.comboBox_alg.setItemText(0, _translate("MainWindow", "Alpha Miner"))
        self.comboBox_alg.setItemText(1, _translate("MainWindow", "Heuristic Miner"))
        self.label_param.setText(_translate("MainWindow", "ParameterValue"))
        self.label_log_file_2.setText(_translate("MainWindow", "Output"))
        self.label_log_file.setText(_translate("MainWindow", "Log file:"))
        self.pushButton_choose_file.setText(_translate("MainWindow", "Choose"))
        self.label_alg.setText(_translate("MainWindow", "Algorithm"))

    def display_image(self, img_filename):
        self.scene.clear()
        pixMap = QtGui.QPixmap(img_filename)
        self.scene.addPixmap(pixMap)
        # self.view.fitInView(QtWidgets.QRectF(0, 0, w, h), QtCore.Qt.KeepAspectRatio)
        self.scene.update()

    def file_open(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self.MainWindow, 'Open File')[0]
        print("\n ------\n File to open: ", name)
        #Validate image
        if '.png' in name.lower() or '.jpg' in name.lower() or ".jpeg" in name.lower():
            # self.original_file_path = name
            self.lineEdit_filename.setText(os.path.basename(name))
        return name

    def set_output(self, to_print=None):
        from collections import OrderedDict

        d = OrderedDict([('a', {}), ('b', {'a': 6, 'b': 3}), ('c', {'b': 3, 'd': 3}), ('d', {'c': 3, 'b': 3}), ('e', {'d': 2}), ('f', {'g': 3, 'd': 1, 'c': 3}), ('g', {'f': 3}), ('h', {'e': 2, 'f': 4})])
        df = pd.DataFrame.from_dict(d).fillna(" ")
        # df.columns = [f"_{col}_" for col in df.columns]

        self.textBrowser.setHtml(df.to_html())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    ui.setupUi(MainWindow)

    ui.display_image("./../results/alpha_result.png")

    ui.set_output()

    MainWindow.show()
    sys.exit(app.exec_())
