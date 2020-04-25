# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_v2.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import os

from BP_mining import *

import pandas as pd

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.algorithm_type = None
        self.param_value = None
        self.miner = None


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
        self.comboBox_alg.setMaximumSize(QtCore.QSize(100, 20))


        self.gridLayout.addWidget(self.comboBox_alg, 3, 0, 1, 1)
        self.label_param = QtWidgets.QLabel(self.centralwidget)
        self.label_param.setMaximumSize(QtCore.QSize(16777215, 20))

        self.gridLayout.addWidget(self.label_param, 4, 0, 1, 1)
        self.doubleSpinBox_param = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_param.setDecimals(2)
        self.doubleSpinBox_param.setMaximum(1.0)
        self.doubleSpinBox_param.setSingleStep(0.1)
        self.doubleSpinBox_param.setMaximumSize(QtCore.QSize(50, 20))
        self.gridLayout.addWidget(self.doubleSpinBox_param, 4, 1, 1, 1)

        self.label_log_file = QtWidgets.QLabel(self.centralwidget)
        self.label_log_file.setMaximumSize(QtCore.QSize(16777215, 20))
        self.gridLayout.addWidget(self.label_log_file, 0, 0, 1, 1)


        self.lineEdit_filename = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_filename.setReadOnly(True)
        self.lineEdit_filename.setMaximumSize(QtCore.QSize(200, 20))


        self.gridLayout.addWidget(self.lineEdit_filename, 1, 0, 1, 1)
        self.pushButton_choose_file = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_choose_file.clicked.connect(self.file_open)
        self.pushButton_choose_file.setMaximumSize(QtCore.QSize(50, 20))


        self.gridLayout.addWidget(self.pushButton_choose_file, 1, 1, 1, 1)
        self.label_alg = QtWidgets.QLabel(self.centralwidget)
        self.label_alg.setMaximumSize(QtCore.QSize(16777215, 20))

        self.gridLayout.addWidget(self.label_alg, 2, 0, 1, 1)

        self.pushButton_go = QtWidgets.QPushButton(self.centralwidget)
        self.gridLayout.addWidget(self.pushButton_go, 5, 0, 1, 1)
        self.pushButton_go.setText("Go!")
        self.pushButton_go.setMaximumSize(QtCore.QSize(16777215, 20))
        self.pushButton_go.clicked.connect(self.update)

        self.verticalLayout_2.addLayout(self.gridLayout)

        self.label_output = QtWidgets.QLabel(self.centralwidget)
        self.label_output.setMaximumSize(QtCore.QSize(16777215, 15))
        self.verticalLayout_2.addWidget(self.label_output)

        self.comboBox_matrix = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_matrix.addItem("Relation Matrix")
        self.comboBox_matrix.addItem("2-loop Matrix")
        self.comboBox_matrix.currentIndexChanged.connect(self.update_output_df)
        self.verticalLayout_2.addWidget(self.comboBox_matrix)

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setMaximumSize(QtCore.QSize(300, 300))


        self.verticalLayout_2.addWidget(self.textBrowser)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView = QtWidgets.QGraphicsView(self.scene, self.centralwidget)
        self.horizontalLayout.addWidget(self.graphicsView)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 3)
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
        self.label_output.setText(_translate("MainWindow", "Output"))
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
        if '.xes' in name.lower():
            # self.original_file_path = name
            self.lineEdit_filename.setText(os.path.basename(name))
            self.log_fn = name
        return name

    def set_output(self, dataframe: pd.DataFrame):
        from collections import OrderedDict

        # d = OrderedDict([('a', {}), ('b', {'a': 6, 'b': 3}), ('c', {'b': 3, 'd': 3}), ('d', {'c': 3, 'b': 3}), ('e', {'d': 2}), ('f', {'g': 3, 'd': 1, 'c': 3}), ('g', {'f': 3}), ('h', {'e': 2, 'f': 4})])
        # df = pd.DataFrame.from_dict(d).fillna(" ")
        # df.columns = [f"_{col}_" for col in df.columns]

        dataframe = dataframe.fillna(" ")
        self.textBrowser.setHtml(dataframe.to_html())

    def save_input_params(self):
        self.algorithm_type = 'alpha' if self.comboBox_alg.currentText()=="Alpha Miner" else "heuristic"
        self.param_value = self.doubleSpinBox_param.value()


    def update(self):
        self.save_input_params()
        print("Updating...")

        if self.algorithm_type == 'alpha':
            self.miner = AlphaMiner(self.log_fn)
        else:
            self.miner = HeuristicMiner(self.log_fn)

        self.miner.execute_algorithm()

        results_path = f"./../results/gui_{self.algorithm_type}"
        self.miner.save_to_png(results_path)

        self.display_image(results_path+'.png')
        self.update_output_df()


    def update_output_df(self):
        if self.miner:
            if self.algorithm_type == 'alpha':
                self.set_output(self.miner.get_relation_df())
            else:
                if self.comboBox_matrix.currentText() == "Relation Matrix":
                    self.set_output(self.miner.get_relation_frequency_matrix())
                else:
                    self.set_output(self.miner.get_2loop_frequency_matrix())



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
