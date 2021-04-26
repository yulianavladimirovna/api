import requests

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QComboBox

from application_service.get_map_uc import GetMapUseCase
from domain.map_params import MapParams


def search_for_coordinates(address):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={',+'.join(address.split(', '))},+1&format=json"
    response = requests.get(geocoder_request)
    json_response = response.json()

    pos = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]

    return map(float, pos.split())


def search_full_name(address):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={',+'.join(address.split(', '))},+1&format=json"
    response = requests.get(geocoder_request)
    json_response = response.json()

    name = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
        "GeocoderMetaData"]["text"]

    return name


class MainWindow(QWidget):
    def __init__(self, uc: GetMapUseCase, parent=None):
        super().__init__(parent)
        self.initUI()
        self.uc = uc
        self.map_params = MapParams()
        self.show_map()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        key = event.key()
        if key == Qt.Key_PageUp:
            self.map_params.up_zoom()
        elif key == Qt.Key_PageDown:
            self.map_params.down_zoom()
        elif key == Qt.Key_Up:
            self.map_params.up()
        elif key == Qt.Key_Down:
            self.map_params.down()
        elif key == Qt.Key_Left:
            self.map_params.left()
        elif key == Qt.Key_Right:
            self.map_params.right()

        self.show_map()

    def initUI(self):
        self.setGeometry(100, 100, 1000, 800)
        self.setWindowTitle('Maps API')

        self.map_label = QLabel(self)
        self.map_label.setGeometry(20, -20, 530, 530)

        layout = QVBoxLayout()
        layout.addWidget(self.map_label)
        self.setLayout(layout)

        self.type_box = QComboBox(self)
        self.type_box.addItems(['Схема', "Спутник", "Гибрид"])
        self.type_box.setGeometry(85, 10, 150, 30)

        self.type_label = QLabel(self)
        self.type_label.setText('Тип карты:')
        self.type_label.setGeometry(10, 10, 150, 30)

        self.res_button = QPushButton("Показать", self)
        self.res_button.setGeometry(10, 50, 150, 30)
        self.res_button.clicked.connect(self.click)

        self.btn1 = QPushButton("Искать", self)
        self.btn1.move(520, 640)
        self.btn1.resize(100, 30)
        self.btn1.clicked.connect(self.click)

        self.btn2 = QPushButton("Сброс поискового результата", self)
        self.btn2.move(10, 720)
        self.btn2.resize(200, 30)
        self.btn2.clicked.connect(self.click)

        self.line1 = QLineEdit('', self)
        self.line1.move(10, 640)
        self.line1.resize(500, 30)

        self.label_fullname = QLabel(self)
        self.label_fullname.setText('Полный адрес: ')
        self.label_fullname.setGeometry(10, 680, 1000, 30)

    def click(self):
        source = self.sender()

        if source.text() == 'Искать':
            address = self.line1.text()
            pos = list(search_for_coordinates(address))
            name = search_full_name(address)
            self.map_params.new_search(pos[0], pos[1])
            self.label_fullname.setText('Полный адрес: ' + name)

        elif source.text() == 'Сброс поискового результата':
            self.line1.setText('')
            name = search_full_name("Москва, МГУ")
            self.label_fullname.setText('Полный адрес: ' + name)

            self.map_params.new_pt('37.530887', '55.703118')
            self.map_params.new_search('37.530887', '55.703118')

        else:
            if self.type_box.currentIndex() == 0:
                self.map_params.new_l('map')
            if self.type_box.currentIndex() == 1:
                self.map_params.new_l('sat')
            if self.type_box.currentIndex() == 2:
                self.map_params.new_l('skl')

        self.show_map()
        self.map_label.setFocus()

    def show_map(self):
        map = self.uc.execute(self.map_params)

        pixmap = QPixmap()
        pixmap.loadFromData(map, "PNG")
        self.map_label.setPixmap(pixmap)
