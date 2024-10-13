import sys
import estimateALAAMSA
import os
import pandas as pd 
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,QMessageBox,
    QTextEdit, QFileDialog, QTableWidget, QTableWidgetItem, QCheckBox, 
    QHBoxLayout, QDialogButtonBox, QDialog, QLabel
)
from changeStatisticsALAAM import *
from changeStatisticsALAAMbipartite import *
from changeStatisticsALAAMdirected import *
from basicALAAMsampler import basicALAAMsampler
from functools import partial

class Ui_Form(QWidget):
    networkSignal = pyqtSignal(object)
    binarySignal = pyqtSignal(object)
    continousSignal = pyqtSignal(object)
    categoricalSignal = pyqtSignal(object)
    dyadicSignal = pyqtSignal(object)
    # Dictionary for directed network functions and their names
    directed_stat_funcs = {
        "Sender": changeSender,
        "Receiver": changeReceiver,
        "Reciprocity": changeReciprocity,
        "EgoInTwoStar": changeEgoInTwoStar,
        "EgoOutTwoStar": changeEgoOutTwoStar,
        "MixedTwoStar": changeMixedTwoStar,
        "MixedTwoStarSource": changeMixedTwoStarSource,
        "MixedTwoStarSink": changeMixedTwoStarSink,
        "Contagion": changeContagion,
        "ContagionReciprocity": changeContagionReciprocity,
        "TransitiveTriangleT1": changeTransitiveTriangleT1,
        "TransitiveTriangleT3": changeTransitiveTriangleT3,
        "TransitiveTriangleD1": changeTransitiveTriangleD1,
        "TransitiveTriangleU1": changeTransitiveTriangleU1,
        "CyclicTriangleC1": changeCyclicTriangleC1,
        "CyclicTriangleC3": changeCyclicTriangleC3,
        "AlterInTwoStar2": changeAlterInTwoStar2,
        "AlterOutTwoStar2": changeAlterOutTwoStar2
    }

    # Dictionary for undirected network functions and their names
    undirected_stat_funcs = {
        "TwoStar": changeTwoStar,
        "ThreeStar": changeThreeStar,
        "PartnerActivityTwoPath": changePartnerActivityTwoPath,
        "TriangleT1": changeTriangleT1,
        "Contagion": changeStatisticsALAAM.changeContagion,  # Change this based on your function
        "IndirectPartnerAttribute": changeIndirectPartnerAttribute,
        "PartnerAttributeActivity": changePartnerAttributeActivity,
        "PartnerPartnerAttribute": changePartnerPartnerAttribute,
        "TriangleT2": changeTriangleT2,
        "TriangleT3": changeTriangleT3
    }
    parameters_list = []
    binary_parameters_list = []
    continous_parameters_list = []
    categorical_parameters_list = []
    dyadic_parameters_list = []

    def __init__(self):
        super(Ui_Form, self).__init__()
        self.setupUi(self)
        # Store headers
        self.headers = []
    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(626, 379)
        self.groupBox = QtWidgets.QGroupBox(parent=Form)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 401, 51))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(parent=self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 20, 81, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(100, 20, 200, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(parent=self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(310, 20, 75, 24))
        self.pushButton.setObjectName("pushButton")

        ##select attribute File
        self.pushButton.clicked.connect(self.selectAttributeFile)

        self.groupBox_2 = QtWidgets.QGroupBox(parent=Form)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 70, 401, 101))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 81, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 20, 200, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 20, 75, 24))
        self.pushButton_2.setObjectName("pushButton_2")

        ##select network File
        self.pushButton_2.clicked.connect(self.selectNetworkFile)

        self.radioButton = QtWidgets.QRadioButton(parent=self.groupBox_2)
        self.radioButton.setGeometry(QtCore.QRect(20, 50, 95, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(parent=self.groupBox_2)
        self.radioButton_2.setGeometry(QtCore.QRect(110, 50, 95, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.pushButton_3.setGeometry(QtCore.QRect(220, 50, 121, 24))
        self.pushButton_3.setObjectName("pushButton_3")

        ##select parameter
        self.pushButton_3.clicked.connect(self.openNetworkWindow)


        self.groupBox_3 = QtWidgets.QGroupBox(parent=Form)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 180, 591, 151))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 121, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.lineEdit_3.setGeometry(QtCore.QRect(160, 20, 200, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_4.setGeometry(QtCore.QRect(370, 20, 75, 24))
        self.pushButton_4.setObjectName("pushButton_4")

        ##select Binary File
        self.pushButton_4.clicked.connect(self.selectBinaryFile)

        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 50, 200, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_5.setGeometry(QtCore.QRect(370, 50, 75, 24))
        self.pushButton_5.setObjectName("pushButton_5")

        ##select continous File
        self.pushButton_5.clicked.connect(self.selectContinousFile)

        self.label_4 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(10, 50, 151, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.lineEdit_5.setGeometry(QtCore.QRect(160, 80, 200, 20))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton_6 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_6.setGeometry(QtCore.QRect(370, 80, 75, 24))
        self.pushButton_6.setObjectName("pushButton_6")

        ##select categorical File
        self.pushButton_6.clicked.connect(self.selectCategoricalFile)

        self.label_5 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(10, 80, 151, 16))
        self.label_5.setObjectName("label_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.lineEdit_6.setGeometry(QtCore.QRect(160, 110, 200, 20))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.pushButton_7 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_7.setGeometry(QtCore.QRect(370, 110, 75, 24))
        self.pushButton_7.setObjectName("pushButton_7")

        ##select Dyadic File
        self.pushButton_7.clicked.connect(self.selectDyadicFile)

        self.label_6 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_6.setGeometry(QtCore.QRect(10, 110, 131, 16))
        self.label_6.setObjectName("label_6")
        self.pushButton_9 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_9.setGeometry(QtCore.QRect(450, 20, 121, 24))
        self.pushButton_9.setObjectName("pushButton_9")

        ##select Binary parameter
        self.pushButton_9.clicked.connect(self.selectBinaryParameter)

        self.pushButton_10 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_10.setGeometry(QtCore.QRect(450, 50, 121, 24))
        self.pushButton_10.setObjectName("pushButton_10")

        ##select Continous parameter
        self.pushButton_10.clicked.connect(self.selectContinousParameter)

        self.pushButton_11 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_11.setGeometry(QtCore.QRect(450, 80, 121, 24))
        self.pushButton_11.setObjectName("pushButton_11")

        ##select categorical parameter
        self.pushButton_11.clicked.connect(self.selectCategoricalParameter)

        self.pushButton_12 = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.pushButton_12.setGeometry(QtCore.QRect(450, 110, 121, 24))
        self.pushButton_12.setObjectName("pushButton_12")

        ##select dyadic parameter
        self.pushButton_12.clicked.connect(self.selectDyadicParameter)
        
        self.groupBox_4 = QtWidgets.QGroupBox(parent=Form)
        self.groupBox_4.setGeometry(QtCore.QRect(450, 10, 161, 161))
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_7 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_7.setGeometry(QtCore.QRect(10, 30, 54, 16))
        self.label_7.setObjectName("label_7")
        self.spinBox = QtWidgets.QSpinBox(parent=self.groupBox_4)
        self.spinBox.setGeometry(QtCore.QRect(70, 30, 71, 21))
        self.spinBox.setMaximum(1000000)
        self.spinBox.setProperty("value", 100)
        self.spinBox.setObjectName("spinBox")
        self.label_8 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_8.setGeometry(QtCore.QRect(10, 70, 61, 16))
        self.label_8.setObjectName("label_8")
        self.spinBox_2 = QtWidgets.QSpinBox(parent=self.groupBox_4)
        self.spinBox_2.setGeometry(QtCore.QRect(70, 70, 71, 21))
        self.spinBox_2.setMaximum(10000000)
        self.spinBox_2.setProperty("value", 100)
        self.spinBox_2.setObjectName("spinBox_2")
        self.label_9 = QtWidgets.QLabel(parent=self.groupBox_4)
        self.label_9.setGeometry(QtCore.QRect(10, 100, 54, 16))
        self.label_9.setObjectName("label_9")
        self.spinBox_3 = QtWidgets.QSpinBox(parent=self.groupBox_4)
        self.spinBox_3.setGeometry(QtCore.QRect(70, 100, 71, 21))
        self.spinBox_3.setMaximum(1000000)
        self.spinBox_3.setProperty("value", 100)
        self.spinBox_3.setObjectName("spinBox_3")
        self.pushButton_8 = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.pushButton_8.setGeometry(QtCore.QRect(20, 130, 121, 24))
        self.pushButton_8.setObjectName("pushButton_8")

        ##analysis
        self.pushButton_8.clicked.connect(self.analysis)

        self.progressBar = QtWidgets.QProgressBar(parent=Form)
        self.progressBar.setGeometry(QtCore.QRect(20, 340, 118, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Attribute"))
        self.label.setText(_translate("Form", "Attribute file: "))
        self.pushButton.setText(_translate("Form", "Browse.."))
        self.groupBox_2.setTitle(_translate("Form", "Network"))
        self.label_2.setText(_translate("Form", "Network file: "))
        self.pushButton_2.setText(_translate("Form", "Browse.."))
        self.radioButton.setText(_translate("Form", "Directed"))
        self.radioButton_2.setText(_translate("Form", "Undirected"))

        self.radioButton.setChecked(True)

        self.pushButton_3.setText(_translate("Form", "Select Prameters"))
        self.groupBox_3.setTitle(_translate("Form", "Attribute/Dyadic covariates"))
        self.label_3.setText(_translate("Form", "Binary Atrribute file: "))
        self.pushButton_4.setText(_translate("Form", "Browse.."))
        self.pushButton_5.setText(_translate("Form", "Browse.."))
        self.label_4.setText(_translate("Form", "Continous Atrribute file: "))
        self.pushButton_6.setText(_translate("Form", "Browse.."))
        self.label_5.setText(_translate("Form", "Categorical Atrribute file: "))
        self.pushButton_7.setText(_translate("Form", "Browse.."))
        self.label_6.setText(_translate("Form", "Dyadic Atrribute file: "))
        self.pushButton_9.setText(_translate("Form", "Select Prameters"))
        self.pushButton_10.setText(_translate("Form", "Select Prameters"))
        self.pushButton_11.setText(_translate("Form", "Select Prameters"))
        self.pushButton_12.setText(_translate("Form", "Select Prameters"))
        self.groupBox_4.setTitle(_translate("Form", "Analysis"))
        self.label_7.setText(_translate("Form", "Burn-in:"))
        self.label_8.setText(_translate("Form", "Iterations:"))
        self.label_9.setText(_translate("Form", "Samples:"))
        self.pushButton_8.setText(_translate("Form", "Analysis"))

#########################functions#########################################################
    def selectAttributeFile(self):
        attributeFile = QFileDialog.getOpenFileName(self, 'Open file','','txt files (*.txt)')
        self.lineEdit.setText(attributeFile[0])

    def selectNetworkFile(self):
        networkFile = QFileDialog.getOpenFileName(self, 'Open file','','txt files (*.txt)')
        self.lineEdit_2.setText(networkFile[0])
    
    def selectBinaryFile(self):
        binaryFile = QFileDialog.getOpenFileName(self, 'Open file','','txt files (*.txt)')
        self.lineEdit_3.setText(binaryFile[0])

    def selectBinaryParameter(self):
        file_path = self.lineEdit_3.text()  # Get the file path from the lineEdit

        if not os.path.exists(file_path):
            # Show an error message if the file does not exist
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error: The file path is incorrect.")
            msg.setInformativeText(f"The file '{file_path}' does not exist. Please check the path and try again.")
            msg.setWindowTitle("File Error")
            msg.exec_()
            return

        try:
            # Load the file with correct delimiter (adjust if it's not tab-separated)
            df = pd.read_csv(file_path, delimiter='\s+')  # Use '\s+' if space-separated
            # Extract the headers from the DataFrame
            headers = df.columns.tolist()  # Get list of headers
            print("Headers:", headers)  # Debugging print to see the headers
            self.binaryWindow = binaryWindow()
            self.binarySignal.connect(self.binaryWindow.createCheckboxes)

            self.binarySignal.emit(headers)
            self.binaryWindow.binarySignal.connect(self.handleBinaryParameters)
            self.binaryWindow.show()
        except Exception as e:
            QMessageBox.warning(self, "File Error", f"An error occurred while reading the file: {str(e)}")
      
    def handleBinaryParameters(self, selected):
        self.binary_parameters_list = selected
        print("Selected Binary parameters:", selected)
    
    def selectContinousFile(self):
        continousFile = QFileDialog.getOpenFileName(self, 'Open file','','txt files (*.txt)')
        self.lineEdit_4.setText(continousFile[0])

    def selectContinousParameter(self):
        file_path = self.lineEdit_4.text()  # Get the file path from the lineEdit

        if not os.path.exists(file_path):
            # Show an error message if the file does not exist
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error: The file path is incorrect.")
            msg.setInformativeText(f"The file '{file_path}' does not exist. Please check the path and try again.")
            msg.setWindowTitle("File Error")
            msg.exec_()
            return

        try:
            # Load the file with correct delimiter (adjust if it's not tab-separated)
            df = pd.read_csv(file_path, delimiter='\s+')  # Use '\s+' if space-separated
            # Extract the headers from the DataFrame
            headers = df.columns.tolist()  # Get list of headers
            print("Headers:", headers)  # Debugging print to see the headers
            self.continousWindow = continousWindow()
            self.continousSignal.connect(self.continousWindow.createCheckboxes)

            self.continousSignal.emit(headers)
            self.continousWindow.continousSignal.connect(self.handleContinousParameters)
            self.continousWindow.show()
        except Exception as e:
            QMessageBox.warning(self, "File Error", f"An error occurred while reading the file: {str(e)}")
      
    def handleContinousParameters(self, selected):
        self.continous_parameters_list = selected
        print("Selected continous parameters:", selected)

    def selectCategoricalFile(self):
        categoricalFile = QFileDialog.getOpenFileName(self, 'Open file','','txt files (*.txt)')
        self.lineEdit_5.setText(categoricalFile[0])    

    def selectCategoricalParameter(self):
        file_path = self.lineEdit_5.text()  # Get the file path from the lineEdit

        if not os.path.exists(file_path):
            # Show an error message if the file does not exist
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error: The file path is incorrect.")
            msg.setInformativeText(f"The file '{file_path}' does not exist. Please check the path and try again.")
            msg.setWindowTitle("File Error")
            msg.exec_()
            return

        try:
            # Load the file with correct delimiter (adjust if it's not tab-separated)
            df = pd.read_csv(file_path, delimiter='\s+')  # Use '\s+' if space-separated
            # Extract the headers from the DataFrame
            headers = df.columns.tolist()  # Get list of headers
            print("Headers:", headers)  # Debugging print to see the headers
            self.categoricalWindow = categoricalWindow()
            self.categoricalSignal.connect(self.categoricalWindow.createCheckboxes)

            self.categoricalSignal.emit(headers)
            self.categoricalWindow.categoricalSignal.connect(self.handleCategoricalParameters)
            self.categoricalWindow.show()
        except Exception as e:
            QMessageBox.warning(self, "File Error", f"An error occurred while reading the file: {str(e)}")
      
    def handleCategoricalParameters(self, selected):
        self.categorical_parameters_list = selected
        print("Selected Categorical parameters:", selected)

    def selectDyadicFile(self):
        dyadicFile = QFileDialog.getOpenFileName(self, 'Open file','','txt files (*.txt)')
        self.lineEdit_6.setText(dyadicFile[0])

    def selectDyadicParameter(self):
        file_path = self.lineEdit_6.text()  # Get the file path from the lineEdit

        if not os.path.exists(file_path):
            # Show an error message if the file does not exist
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error: The file path is incorrect.")
            msg.setInformativeText(f"The file '{file_path}' does not exist. Please check the path and try again.")
            msg.setWindowTitle("File Error")
            msg.exec_()
            return

        try:
            # Load the file with correct delimiter (adjust if it's not tab-separated)
            df = pd.read_csv(file_path, delimiter='\s+')  # Use '\s+' if space-separated
            # Extract the headers from the DataFrame
            headers = df.columns.tolist()  # Get list of headers
            print("Headers:", headers)  # Debugging print to see the headers
            self.dyadicWindow = dyadicWindow()
            self.dyadicSignal.connect(self.dyadicWindow.createCheckboxes)

            self.dyadicSignal.emit(headers)
            self.dyadicWindow.dyadicSignal.connect(self.handleDyadicParameters)
            self.dyadicWindow.show()
        except Exception as e:
            QMessageBox.warning(self, "File Error", f"An error occurred while reading the file: {str(e)}")
      
    def handleDyadicParameters(self, selected):
        self.dyadic_parameters_list = selected
        print("Selected Dyadic parameters:", selected)


    def openNetworkWindow(self):
        self.networkWindow = networkWindow()
        self.networkSignal.connect(self.networkWindow.createCheckboxes)
        mode = "0"
        if self.radioButton.isChecked():
            mode = "0"
        elif self.radioButton_2.isChecked():
            mode = "1"
        print(f"Selected mode: {mode}")  # Debug: Print the mode value
        self.networkSignal.emit(mode)
        self.networkWindow.selectedSignal.connect(self.handleSelectedParameters)
        self.networkWindow.show()

    def handleSelectedParameters(self, selected):
        # Handle the result from the networkWindow (selected checkboxes)
        self.parameters_list = selected
        print("Selected parameters:", selected)


    def analysis(self):
        attributeFilepath = self.lineEdit.text() 
        networkFilepath = self.lineEdit_2.text()
        binaryFilepath = self.lineEdit_3.text()
        continousFilepath = self.lineEdit_4.text()
        categoricalFilepath = self.lineEdit_5.text()
        dyadicFilepath = self.lineEdit_6.text()
        burnIn = self.spinBox.value()
        iterations = self.spinBox_2.value()
        samples = self.spinBox_3.value()
        self.progressBar.setRange(0, 0)

        # Check if the filepaths are empty strings, and assign None if they are
        binaryFilepath = None if binaryFilepath == "" else binaryFilepath
        continousFilepath = None if continousFilepath == "" else continousFilepath
        categoricalFilepath = None if categoricalFilepath == "" else categoricalFilepath
        dyadicFilepath = None if dyadicFilepath == "" else dyadicFilepath
        # Check whether the network is directed or undirected (for example, using a checkbox)
        is_directed = self.radioButton.isChecked()

        # Prepare lists for functions and corresponding names
        selected_funcs = []
        selected_names = []

        # Choose the correct dictionary based on the network type
        if is_directed:
            func_dict = self.directed_stat_funcs
        else:
            func_dict = self.undirected_stat_funcs
        
        # Iterate through selected parameters to map them to functions
        for param in self.parameters_list:
            if param in func_dict:
                selected_funcs.append(func_dict[param])  # Add the corresponding function
                selected_names.append(param)  # Add the corresponding name
        
        #for param in self.binary_parameters_list:
        if len(self.binary_parameters_list) != 0:
            for param in self.binary_parameters_list:
                # Remove the "_oOA" suffix from the parameter name
                clean_param = param.replace("_oOA", "")
                selected_funcs.append(partial(changeoOb, clean_param))  # Add the corresponding function
                selected_names.append(param)  # Add the corresponding name

        #for param in self.continous_parameters_list:
        if len(self.continous_parameters_list) != 0:
            for param in self.continous_parameters_list:
                # Remove the "_oOA" suffix from the parameter name
                clean_param = param.replace("_oOA", "")
                selected_funcs.append(partial(changeoOc, clean_param))  # Add the corresponding function
                selected_names.append(param)  # Add the corresponding name

        #for param in self.categorical_parameters_list:
        if len(self.categorical_parameters_list) != 0:
            for param in self.categorical_parameters_list:
                # Remove the "_oOA" suffix from the parameter name
                clean_param = param.replace("_oOA", "")
                selected_funcs.append(partial(changeoO_OsameContagion, clean_param))  # Add the corresponding function
                selected_names.append(param)  # Add the corresponding name

        #for param in self.dyadic_parameters_list:
        if len(self.dyadic_parameters_list) != 0:
            for param in self.dyadic_parameters_list:
                # Remove the "_oOA" suffix from the parameter name
                clean_param = param.replace("_oOA", "")
                selected_funcs.append(partial(changeoOb, clean_param))  # Add the corresponding function
                selected_names.append(param)  # Add the corresponding name
        
        print ("selected_funcs: "+ str(selected_funcs))
        print ("selected_names: "+ str(selected_names))

        results = estimateALAAMSA.run_on_network_attr(
            networkFilepath,  # Network data file path
            selected_funcs,  # List of selected functions
            selected_names,  # List of selected names
            attributeFilepath,  # Sample file path
            binaryFilepath,  # Binary attribute file path
            continousFilepath,  # Continuous attribute file path
            categoricalFilepath, # categorical attribute file path
            basicALAAMsampler,
            None,
            is_directed,
            False,
            iterations,
            burnIn,
            None,
            None,
            "testoutput1.html",
            "testoutput2.html"
        )
        print(results) 


################sub window#################################
class networkWindow(QWidget):
    selectedSignal = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select Parameters")
        self.setFixedWidth(300)  # Set a wider width
        self.layout = QVBoxLayout(self)

        # Set some padding around the window
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # OK button to confirm selection
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.sendSelection)

        # Add the OK button to the layout
        self.layout.addStretch()
        self.layout.addWidget(self.ok_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)
        self.checkboxes = []  # To store checkboxes

        # Optionally set a maximum height
        self.setMaximumHeight(400)

    def createCheckboxes(self, mode):
        # Clear any existing checkboxes by removing them from the layout
        for checkbox in self.checkboxes:
            self.layout.removeWidget(checkbox)  # Remove from layout
            checkbox.deleteLater()  # Delete the checkbox
        self.checkboxes.clear()

        # Create checkboxes based on the mode
        print(f"Mode received in createCheckboxes: {mode}") 
        if mode == "0":
            options = [
                "Sender","Receiver","EgoInTwoStar","EgoOutTwoStar","MixedTwoStar","MixedTwoStarSource","MixedTwoStarSink","Contagion","ContagionReciprocity","TransitiveTriangleT1","TransitiveTriangleT3","TransitiveTriangleD1","TransitiveTriangleU1","CyclicTriangleC1","CyclicTriangleC3","AlterInTwoStar2","AlterOutTwoStar2"
            ]
        else:
            options = [
                "TwoStar","ThreeStar","PartnerActivityTwoPath","TriangleT1","Contagion","IndirectPartnerAttribute","PartnerAttributeActivity","PartnerPartnerAttribute","TriangleT2","TriangleT3"
            ]

        # Create and add new checkboxes based on the selected mode
        for option in options:
            checkbox = QCheckBox(option, self)
            checkbox.setStyleSheet("margin: 5px;")  # Add some margin to checkboxes
            self.layout.insertWidget(self.layout.count() - 1, checkbox)  # Insert before the OK button
            self.checkboxes.append(checkbox)

    def sendSelection(self):
        # Get selected checkboxes
        selected = [cb.text() for cb in self.checkboxes if cb.isChecked()]

        # Emit the selected checkboxes back to the main window
        self.selectedSignal.emit(selected)

        # Close the window after selection
        self.close()

################end sub window#######################################
################binary window########################################
class binaryWindow(QWidget):
    # Signal to send selected checkboxes back to the main window
    binarySignal = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select Binary Parameters")
        self.setFixedWidth(300)  # Set a wider width
        self.layout = QVBoxLayout(self)

        # Set padding and spacing around the window
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # OK button to confirm selection
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.sendSelection)

        # Add the OK button to the layout
        self.layout.addStretch()
        self.layout.addWidget(self.ok_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)
        self.checkboxes = []  # To store checkboxes

        # Optionally set a maximum height
        self.setMaximumHeight(400)

    def createCheckboxes(self, headers):
        # Clear any existing checkboxes by removing them from the layout
        for checkbox in self.checkboxes:
            self.layout.removeWidget(checkbox)  # Remove from layout
            checkbox.deleteLater()  # Delete the checkbox
        self.checkboxes.clear()

        # Create checkboxes based on headers passed in
        for header in headers:
            print (header+"##")
            header = header.strip()  # Remove extra spaces, line breaks, etc.
            checkbox_label = f"{header}_oOA"  # Format the label correctly
            checkbox = QCheckBox(checkbox_label, self)
            checkbox.setStyleSheet("margin: 5px;")  # Add some margin to checkboxes
            self.layout.insertWidget(self.layout.count() - 1, checkbox)  # Insert before the OK button
            self.checkboxes.append(checkbox)

    def sendSelection(self):
        # Get selected checkboxes
        selected = [cb.text() for cb in self.checkboxes if cb.isChecked()]

        # Emit the selected checkboxes back to the main window
        self.binarySignal.emit(selected)

        # Close the window after selection
        self.close()

################end binary window###################################
################continous window########################################
class continousWindow(QWidget):
    # Signal to send selected checkboxes back to the main window
    continousSignal = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select Continous Parameters")
        self.setFixedWidth(300)  # Set a wider width
        self.layout = QVBoxLayout(self)

        # Set padding and spacing around the window
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # OK button to confirm selection
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.sendSelection)

        # Add the OK button to the layout
        self.layout.addStretch()
        self.layout.addWidget(self.ok_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)
        self.checkboxes = []  # To store checkboxes

        # Optionally set a maximum height
        self.setMaximumHeight(400)

    def createCheckboxes(self, headers):
        # Clear any existing checkboxes by removing them from the layout
        for checkbox in self.checkboxes:
            self.layout.removeWidget(checkbox)  # Remove from layout
            checkbox.deleteLater()  # Delete the checkbox
        self.checkboxes.clear()

        # Create checkboxes based on headers passed in
        for header in headers:
            print (header+"##")
            header = header.strip()  # Remove extra spaces, line breaks, etc.
            checkbox_label = f"{header}_oOA"  # Format the label correctly
            checkbox = QCheckBox(checkbox_label, self)
            checkbox.setStyleSheet("margin: 5px;")  # Add some margin to checkboxes
            self.layout.insertWidget(self.layout.count() - 1, checkbox)  # Insert before the OK button
            self.checkboxes.append(checkbox)

    def sendSelection(self):
        # Get selected checkboxes
        selected = [cb.text() for cb in self.checkboxes if cb.isChecked()]

        # Emit the selected checkboxes back to the main window
        self.continousSignal.emit(selected)

        # Close the window after selection
        self.close()

################end continous window###################################
################categorical window########################################
class categoricalWindow(QWidget):
    # Signal to send selected checkboxes back to the main window
    categoricalSignal = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select Categorical Parameters")
        self.setFixedWidth(300)  # Set a wider width
        self.layout = QVBoxLayout(self)

        # Set padding and spacing around the window
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # OK button to confirm selection
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.sendSelection)

        # Add the OK button to the layout
        self.layout.addStretch()
        self.layout.addWidget(self.ok_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)
        self.checkboxes = []  # To store checkboxes

        # Optionally set a maximum height
        self.setMaximumHeight(400)

    def createCheckboxes(self, headers):
        # Clear any existing checkboxes by removing them from the layout
        for checkbox in self.checkboxes:
            self.layout.removeWidget(checkbox)  # Remove from layout
            checkbox.deleteLater()  # Delete the checkbox
        self.checkboxes.clear()

        # Create checkboxes based on headers passed in
        for header in headers:
            print (header+"##")
            header = header.strip()  # Remove extra spaces, line breaks, etc.
            checkbox_label = f"{header}_oOA"  # Format the label correctly
            checkbox = QCheckBox(checkbox_label, self)
            checkbox.setStyleSheet("margin: 5px;")  # Add some margin to checkboxes
            self.layout.insertWidget(self.layout.count() - 1, checkbox)  # Insert before the OK button
            self.checkboxes.append(checkbox)

    def sendSelection(self):
        # Get selected checkboxes
        selected = [cb.text() for cb in self.checkboxes if cb.isChecked()]

        # Emit the selected checkboxes back to the main window
        self.categoricalSignal.emit(selected)

        # Close the window after selection
        self.close()

################end categorical window###################################
################dyadic window########################################
class dyadicWindow(QWidget):
    # Signal to send selected checkboxes back to the main window
    dyadicSignal = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select Dyadic Parameters")
        self.setFixedWidth(300)  # Set a wider width
        self.layout = QVBoxLayout(self)

        # Set padding and spacing around the window
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # OK button to confirm selection
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.sendSelection)

        # Add the OK button to the layout
        self.layout.addStretch()
        self.layout.addWidget(self.ok_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)
        self.checkboxes = []  # To store checkboxes

        # Optionally set a maximum height
        self.setMaximumHeight(400)

    def createCheckboxes(self, headers):
        # Clear any existing checkboxes by removing them from the layout
        for checkbox in self.checkboxes:
            self.layout.removeWidget(checkbox)  # Remove from layout
            checkbox.deleteLater()  # Delete the checkbox
        self.checkboxes.clear()

        # Create checkboxes based on headers passed in
        for header in headers:
            print (header+"##")
            header = header.strip()  # Remove extra spaces, line breaks, etc.
            checkbox_label = f"{header}_oOA"  # Format the label correctly
            checkbox = QCheckBox(checkbox_label, self)
            checkbox.setStyleSheet("margin: 5px;")  # Add some margin to checkboxes
            self.layout.insertWidget(self.layout.count() - 1, checkbox)  # Insert before the OK button
            self.checkboxes.append(checkbox)

    def sendSelection(self):
        # Get selected checkboxes
        selected = [cb.text() for cb in self.checkboxes if cb.isChecked()]

        # Emit the selected checkboxes back to the main window
        self.dyadicSignal.emit(selected)

        # Close the window after selection
        self.close()

################end dyadic window###################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = Ui_Form()
    mainWin.show()
    sys.exit(app.exec())