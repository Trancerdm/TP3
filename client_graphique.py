from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
)
from PyQt5.Qt import QUrl, QDesktopServices
import requests
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Client")
        self.setFixedSize(400, 500)
        self.label1 = QLabel(" Enter your host name:", self)
        self.text = QLineEdit(self)
        self.text.move(10, 30)
        self.label2 = QLabel("Answer:", self)
        self.label2.move(10, 65)

        self.label3 = QLabel("Enter your api key:", self)
        self.label3.move(10, 100)
        self.text2 = QLineEdit(self)
        self.text2.move(10, 130)
        self.label4 = QLabel("Answer:", self)
        self.label4.move(10, 160)

        self.label5 = QLabel("Enter your IP:", self)
        self.label5.move(10, 205)
        self.text3 = QLineEdit(self)
        self.text3.move(10, 235)
        self.label6 = QLabel("Answer:", self)
        self.label6.move(10, 265)
        self.button = QPushButton("Send", self)
        self.button.move(10, 295)

        self.button.clicked.connect(self.on_click)
        self.button.pressed.connect(self.on_click)

        self.show()

    def create_url(self,res):
        openstreetmap_url = "https://www.openstreetmap.org/?mlat=%s&mlon=%s#map=12"%(res["latitude"], res["longitude"])
        return openstreetmap_url

    def on_click(self):
        #Hostname
        hostname = self.text.text()
        ip = self.text3.text()
        api = self.text2.text()

        if hostname == "" or ip == "" or api == "":
            QMessageBox.about(self, "Error", "Please fill the field")
        else:
            res = self.__query(hostname, ip, api)
            if res:
                self.label2.setText("hostname fonctionne")
                self.label4.setText("api fonctionne")
                self.label6.setText("ip fonctionne")
                self.label2.adjustSize()
                self.label4.adjustSize()
                self.label6.adjustSize()
                self.show()

                print(res)
                openstreetmap_url = "https://www.openstreetmap.org/?mlat="+str(res["latitude"])+"&mlon="+str(res["longitude"])+"#map=12"
             
                QDesktopServices.openUrl(QUrl(openstreetmap_url))
                pass
                
    #Hostname
    def __query(self, hostname, ip, api):
        url = "http://%s/ip/%s/?key=%s" % (hostname, ip, api)
        r = requests.get(url)
        if r.status_code == requests.codes.NOT_FOUND:
            QMessageBox.about(self, "Error", "Name not found")
        if r.status_code == requests.codes.OK:
            return r.json()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()