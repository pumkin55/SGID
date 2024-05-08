"""
application for labour assistance management
"""

try:
    from importlib import metadata as importlib_metadata
except ImportError:
    # Backwards compatibility - importlib.metadata was added in Python 3.8
    import importlib_metadata

import os
import pickle
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QActionGroup
from PySide6.QtWidgets import (QMainWindow, QStackedWidget, QToolBar,
                               QApplication, QLabel, QVBoxLayout, QWidget,
                               QMessageBox
                               )
from .controllers.admin_panel import admin_panel
from .controllers.authenticated_users import authenticated_users
from .controllers.daily_authentication import daily_authentication
from .controllers.help_menu import help_menu
from .controllers.registry import registry

def get_path_image(nombre_imagen):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = os.path.join(script_dir, 'resources')
    imagen_path = os.path.join(resources_dir, nombre_imagen)

    if os.path.exists(imagen_path):
        return imagen_path
    else:
        raise FileNotFoundError(f"No se encontró la imagen: {nombre_imagen}")


class PrincipalSGID(QMainWindow):
    def __init__(self):
        super().__init__()
        self.action_exit = None
        self.action_help = None
        self.action_signature_sheet = None
        self.action_admin_panel = None
        self.action_authenticated = None
        self.action_daily = None
        self.stacked_widget = None
        self.toolbar = None
        icon = QIcon(get_path_image("app_icon/logo.ico"))
        self.setWindowIcon(icon)

        self.campos = self.load_users_authenticated()

        # Crear QAction y asignar QActionGroup
        self.action_group = QActionGroup(self)

        self.main_daily = daily_authentication.MainDaily(self.campos)

        self.auth_user = authenticated_users.AuthenticatedUsers(self.main_daily)

        self.admin_panel = admin_panel.AdminPanel()

        self.signature_sheet = registry.SignatureSheet()

        self.help_menu = help_menu.HelpMenu()

        self.create_actions()
        self.create_toolbar()
        self.create_stacked_widget()
        self.bottom_label = QLabel("Universidad de Artemisa\n2024", self)
        self.bottom_label.setAlignment(Qt.AlignCenter)
        self.bottom_label.setStyleSheet("font-size: 10px;")
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.stacked_widget)
        layout.addWidget(self.bottom_label)
        # Ajustar el margen inferior en -5 píxeles
        layout.setContentsMargins(0, 0, 0, -5)
        # dummy Widget to set the layout in the window
        widget = QWidget(self)
        # setting the layout on window
        widget.setLayout(layout)
        # centring the layout and widget in the window
        self.setCentralWidget(widget)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Sistema Gestor de Ingreso Diario SGID')
        self.showMaximized()
        self.show()

    def create_actions(self):
        """Creates the actions"""
        self.action_daily = QAction("Autenticaci\u00F3n Diaria", self)
        self.action_authenticated = QAction("Usuarios Autenticados", self)
        self.action_admin_panel = QAction("Panel Administraci\u00F3n", self)
        self.action_signature_sheet = QAction("Registro General", self)
        self.action_help = QAction("Ayuda", self)
        self.action_exit = QAction("Salir", self)

        self.action_daily.setCheckable(True)
        self.action_authenticated.setCheckable(True)
        self.action_admin_panel.setCheckable(True)
        self.action_signature_sheet.setCheckable(True)
        self.action_help.setCheckable(True)
        self.action_exit.setCheckable(True)

        self.action_group.addAction(self.action_daily)
        self.action_group.addAction(self.action_authenticated)
        self.action_group.addAction(self.action_admin_panel)
        self.action_group.addAction(self.action_signature_sheet)
        self.action_group.addAction(self.action_help)
        self.action_group.addAction(self.action_exit)

        self.action_daily.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.action_authenticated.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.action_signature_sheet.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.action_admin_panel.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.action_help.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.action_exit.triggered.connect(self.exit_program)

    def create_toolbar(self):
        """Creates the toolbar"""
        self.toolbar = QToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet(
            "QToolButton:hover {background-color: rgb(200, 225, 255);}"
            "QAction:checked {background-color: yellow;}"
        )
        self.toolbar.addAction(self.action_daily)
        self.toolbar.addAction(self.action_authenticated)
        self.toolbar.addAction(self.action_signature_sheet)
        self.toolbar.addAction(self.action_admin_panel)
        self.toolbar.addAction(self.action_help)
        self.toolbar.addAction(self.action_exit)

    def create_stacked_widget(self):
        """Creates the stacked widgets"""
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(self.main_daily)
        self.stacked_widget.addWidget(self.auth_user)
        self.stacked_widget.addWidget(self.signature_sheet)
        self.stacked_widget.addWidget(self.admin_panel)
        self.stacked_widget.addWidget(self.help_menu)

    def load_users_authenticated(self):
        try:
            with open('usuarios_autenticados.pkl', 'rb') as archivo:
                usuarios = pickle.load(archivo)
                if len(usuarios) == 0:
                    print('El archivo .pkl esta vacio')
                else:
                    print('El archivo .pkl no esta vacio')
                self.campos = usuarios
                print('Archivo Principal.py...')
                print('.pkl --> ', self.campos)
                return self.campos
        except FileNotFoundError:
            print('No existe archivo .pkl')
            return {}

    def exit_program(self):
        reply = QMessageBox.question(
            self,
            "Salir",
            "¿Estás seguro de que quieres salir del programa?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            QApplication.quit()


def main():
    # Find the name of the module that was used to start the app
    app_module = sys.modules['__main__'].__package__
    # Retrieve the app's metadata
    metadata = importlib_metadata.metadata(app_module)

    QApplication.setApplicationName(metadata['Sistema Gestor de Ingreso Diario SGID'])

    app = QApplication(sys.argv)
    p = PrincipalSGID()
    p.show()
    sys.exit(app.exec())
    

