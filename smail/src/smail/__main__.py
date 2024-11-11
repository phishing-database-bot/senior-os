import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QApplication, QMainWindow


from smail.layout import first_frame


import sconf.configuration.configuration_writer as dataWriter
import sconf.configuration.configuration_provider as dataProvider

def main():
    current_dir = os.getcwd()
    CONFIG_FILE_NAME = 'config.json'
    config_folder = os.path.join(current_dir, '../sconf')


    _dataProvider = dataProvider.ConfigurationProvider(configFileName=CONFIG_FILE_NAME, configStoragePath=config_folder)

    try:

        app = QApplication([])
        window = QMainWindow()
        # window.showFullScreen()
        window.setGeometry(100, 100, 1280, 420)
        window.setWindowFlags(Qt.FramelessWindowHint)
        layout = first_frame(window, _dataProvider)
        window.setCentralWidget(layout)
        window.show()
        app.exec()

    except Exception as e:
        print(f"Could not start SMAIL app, error loading configuration. {e}" )

if __name__ == '__main__':
    main()
