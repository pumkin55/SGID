import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton


def get_path_image(nombre_imagen):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = os.path.join(script_dir, '..', '..', 'resources')
    imagen_path = os.path.join(resources_dir, nombre_imagen)

    if os.path.exists(imagen_path):
        return imagen_path
    else:
        raise FileNotFoundError(f"No se encontró la imagen: {nombre_imagen}")


class HelpMenu(QWidget):
    def __init__(self):
        super().__init__()
        # Obtener las imágenes en resources/help_menu
        self.image_files = []
        self.current_image_index = 0

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Agregamos los botones de navegación al contenedor
        self.btn_prior = QPushButton(self)
        self.btn_prior.setIcon(QIcon(get_path_image("chevron-left.svg")))
        self.btn_prior.setFixedSize(25, 25)  # Establecemos el tamaño del botón
        self.btn_prior.setStyleSheet("background-color: lightblue;")

        self.btn_next = QPushButton(self)
        self.btn_next.setIcon(QIcon(get_path_image("chevron-right.svg")))
        self.btn_next.setFixedSize(25, 25)  # Establecemos el tamaño del botón
        self.btn_next.setStyleSheet("background-color: lightblue;")

        # Conectar los botones a los métodos correspondientes
        self.btn_prior.clicked.connect(self.show_previous_image)
        self.btn_next.clicked.connect(self.show_next_image)

        # Crear el layout principal y los layouts para los botones
        main_layout = QVBoxLayout(self)
        button_layout_h = QHBoxLayout()

        # Agregar los widgets al layout
        main_layout.addWidget(self.image_label)
        button_layout_h.addWidget(self.btn_prior)
        button_layout_h.addWidget(self.btn_next)
        main_layout.addLayout(button_layout_h)

        # Mostrar la primera imagen
        self.show_image(self.current_image_index)

    def show_image(self, index):
        try:
            # Cargar la imagen correspondiente al índice actual
            image_path = self.image_files[index]
            pixmap = QPixmap(image_path)

            # Definir el tamaño deseado para la imagen
            desired_width = 400
            desired_height = 575

            # Redimensionar la imagen al tamaño deseado
            scaled_pixmap = pixmap.scaled(desired_width, desired_height, Qt.AspectRatioMode.KeepAspectRatio)

            # Mostrar la imagen en el QLabel
            self.image_label.setPixmap(scaled_pixmap)

        except IndexError:
            print("No se encontraron imágenes con el prefijo especificado o la lista está vacía.")
            self.image_label.setText("Actualmente no existe ayuda disponible. Disculpe las molestias.")
            self.image_label.setStyleSheet("font-family: Arial; font-size: 24pt;")
            self.btn_next.hide()
            self.btn_prior.hide()

    def show_previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image(self.current_image_index)

    def show_next_image(self):
        if self.current_image_index < len(self.image_files) - 1:
            self.current_image_index += 1
            self.show_image(self.current_image_index)
