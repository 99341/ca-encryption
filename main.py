import sys
from PyQt5.QtWidgets import *
import encrypting as ec


app = QApplication(sys.argv)
window = ec.SecretKey()
window.setWindowTitle('Secret key encrypting')
window.show()
sys.exit(app.exec_())

