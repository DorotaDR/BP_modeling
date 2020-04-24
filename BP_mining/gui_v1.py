# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_v1.ui'
#
# Created by: PyQt5 UI code generator 5.14.2

from PyQt5 import QtCore, QtGui, QtWidgets

import os

import pandas as pd

from PIL import Image


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(671, 493)
        self.MainWindow = MainWindow

        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView = QtWidgets.QGraphicsView(self.scene, self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(230, 10, 401, 441))

        self.doubleSpinBox_paramerer = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_paramerer.setGeometry(QtCore.QRect(100, 150, 62, 22))
        self.doubleSpinBox_paramerer.setDecimals(2)
        self.doubleSpinBox_paramerer.setMaximum(1.0)
        self.doubleSpinBox_paramerer.setSingleStep(0.1)

        self.label_param = QtWidgets.QLabel(self.centralwidget)
        self.label_param.setGeometry(QtCore.QRect(10, 150, 71, 21))

        self.comboBox_alg = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_alg.setGeometry(QtCore.QRect(10, 110, 171, 21))

        self.comboBox_alg.addItem("")
        self.comboBox_alg.addItem("")

        self.label_alg = QtWidgets.QLabel(self.centralwidget)
        self.label_alg.setGeometry(QtCore.QRect(10, 90, 47, 13))

        self.pushButton_choose_file = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_choose_file.clicked.connect(self.file_open)
        self.pushButton_choose_file.setGeometry(QtCore.QRect(130, 40, 75, 23))

        self.lineEdit_filename = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_filename.setGeometry(QtCore.QRect(10, 40, 113, 20))
        self.lineEdit_filename.setReadOnly(True)

        self.label_log_file = QtWidgets.QLabel(self.centralwidget)
        self.label_log_file.setGeometry(QtCore.QRect(10, 20, 47, 13))

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 220, 191, 221))

        self.label_log_file_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_log_file_2.setGeometry(QtCore.QRect(10, 200, 47, 13))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 671, 21))

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_param.setText(_translate("MainWindow", "ParameterValue"))
        self.comboBox_alg.setItemText(0, _translate("MainWindow", "Alpha Miner"))
        self.comboBox_alg.setItemText(1, _translate("MainWindow", "Heuristic Miner"))
        self.label_alg.setText(_translate("MainWindow", "Algorithm"))
        self.pushButton_choose_file.setText(_translate("MainWindow", "Choose"))
        self.label_log_file.setText(_translate("MainWindow", "Log file:"))
        self.label_log_file_2.setText(_translate("MainWindow", "Output"))

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
        df = pd.DataFrame.from_dict(d)
        self.textBrowser.setHtml(df.to_html())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)


    ui.display_image("./../results/alpha_result.png")

    ui.set_output()

    MainWindow.show()
    sys.exit(app.exec_())
