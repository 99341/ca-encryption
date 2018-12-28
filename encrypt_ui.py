# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(457, 374)
        self.text_binary = QtWidgets.QLineEdit(Dialog)
        self.text_binary.setGeometry(QtCore.QRect(40, 160, 401, 21))
        self.text_binary.setText("")
        self.text_binary.setObjectName("text_binary")
        self.generate_key = QtWidgets.QPushButton(Dialog)
        self.generate_key.setGeometry(QtCore.QRect(270, 100, 151, 23))
        self.generate_key.setObjectName("generate_key")
        self.key_binary = QtWidgets.QLineEdit(Dialog)
        self.key_binary.setGeometry(QtCore.QRect(40, 210, 401, 21))
        self.key_binary.setText("")
        self.key_binary.setObjectName("key_binary")
        self.encrypted_message = QtWidgets.QLineEdit(Dialog)
        self.encrypted_message.setGeometry(QtCore.QRect(40, 260, 401, 21))
        self.encrypted_message.setText("")
        self.encrypted_message.setObjectName("encrypted_message")
        self.text_to_encrypt_box = QtWidgets.QLineEdit(Dialog)
        self.text_to_encrypt_box.setGeometry(QtCore.QRect(40, 50, 211, 21))
        self.text_to_encrypt_box.setText("")
        self.text_to_encrypt_box.setObjectName("text_to_encrypt_box")
        self.generated_key_box = QtWidgets.QLineEdit(Dialog)
        self.generated_key_box.setGeometry(QtCore.QRect(40, 100, 211, 21))
        self.generated_key_box.setText("")
        self.generated_key_box.setObjectName("generated_key_box")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 30, 211, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.encrypt_key = QtWidgets.QPushButton(Dialog)
        self.encrypt_key.setGeometry(QtCore.QRect(160, 310, 151, 23))
        self.encrypt_key.setObjectName("encrypt_key")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 80, 211, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(130, 140, 211, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(130, 190, 211, 20))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(130, 240, 211, 20))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.generate_key.setText(_translate("Dialog", "Generate Key"))
        self.label.setText(_translate("Dialog", "Insert text to encrypt"))
        self.encrypt_key.setText(_translate("Dialog", "Encrypt"))
        self.label_2.setText(_translate("Dialog", "Generated key"))
        self.label_3.setText(_translate("Dialog", "Binary text"))
        self.label_4.setText(_translate("Dialog", "Binary key"))
        self.label_5.setText(_translate("Dialog", "Binary encrypted text"))

