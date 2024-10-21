from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget

from shelp.src.ui.view.GlobalSettingsView import GlobalSettingsView
from shelp.src.ui.view.SmailSettingsView import MailSettingsView
from shelp.src.ui.view.SwebSettingsView import WebSettingsView


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set main window properties
        self.setWindowTitle("Main Window")
        self.setFixedSize(1260, 580)
        self.setStyleSheet("""
                    QMainWindow {
                        background-color: #FFFFFF;
                        border: 3px solid #000000;
                        border-radius: 3px;
                    }
                    QPushButton {
                        text-align:center;
                        font-family: Inter;
                        font-size: 40px;
                        color: #000000;
                        padding: 5px;
                        background-color: #949494;
                        border: 1px solid #797979;
                        border-radius: 3px;
                        color: #FFFFFF;
                        margin-left: 10px;
                        margin-top: 10px;
                        margin-right: 10px;
                        margin-bottom: 12px;
                    }
                    QPushButton:hover {
                        background-color: #48843F;
                    }
                    QPushButton:open {
                        background-color: #48843F;
                    }
                """)
        self.setFont(QFont('Inter', 20))
        # Main layout
        self.main_layout = QVBoxLayout(self)

        # Menu layout
        self.menu_layout = QHBoxLayout()

        # Creating the menu buttons
        self.menu_buttons = {
            "Menu": QPushButton("Menu"),
            "x": QPushButton("X"),
            "Global": QPushButton("Global"),
            "Web": QPushButton("Web"),
            "Mail": QPushButton("Mail")
        }

        for button in self.menu_buttons.values():
            button.setFixedSize(244, 107)
            self.menu_layout.addWidget(button)

        self.main_layout.addLayout(self.menu_layout)

        # Stack for holding multiple views (screens)
        self.stacked_widget = QStackedWidget()

        # Creating views for different sections
        self.global_view = GlobalSettingsView()
        self.web_view = WebSettingsView()
        self.mail_view = MailSettingsView()

        # Adding views to the stacked widget
        self.stacked_widget.addWidget(self.global_view)  # Index 0
        self.stacked_widget.addWidget(self.web_view)     # Index 1
        self.stacked_widget.addWidget(self.mail_view)    # Index 2

        # Adding the stacked widget to the main layout
        self.main_layout.addWidget(self.stacked_widget)

        # Connecting menu buttons to their respective actions
        self.menu_buttons["Global"].clicked.connect(self.show_global_view)
        self.menu_buttons["Web"].clicked.connect(self.show_web_view)
        self.menu_buttons["Mail"].clicked.connect(self.show_mail_view)

        self.setLayout(self.main_layout)

    def get_button_style(self, active):
        # Define styles for normal and phishing states
        base_style = """
                QPushButton {
                    background-color: #949494;
                    border: 1px solid #797979;
                    border-radius: 3px;
                    color: #FFFFFF;
                    margin-left: 10px;
                    margin-top: 10px;
                    margin-right: 10px;
                    margin-bottom: 12px;
                }
                QPushButton:hover {
                    background-color: #48843F;
                }
            """

        if active:
            return base_style + """
                QPushButton {
                    background-color: #48843F
                }
            """

        return base_style

    # Slot to switch to Global view
    def show_global_view(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_web_view(self):
        self.stacked_widget.setCurrentIndex(1)

    # Slot to switch to Mail view
    def show_mail_view(self):
        self.stacked_widget.setCurrentIndex(2)

