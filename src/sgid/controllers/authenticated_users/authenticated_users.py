"""
    Module name: authenticated_users.py
    1. summary
    2. extended summary
    3. routine listings
    4. see also
    5. notes
    6. references
    7. examples
"""
import csv
import os
import sys

from PySide6.QtCore import QTimer, QDate, Qt, Slot, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget, QTableWidget, QGridLayout, QTableWidgetItem, QPushButton,
    QMessageBox, QHBoxLayout, QHeaderView, QFileDialog
)
from sgid.controllers.daily_authentication import daily_authentication


def get_path_image(nombre_imagen):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = os.path.join(script_dir, '..', '..', 'resources')
    imagen_path = os.path.join(resources_dir, nombre_imagen)

    if os.path.exists(imagen_path):
        return imagen_path
    else:
        raise FileNotFoundError(f"No se encontró la imagen: {nombre_imagen}")


class AuthenticatedUsers(QWidget):
    """
        A QWidget subclass that displays a table of authenticated users and
        provides functionality to export the table data to a CSV file, delete
        the daily registry of authenticated users, and navigate through the
        table.

        Attributes:
            pos (int): The current position/index in the table.
            table (QTableWidget): The table widget to display the user data.
            campos (MainDaily): An instance of MainDaily class to retrieve the
            user data.

        Methods:
            __init__(self, main_daily: MainDaily): Initializes the
            AuthenticatedUsers widget.
            display_values(self): Displays the user data in the table.
            export_to_csv(self): Exports the table data to a CSV file.
            delete_pkl_file(self): Deletes the daily registry file.
            show_confirmation_message(self): Displays a confirmation message
            box to delete the registry.
            update_indices(self): Updates the indices in the table.
            show_previous(self): Displays the previous 10 values in the table.
            show_next(self): Displays the next 10 values in the table.
        """

    def __init__(self, main_daily: daily_authentication.MainDaily):
        """
            Initialize the class with the given MainDaily instance.

            Parameters
            ----------
            main_daily : MainDaily
                The MainDaily instance used for initialization.

        """
        super().__init__()

        #
        self.pos = 1

        print('instancia2:', main_daily)
        self.campos = main_daily

        # Creamos la table y configuramos los encabezados
        self.table = QTableWidget(self)

        columnas = ["Nombre", "2do Nombre", "Apellido", "2do Apellido", "\u00C1rea",
                    "Hora de Entrada", "Hora de Salida"]
        self.table.setRowCount(15)
        self.table.setColumnCount(len(columnas))
        self.table.setHorizontalHeaderLabels(columnas)
        # Establecemos el tamaño de la table
        self.table.setFixedSize(954, 473)
        #
        # Ajustar el tamaño de las columnas al contenido
        for column in range(self.table.columnCount()):
            self.table.resizeColumnToContents(column)

        # Establecer las dos últimas columnas para ocupar el espacio restante de forma uniforme
        last_column = self.table.columnCount() - 1
        entry_column = last_column - 1
        area_column = last_column - 2
        second_last_name_column = last_column - 3
        last_name_column = last_column - 4
        name_column = last_column - 6
        self.table.horizontalHeader().setSectionResizeMode(name_column, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(
            last_name_column, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(
            second_last_name_column, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(area_column, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(entry_column, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(last_column, QHeaderView.Stretch)

        # Establecemos el estilo de la table
        self.table.setStyleSheet("""
                    QTableWidget::item:selected {
                        background-color: rgb(200, 225, 255);
                        color: black;
                    }
                """)

        self.table.horizontalHeader().setStyleSheet("""
                            background-color: rgb(200, 200, 200);
                            color: black;
                            font-weight: bold;
                        """)

        # Creamos el layout
        layout = QGridLayout(self)

        # Posicionamos la table en la celda 0,0
        layout.addWidget(self.table, 0, 0)

        # Creamos un contenedor para el botón y su diseño
        btn_container_g = QWidget(self)
        btn_container_h = QWidget(self)
        #
        btn_layout_g = QGridLayout(btn_container_g)
        #
        btn_layout_h = QHBoxLayout(btn_container_h)

        # Agregamos los botones de navegación al contenedor
        self.btn_prior = QPushButton(self)
        self.btn_prior.setIcon(QIcon(get_path_image("chevron-left.svg")))
        self.btn_prior.setFixedSize(25, 25)  # Establecemos el tamaño del botón
        self.btn_prior.setStyleSheet("background-color: lightblue;")
        btn_layout_h.addWidget(self.btn_prior, alignment=Qt.AlignHCenter)

        self.btn_next = QPushButton(self)
        self.btn_next.setIcon(QIcon(get_path_image("chevron-right.svg")))
        self.btn_next.setFixedSize(25, 25)  # Establecemos el tamaño del botón
        self.btn_next.setStyleSheet("background-color: lightblue;")
        btn_layout_h.addWidget(self.btn_next, alignment=Qt.AlignHCenter)
        # Create a QPushButton instance and set 'self' as its parent
        self.btn_csv = QPushButton(self)
        self.btn_csv.setToolTip(str("Exportar tabla .csv"))
        # Create a QIcon instance with the path to the SVG image
        icon = QIcon(get_path_image("filetype-csv.svg"))
        # Create a QPixmap from the SVG image with the desired size for the button
        pixmap = icon.pixmap(QSize(55, 20))
        # Set the QPixmap as the icon for the button
        self.btn_csv.setIcon(QIcon(pixmap))
        # Set the size of the button's icon to match the size of the QPixmap
        self.btn_csv.setIconSize(pixmap.size())
        # Set the fixed size of the button to 100x100 pixels
        self.btn_csv.setFixedSize(70, 30)
        # Set the background color of the button using CSS styling
        self.btn_csv.setStyleSheet(
            "background-color: lightgreen;")
        btn_layout_g.addWidget(self.btn_csv, 1, 1)
        # Create a QPushButton instance and set 'self' as its parent
        self.btn_eliminar = QPushButton(self)
        self.btn_eliminar.setToolTip(str("Limpiar registros"))
        # Create a QIcon instance with the path to the SVG image
        icon = QIcon(get_path_image("trash.svg"))
        # Create a QPixmap from the SVG image with the desired size for the button
        pixmap = icon.pixmap(QSize(55, 20))
        # Set the QPixmap as the icon for the button
        self.btn_eliminar.setIcon(QIcon(pixmap))
        # Set the size of the button's icon to match the size of the QPixmap
        self.btn_eliminar.setIconSize(pixmap.size())
        # Set the fixed size of the button to 100x100 pixels
        self.btn_eliminar.setFixedSize(70, 30)
        # Set the background color of the button using CSS styling
        self.btn_eliminar.setStyleSheet(
            "background-color: #FF5151;")
        btn_layout_g.addWidget(self.btn_eliminar, 1, 2)

        # Conectamos el botón a la función exportar_csv
        self.btn_csv.clicked.connect(self.export_to_csv)

        # Conectamos el botón a la función mostrar_mensaje_pregunta
        self.btn_eliminar.clicked.connect(self.show_confirmation_message)

        # Agregamos el contenedor al layout principal
        layout.addWidget(btn_container_h, 1, 0, alignment=Qt.AlignTop | Qt.AlignHCenter)
        #
        layout.addWidget(btn_container_g, 1, 0, alignment=Qt.AlignTop | Qt.AlignRight)

        # Conectar los botones a sus respectivas funciones
        self.btn_prior.clicked.connect(self.show_previous)
        self.btn_next.clicked.connect(self.show_next)
        #
        self.update_indices()
        #
        self.display_values()

        # Set the layout on the application's window
        self.setLayout(layout)

        # Configure a timer to update the table at regular intervals
        self.timer = QTimer(self)

        # Luego se muestran los datos en la interfaz
        self.timer.timeout.connect(self.update_indices)
        # Timer, when two seconds are reached, start from the beginning.
        # Refresh every 2 seconds (adjust interval to suit your needs)
        self.timer.start(2000)

    def display_values(self):
        """
            Display the values in the table.

            This method retrieves the values from the fields dictionary and
            displays them in the corresponding cells of the table.It also
            clears the table before showing new values.

            """
        valores = [n for n in self.campos.get_campos().values()]
        print('valores: ', valores)

        # Limpiar la table antes de mostrar nuevos valores
        self.table.clearContents()

        # Establecer el número de filas en la table
        self.table.setRowCount(15)

        # Recorrer los valores y mostrarlos en las celdas correspondientes
        for i, indice in enumerate(range(self.pos - 1, self.pos + 15)):
            # Verificar si el índice está dentro del rango de la lista
            # Esto es para actualizar los valors de la table
            if indice < len(valores):
                valores_usuario = valores[indice]
                for j, valor in enumerate(valores_usuario):
                    item = QTableWidgetItem(valor)
                    self.table.setItem(i, j, item)
            else:
                print('No hay valores para mostrar')

    def export_to_csv(self):
        global folder_selected
        try:
            folder_dialog = QFileDialog()
            folder_dialog.setFileMode(QFileDialog.Directory)
            folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)
            folder_selected = folder_dialog.getExistingDirectory(self, "Seleccionar directorio")
        except:
            print('Hubo un problema a la hora de guardar el archivo')

        tmp = True  # variable para algo

        if folder_selected:
            current_date = QDate.currentDate().toString("yyyy_MM_dd")
            filename = f"{current_date}_Registro_de_Asistencia_Diario.csv"
            filepath = os.path.join(folder_selected, filename)
            valores = []
            for fila in range(1000):  # un numero exageradamente grande
                if tmp:
                    fila_valores = []
                    for columna in range(self.table.columnCount()):
                        item = self.table.item(fila, columna)
                        if item is None and columna == 0:
                            tmp = False
                            break
                        elif item is not None:
                            fila_valores.append(item.text())
                        else:
                            fila_valores.append("")
                    valores.append(fila_valores)
                else:
                    break

            with open(filepath, "w", newline="") as archivo_csv:
                escritor = csv.writer(archivo_csv)
                for fila_valores in valores:
                    escritor.writerow(fila_valores)
            print(f"Archivo {filename} exportado correctamente.")
        else:
            print("No se pudo exportar el archivo .csv")

    def delete_pkl_file(self):
        """
            Delete the .pkl file and remove all records.

            This method checks if a .pkl file exists and deletes it, along with
            removing all the records(including those displayed visually on the
            screen) from the document.
        """
        self.campos.clear_campos()
        os.remove('usuarios_autenticados.pkl')
        try:
            # Eliminar el archivo usuarios_autenticados.pkl
            os.remove('usuarios_autenticados.pkl')
            print("Archivo usuarios_autenticados.pkl eliminado correctamente.")
        except FileNotFoundError:
            print("El archivo usuarios_autenticados.pkl no existe.")
        except Exception as e:
            print(f"Error al eliminar el archivo usuarios_autenticados.pkl: {str(e)}")

    @Slot()
    def show_confirmation_message(self):
        """
            Display a confirmation message box.

            This method displays a message box with a confirmation question.
            If the user selects 'Yes', it calls the delete_pkl_file method to
            delete the daily registry of authenticated users.
            If the user selects 'No', it prints a corresponding message.

            """
        text = "¿Estás seguro de realizar esta acción? " \
               "Se eliminara el registry diario de usurios autenticados " \
               "hasta el momento. "
        message = QMessageBox.question(self, "Pregunta", text)
        if message == QMessageBox.Yes:
            self.delete_pkl_file()
            self.campos.show_data({})
            print("Se seleccionó 'Sí'")
        else:
            print("Se seleccionó 'No'")

    def update_indices(self):
        """
            Update the index values in the table.

            This method updates the index values in the table based on the
            initial row position.
            It calls the display_values method to refresh the table data and
            then updates the vertical header items.

            """
        """Actualiza los valores de los índices en la table"""
        fila_inicial = self.pos
        # print('-----------------------------------------------------')
        # print('Actualizar indices:')
        # print('fila_inicial', fila_inicial)
        # print('self.table.rowCount()', self.table.rowCount())
        self.display_values()
        for i in range(self.table.rowCount()):
            self.table.setVerticalHeaderItem(
                i, QTableWidgetItem(str(fila_inicial + i))
            )

    def show_previous(self):
        """
        Show the previous 10 values in the table.
        """
        if self.pos - 10 <= 0:
            print('no se puede ir mas hacia atras')
        else:
            # if self.pos - 10 <= self.table.rowCount():
            self.pos = self.pos - 10
            self.table.setCurrentCell(self.pos, 0)
            self.update_indices()

    def show_next(self):
        """
        Show the next 10 values in the table.
        """
        self.pos = self.pos + 10
        if self.pos + 10 >= self.table.rowCount():
            self.table.setCurrentCell(self.pos, 0)
            self.update_indices()
