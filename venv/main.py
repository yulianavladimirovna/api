from PyQt5.QtWidgets import QApplication

from application_service.get_map_uc import GetMapUseCase
from services.yandex_map_adapter import YandexMapAdapter
from ui.main_window import MainWindow

adapter = YandexMapAdapter()
use_case = GetMapUseCase(adapter)

app = QApplication([])

win = MainWindow(use_case)
win.show()
app.exec()

# Москва, Красная площадь
