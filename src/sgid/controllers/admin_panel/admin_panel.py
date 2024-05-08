"""
    Module name: admin_panel.py
    1. summary
    2. extended summary
    3. routine listings
    4. see also
    5. notes
    6. references
    7. examples
"""
import os
import re
from typing import Any

from PySide6.QtCore import Qt, QRegularExpression, QTimer
from PySide6.QtGui import QIcon, QFont, QPixmap, QRegularExpressionValidator
from PySide6.QtWidgets import QWidget, QTableWidget, QPushButton, QLabel, QLineEdit, \
    QHBoxLayout, QVBoxLayout, QFrame, QSpacerItem, QSizePolicy, QDialog, QApplication, QComboBox, QFormLayout, \
    QGridLayout, QTableWidgetItem, QMessageBox, QHeaderView, QDialogButtonBox
from sgid.models import data_access


def get_path_image(nombre_imagen):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = os.path.join(script_dir, '..', '..', 'resources')
    imagen_path = os.path.join(resources_dir, nombre_imagen)

    if os.path.exists(imagen_path):
        return imagen_path
    else:
        raise FileNotFoundError(f"No se encontró la imagen: {nombre_imagen}")

def check_ci_input_user(ci) -> bool:
        """Valida el ci introducido por el usuario"""
        regex = re.compile(r'^[0-9]{11}$')

        if ci == '':
            return False

        if not regex.match(ci):
            print("Introduzca un valor válido", ci)
            # QMessageBox.warning("Advertencia", "Introduzca un valor válido.")
            return False

        return True

class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()

        # Crear QFrame para el área de filtrado
        self.boton_eliminar = None
        self.boton_editar = None
        self.worker_list = []
        self.timer = QTimer(self)
        filter_frame = QFrame()
        filter_frame.setObjectName("FilterFrame")  # Establecer un nombre de objeto para aplicar estilo CSS
        filter_frame.setFrameShape(QFrame.StyledPanel)  # Establecer el estilo del panel
        filter_frame.setFixedHeight(90)
        #
        self.worker_add = WorkerCRUD()
        self.worker_up = WorkerCRUD()
        #
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # Aplicar estilo CSS al QFrame
        filter_frame.setStyleSheet("""
                            QFrame#FilterFrame {
                                /* Establecer un borde de 2 píxeles de ancho en color negro */
                                border: 2px solid #000000;  
                                /* Redondear las esquinas del borde */
                                border-radius: 5px;  
                                /* Establecer un color de fondo para resaltar el área */
                                background-color: #F0F0F0;  
                                /* Agregar un margen para separar el área del borde de la ventana */
                                margin: 10px;  
                            }
                        """)
        # Crear layout vertical para los widgets de filtrado
        filter_layout = QHBoxLayout(filter_frame)
        #
        layout_table = QHBoxLayout()
        # Creamos la tabla y configuramos los encabezados
        self.table = QTableWidget()
        self.table.setRowCount(15)
        columnas = ["Nombre", "2do Nombre", "Apellido", "2do Apellido", "CI", "\u00C1rea",
                    "Departamento", "Cargo", "Editar", "Eliminar"]
        self.table.setColumnCount(len(columnas))
        #
        self.table.setHorizontalHeaderLabels(columnas)
        #
        self.table.setFixedHeight(473)  # Se ajusta el alto de la tabla
        # Establecemos el estilo de la tabla
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
        # Ajustar el tamaño de la encabezado horizontal para ocupar solo el espacio necesario
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # Establecer las dos últimas columnas para ocupar el espacio restante de forma uniforme
        last_column = self.table.columnCount() - 1
        job_position_column = last_column - 2
        department_column = last_column - 3
        area_column = last_column - 4
        self.table.horizontalHeader().setSectionResizeMode(area_column, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(department_column, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(job_position_column, QHeaderView.Stretch)

        self.table.setColumnWidth(last_column - 1, 110)
        self.table.setColumnWidth(last_column, 110)

        # Creamos el layout
        layout = QVBoxLayout(self)
        # Botón "Adicionar Trabajador"
        self.boton_adicionar = QPushButton(self)
        self.boton_adicionar.setIcon(QIcon(get_path_image("person-plus.svg")))
        self.boton_adicionar.setToolTip(str("Adicionar Trabajador"))
        self.boton_adicionar.setFixedSize(100, 25)  # Establecemos el tamaño del botón
        self.boton_adicionar.setStyleSheet("background-color: lightgreen;")
        filter_layout.addWidget(self.boton_adicionar)

        # Label "Buscar por ci"
        label_buscar_ci = QLabel("Filtrar por CI:")
        filter_layout.addWidget(label_buscar_ci)

        # Campo de entrada de datos
        self.ci = QLineEdit()
        self.ci.setToolTip(str("Buscar trabajador por CI"))
        self.ci.setFixedWidth(150)
        self.ci.setMaxLength(11)
        # Expresión regular para permitir solo números del 0 al 9
        regex = QRegularExpression("^[0-9]{11}$")
        # Validador de expresión regular
        validator = QRegularExpressionValidator(regex)
        # Establecer el validador en el campo de texto
        self.ci.setValidator(validator)
        filter_layout.addWidget(self.ci)
        self.boton_buscar = QPushButton(self)
        self.boton_buscar.setIcon(QIcon(get_path_image("search.svg")))
        self.boton_buscar.setFixedSize(40, 25)  # Establecemos el tamaño del botón
        self.boton_buscar.setStyleSheet("background-color: lightblue;")
        filter_layout.addWidget(self.boton_buscar, alignment=Qt.AlignLeft)
        filter_layout.addWidget(self.boton_buscar)
        filter_layout.addStretch(0)  # Agregar espacio elástico al final del layout
        self.btn_prior = QPushButton(self)
        self.btn_prior.setIcon(QIcon((get_path_image("chevron-left.svg"))))
        self.btn_prior.setFixedSize(25, 25)
        self.btn_prior.setStyleSheet("background-color: lightblue;")
        self.btn_next = QPushButton(self)
        self.btn_next.setIcon(QIcon(get_path_image("chevron-right.svg")))
        self.btn_next.setFixedSize(25, 25)
        self.btn_next.setStyleSheet("background-color: lightblue;")
        self.btn_first = QPushButton(self)
        self.btn_first.setIcon(QIcon(get_path_image("chevron-bar-left.svg")))
        self.btn_first.setFixedSize(25, 25)  # Establecemos el tamaño del botón
        self.btn_first.setStyleSheet("background-color: lightblue;")
        self.btn_last = QPushButton(self)
        self.btn_last.setIcon(QIcon(get_path_image("chevron-bar-right.svg")))
        self.btn_last.setFixedSize(25, 25)  # Establecemos el tamaño del botón
        self.btn_last.setStyleSheet("background-color: lightblue;")
        # Layout para distribuir los botones btn_first,btn_prior,btn_next,btn_last
        btn_layout = QHBoxLayout()
        # Establecer margen de 5 píxeles entre los widgets
        btn_layout.setSpacing(5)
        btn_layout.addItem(spacer)
        btn_layout.addWidget(self.btn_first)
        btn_layout.addWidget(self.btn_prior)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addWidget(self.btn_last)
        btn_layout.addItem(spacer)
        # Agregamos el QHBoxLayout al layout principal
        layout.addWidget(filter_frame)
        layout_table.addWidget(self.table)
        layout.addLayout(layout_table)
        layout.addLayout(btn_layout)
        self.edit_delete_buttons()
        # Set the layout on the application's window
        self.setLayout(layout)
        #
        self.pos = 0
        # Conectar los botones a sus respectivas funciones
        self.btn_prior.clicked.connect(self.show_previous)
        self.btn_next.clicked.connect(self.show_next)
        self.btn_first.clicked.connect(self.show_first)
        self.btn_last.clicked.connect(self.show_last)
        # Luego se muestran los datos en la interfaz
        self.timer.timeout.connect(self.display_values)
        # Conexión del botón "boton_adicionar" con el método add_worker
        self.boton_adicionar.clicked.connect(self.press_add_worker)
        # Conexión del botón "boton_adicionar" con el método show_user_by_ci
        self.boton_buscar.clicked.connect(self.update_worker_init_process)
        # Iniciar temporizador para mostrar los datos
        self.timer.start(2000)

    def press_add_worker(self):
        self.worker_add.add_worker_from_interface()
        self.worker_add.show()
        self.worker_add.exec()

    def update_worker_init_process(self) -> None:
        # obtener el objeto que emitió la señal
        sender_button = self.sender()
        global worker_data
        ci = self.ci.text()
        if (len(ci) == 11) and (sender_button == self.boton_buscar):
            worker_data = data_access.get_fields_by_ci(ci)
        elif sender_button in self.boton_editar_list:
            # Obtener el botón que emitió la señal
            button = self.sender()
            # Obtener la posición del botón en la tabla
            index = self.table.indexAt(button.pos())
            # Obtener el número de fila
            row = index.row()
            row = self.pos + row
            # Datos actuales del trabajador seleccionado
            worker_data = self.worker_list[row]
            worker_data = data_access.get_fields_by_ci(worker_data[5])
        else:
            worker_data = None

        if worker_data:
            self.worker_up.update_worker_from_interface(worker_data.values())
            self.worker_up.show()
            self.worker_up.exec()
        else:
            print('Insufficient data to update an employee')
            pass
        pass

    def edit_delete_buttons(self):
        # Lista para almacenar los botones self.boton_editar
        self.boton_editar_list = []
        # Añadimos los botones a la tabla
        for i in range(0, 15):
            self.boton_editar = QPushButton(self)
            self.boton_eliminar = QPushButton(self)
            self.boton_editar.setIcon(QIcon(get_path_image("pencil-square.svg")))
            self.boton_editar.setFixedSize(109, 29)
            self.boton_editar.setStyleSheet("background-color: lightblue;")
            self.boton_eliminar.setIcon(QIcon(get_path_image("trash.svg")))
            self.boton_eliminar.setFixedSize(109, 29)
            self.boton_eliminar.setStyleSheet("background-color: #FF5151")
            #
            self.boton_editar.clicked.connect(self.update_worker_init_process)
            self.boton_eliminar.clicked.connect(self.delete_worker_row)
            #
            self.table.setCellWidget(i, 8, self.boton_editar)
            self.table.setCellWidget(i, 9, self.boton_eliminar)

            self.boton_editar_list.append(self.boton_editar)  # Agregar el botón a la lista

    def delete_worker_row(self):
        button = self.sender()  # Obtener el botón que emitió la señal
        index = self.table.indexAt(button.pos())  # Obtener la posición del botón en la tabla
        row = index.row()  # Obtener el número de fila
        row = self.pos + row
        print("Fila seleccionada:", row)
        w_data = self.worker_list[row]
        worker_id = w_data[0]  # Assuming the worker ID is at index 0 in the worker_list
        text = (f"Eliminar a {self.worker_list[row][1]} "
                f"{self.worker_list[row][2]} "
                f"{self.worker_list[row][3]} "
                f"{self.worker_list[row][4]} ")
        reply = QMessageBox.question(
            self, 'Confirmar Eliminación', text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            data_access.delete_worker(worker_id)
            self.worker_list.pop(row)
            self.display_values()

    def display_values(self):
        workers = data_access.get_all_workers()
        self.worker_list = []
        for worker_id, worker_d in workers.items():
            worker_dict = {
                'id': worker_id,  # 0
                'name': worker_d['name'],  # 1
                'middle_name': worker_d['middle_name'],  # 2
                'last_name': worker_d['last_name'],  # 3
                'second_last_name': worker_d['second_last_name'],  # 4
                'ci': worker_d['ci'],  # 5
                'work_area': worker_d['work_area'],  # 6
                'department': worker_d['department'],  # 7
                'job_position': worker_d['job_position'],  # 8
                'gender': worker_d['gender'],  # 9
            }
            self.worker_list.append(list(worker_dict.values()))

        # Limpiar la tabla antes de mostrar nuevos valores
        self.table.clearContents()
        self.edit_delete_buttons()

        # Recorrer los valores y mostrarlos en las celdas correspondientes
        for i, indice in enumerate(range(self.pos, self.pos + 15)):
            if indice < len(self.worker_list):
                v = self.worker_list[indice]
                for j, k in enumerate(v[1:9]):
                    item = QTableWidgetItem(str(k))
                    self.table.setItem(i, j, item)
            else:
                # print('No hay valores para mostrar')
                pass

    def update_indices(self):
        """
            Update the index values in the table.

            This method updates the index values in the table based on the
            initial row position.
            It calls the display_values method to refresh the table data and
            then updates the vertical header items.

            """
        print(f"------------------------------------------------------ \n"
              f"Actualizar indices: \n"
              f"fila actual de la tabla: {self.pos} \n"
              f"numero de filas de la tabla:{self.table.rowCount()} \n")
        self.display_values()
        for i in range(self.table.rowCount()):
            print('i:', i, 'QTableWidgetItem(str(self.pos + i): ', QTableWidgetItem(str(self.pos + i)))
            self.table.setVerticalHeaderItem(
                i, QTableWidgetItem(str(self.pos + i + 1))
            )

    def show_previous(self) -> None:
        """
            Show the previous 15 values in the table.
        """
        var = 15
        if self.pos - var < 0:
            self.pos = 0
            print('no se puede ir mas hacia atras')
        else:
            self.pos = self.pos - var
            self.table.setCurrentCell(self.pos, 0)
            self.update_indices()

    def show_next(self) -> None:
        """
            Show the next 15 values in the table.

        """
        var = 15
        self.pos = self.pos + var
        self.table.setCurrentCell(self.pos, 0)
        self.update_indices()

    def show_first(self) -> None:
        var = 15
        if self.pos - var < 0:
            self.pos = 0
            print('no se puede ir mas hacia atras')
        else:
            self.pos = 0
            self.table.setCurrentCell(self.pos, 0)
            self.update_indices()
        pass

    def show_last(self) -> None:
        var = 15
        last_position = len(self.worker_list) - 1
        if last_position < var:
            self.pos = 0
        else:
            self.pos = last_position - (last_position % var)
        self.table.setCurrentCell(self.pos, 0)
        self.update_indices()


class WorkerCRUD(QDialog):
    def __init__(self):
        super().__init__()
        # Configuración de la ventana auxiliar
        self.setFixedSize(700, 500)
        self.setModal(True)
        # Formulario
        self.formulario = FormularioWorker()
        self.layout = QVBoxLayout()
        self.layout_grid = QGridLayout()
        self.close_buttom = QPushButton("Cerrar")
        self.aply_buttom = QPushButton("Aplicar")
        self.layout_v = QVBoxLayout()
        self.layout_h = QHBoxLayout()
        # Creación de los botones de aceptar y cerrar
        self.button_box = QDialogButtonBox()
        self.save_button = self.button_box.addButton("Guardar", QDialogButtonBox.AcceptRole)
        self.cancel_button = self.button_box.addButton("Cancelar", QDialogButtonBox.RejectRole)

        self.save_button.setStyleSheet("background-color: lightblue;")
        self.save_button.setFixedSize(90, 40)
        self.cancel_button.setStyleSheet("background-color: red;")
        self.cancel_button.setFixedSize(90, 40)

        # Configuración de eventos
        self.save_button.clicked.connect(self.add_worker_data)
        self.cancel_button.clicked.connect(self.close)

    def add_worker_from_interface(self):
        self.setWindowTitle("Adicionar Trabajador")
        self.formulario.reset_form()
        # Agregar un espacio flexible para empujar los botones hacia la derecha
        self.layout_h.addStretch(1)
        self.layout_h.addWidget(self.save_button)
        self.layout_h.addWidget(self.cancel_button)
        self.layout.addWidget(self.formulario)
        self.layout_v.addLayout(self.layout)
        self.layout_v.addLayout(self.layout_h)
        self.setLayout(self.layout_v)

    def update_worker_from_interface(self, data):
        # variable para poder obtener el ci del usuario y que la app
        # no me de batae a la hora de update
        self.tmp = list(map(str, data))[0]
        self.setWindowTitle("Editar Datos del Trabajador")
        #
        self.close_buttom.setFixedSize(100, 30)  # Establecemos el tamaño del botón
        self.close_buttom.setStyleSheet("background-color: lightgray;")
        #
        self.aply_buttom.setFixedSize(100, 30)  # Establecemos el tamaño del botón
        self.aply_buttom.setStyleSheet("background-color: lightgreen;")

        # Create the necessary UI elements
        label_photo_title = QLabel(self)
        label_photo_title.setText("Foto")
        label_photo_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Set the font style
        font = QFont("Verdana", 18)
        label_photo_title.setFont(font)
        label_worker_photo = QLabel(self)
        photo_path = get_path_image("unknow.png")
        pixmap = QPixmap(photo_path).scaled(250, 200, Qt.AspectRatioMode.KeepAspectRatio)
        label_worker_photo.setPixmap(pixmap)
        label_worker_photo.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align the photo to the center

        label_datos = QLabel(self)
        label_datos.setText("Datos del trabajador")
        label_datos.setFont(font)

        # Area: Form
        self.layout.addWidget(self.formulario)

        # Create a QGridLayout to hold the UI elements
        self.layout_grid.addWidget(label_datos, 0, 0, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.layout_grid.addLayout(self.layout, 1, 0, 1, 2)
        self.layout_grid.addWidget(label_photo_title, 0, 3, 1, 2, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.layout_grid.addWidget(label_worker_photo, 1, 3, 1, 2, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.layout_grid.addWidget(self.close_buttom, 3, 4)
        self.layout_grid.addWidget(self.aply_buttom, 3, 3)
        self.setLayout(self.layout_grid)
        #
        self.formulario.set_values_form(data)
        # Events
        self.aply_buttom.clicked.connect(self.update_worker_data)
        self.close_buttom.clicked.connect(self.close)

    def update_worker_data(self):
        w = self.formulario.return_worker_data()
        w.insert(0, self.tmp)
            
        if w:
            data_access.update_worker(*w)
            self.accept()
        else:
            pass

    def add_worker_data(self) -> None:
        w = self.formulario.return_worker_data()
        if w:
            if data_access.is_user_in_worker(w[4]):
                QMessageBox.warning(self, "Warning", 
                                    "El campo CI se encuentra registrado en la base de datos.")
            elif data_access.is_user_phone_in_worker(w[10]):
                QMessageBox.warning(self, "Warning", 
                                    "El campo Número Telefónico se encuentra registrado en la base de datos.")
            else:
                data_access.create_worker(*w)
                self.accept()
                


class FormularioWorker(QDialog):
    def __init__(self):
        super().__init__()
        # Creación de los campos del formulario
        self.nombre_field = QLineEdit()
        self.nombre_field.setValidator(QRegularExpressionValidator(QRegularExpression("[A-Za-z]{1,30}")))
        self.segundo_nombre_field = QLineEdit()
        self.segundo_nombre_field.setValidator(QRegularExpressionValidator(QRegularExpression("[A-Za-z]{1,30}")))
        self.apellido_field = QLineEdit()
        self.apellido_field.setValidator(QRegularExpressionValidator(QRegularExpression("[A-Za-z]{1,30}")))
        self.segundo_apellido_field = QLineEdit()
        self.segundo_apellido_field.setValidator(QRegularExpressionValidator(QRegularExpression("[A-Za-z]{1,30}")))
        #
        self.ci_field = QLineEdit()
        self.ci_field.setMaxLength(11)
        # Expresión regular para permitir solo números del 0 al 9
        regex = QRegularExpression("^[0-9]{11}$")
        # Validador de expresión regular
        validator = QRegularExpressionValidator(regex)
        # Establecer el validador en el campo de texto
        self.ci_field.setValidator(validator)
        #
        self.area_field = QComboBox()
        self.area_field.addItem("Human Resources")
        self.area_field.addItem("Informatizaci\u00F3n")
        self.area_field.addItem("Academic Affairs")
        self.area_field.addItem("Administration")
        self.area_field.addItem("Facilities Management")
        self.area_field.addItem("Security")
        self.area_field.currentIndexChanged.connect(self.update_departments)
        #
        self.departamento_field = QComboBox()
        #
        self.job_position_field = QComboBox()

        self.departments = {
            "Human Resources": ["Recruitment", "Training and Development",
                                "Employee Relations",
                                "Compensation and Benefits",
                                "HR Information Systems"],
            "Informatizaci\u00F3n": ["Direcci\u00F3n de Informatizaci\u00F3n",
                                     "Seguridad Inform\u00E1tica",
                                     "Educai\u00F3n a Distancia",
                                     "Dise\u00F1o de Software",
                                     "Asistencia T\u00E9cnica",
                                     "Nodo",
                                     "Laboratorio",
                                     "Respaldo E\u00E9lectrico",
                                     ],
            "Academic Affairs": ["Registrar's Office",
                                 "Curriculum Development",
                                 "Student Affairs",
                                 "Faculty Affairs",
                                 "Quality Assurance"],
            "Administration": ["Finance", "Procurement", "Human Resources", "Facilities Management", "Legal"],
            "Facilities Management": ["Maintenance", "Custodial Services", "Groundskeeping", "Energy Management",
                                      "Space Planning"],
            "Security": ["Campus Patrol", "Access Control", "Emergency Response", "Investigations",
                         "Security Monitoring"]
        }

        self.job_positions = {
            "Human Resources": ["HR Manager", "Recruiter", "Training Specialist", "Employee Relations Officer",
                                "Compensation Analyst"],
            "Informatizaci\u00F3n": ["Director de Informatizaci\u00F3n",
                                     "Especialista en Seguridad Inform\u00E1tica",
                                     "Especialista de Tecnolog\u00EDa Educativa",
                                     "Especialista en Desarrollo de Software",
                                     "Especialista en Dise\u00F1o de Software",
                                     "Especialista en Asistencia T\u00E9cnica",
                                     "Especialista en Administraci\u00F3n de Redes",
                                     ],
            "Academic Affairs": ["Registrar", "Curriculum Developer", "Student Affairs Officer",
                                 "Faculty Affairs Officer",
                                 "Quality Assurance Analyst"],
            "Administration": ["Finance Manager", "Procurement Officer", "HR Generalist", "Facilities Manager",
                               "Legal Counsel"],
            "Facilities Management": ["Maintenance Supervisor", "Custodial Services Coordinator",
                                      "Groundskeeping Manager",
                                      "Energy Management Specialist", "Space Planner"],
            "Security": ["Security Manager", "Security Officer", "Emergency Response Coordinator", "Investigator",
                         "Security Monitoring Specialist"]
        }

        self.update_departments()
        self.update_job_positions()
        #
        self.nivel_academico_field = QComboBox()
        self.nivel_academico_field.addItem("Universidad")
        self.nivel_academico_field.addItem("Pre Universitario")
        self.nivel_academico_field.addItem("T\u00E9cnico Medio")
        self.nivel_academico_field.addItem("Secundaria")
        #
        self.genero_field = QComboBox()
        self.genero_field.addItem("Masculino")
        self.genero_field.addItem("Femenino")
        #
        self.telefono_field = QLineEdit()
        self.telefono_field.setMaxLength(8)
        # Expresión regular para permitir solo números del 0 al 9
        regex_phone = QRegularExpression("^[0-9]{11}$")
        # Validador de expresión regular
        validator_phone = QRegularExpressionValidator(regex_phone)
        # Establecer el validador en el campo de texto
        self.telefono_field.setValidator(validator_phone)
        #
        self.provinces_cuba = {
            "Pinar del Río": ["Pinar del Río", "San Juan y Martínez", "San Luis", "Consolación del Sur", "Guane",
                              "Minas de Matahambre", "Mantua"],
            "Artemisa": ["Artemisa", "Bahía Honda", "Candelaria", "Mariel", "San Cristóbal", "Guanajay", "Caimito",
                         "Bauta", "San Antonio de los Baños", "Alquízar"],
            "La Habana": ["La Habana Vieja", "Centro Habana", "Regla", "Cerro", "Marianao", "La Lisa", "Playa",
                          "Plaza de la Revolución", "Habana del Este", "Guajimar", "Diez de Octubre"],
            "Mayabeque": ["Bejucal", "Güines", "Quivicán", "San José de las Lajas", "Melena del Sur", "Nueva Paz",
                          "Santa Cruz del Norte"],
            "Matanzas": ["Matanzas", "Cárdenas", "Colón", "Jovellanos", "Pedro Betancourt", "Perico", "Limonar",
                         "Los Arabos", "Unión de Reyes", "Jagüey Grande"],
            "Cienfuegos": ["Cienfuegos", "Cruces", "Palmira", "Rodas", "Lajas", "Abreus"],
            "Villa Clara": ["Santa Clara", "Santo Domingo", "Caibarién", "Remedios", "Sagua la Grande", "Camajuaní",
                            "Encrucijada", "Placetas", "Quemado de Güines"],
            "Sancti Spíritus": ["Trinidad", "Cabaiguán", "Fomento", "Jatibonico", "La Sierpe", "Sancti Spíritus"],
            "Ciego de Ávila": ["Ciego de Ávila", "Morón", "Chambas", "Majagua", "Primero de Enero", "Venezuela"],
            "Camagüey": ["Camagüey", "Florida", "Esmeralda", "Vertientes", "Sibanicú", "Guáimaro", "Nuevitas",
                         "Santa Cruz del Sur", "Minas"],
            "Las Tunas": ["Las Tunas", "Puerto Padre", "Majibacoa", "Jobabo", "Colombia", "Amancio"],
            "Holguín": ["Holguín", "Banes", "Gibara", "Rafael Freyre", "Antilla", "Baguanos", "Calixto García",
                        "Cacocum", "Cueto", "Frank País", "Sagua de Tánamo"],
            "Granma": ["Bayamo", "Manzanillo", "Media Luna", "Niquero", "Yara", "Campechuela", "Guisa",
                       "Bartolomé Masó", "Jiguaní", "Pilón"],
            "Santiago de Cuba": ["Santiago de Cuba", "Contramaestre", "Mella", "San Luis", "Songo-La Maya",
                                 "Palma Soriano", "Tercer Frente", "Guamá"],
            "Guantánamo": ["Guantánamo", "Baracoa", "Yateras", "Imías", "San Antonio del Sur", "Caimanera",
                           "El Salvador", "Manuel Tames"],
            "Isla de la Juventud": ["Isla de la Juventud"]
        }
        self.province_field = QComboBox()
        self.province_field.addItems(self.provinces_cuba.keys())
        #
        self.municipality_field = QComboBox()
        #
        self.update_municipalities()
        #
        self.province_field.currentIndexChanged.connect(self.update_municipalities)

        # Diseño del formulario
        layout = QVBoxLayout()
        #
        layout_h = QHBoxLayout()
        #
        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form_layout.addRow("Nombre:", self.nombre_field)
        form_layout.addRow("2do Nombre:", self.segundo_nombre_field)
        form_layout.addRow("Apellido:", self.apellido_field)
        form_layout.addRow("2do Apellido:", self.segundo_apellido_field)
        form_layout.addRow("Carnet de Identidad:", self.ci_field)
        form_layout.addRow("\u00C1rea:", self.area_field)
        form_layout.addRow("Departamento:", self.departamento_field)
        form_layout.addRow("Cargo:", self.job_position_field)
        form_layout.addRow("Nivel Académico:", self.nivel_academico_field)
        form_layout.addRow("Género:", self.genero_field)
        form_layout.addRow("Número Telefónico:", self.telefono_field)
        form_layout.addRow("Provincia:", self.province_field)
        form_layout.addRow("Municipio:", self.municipality_field)
        layout.addLayout(form_layout)

        # Agregar un QSpacerItem flexible al final del layout_h para empujar los botones hacia la derecha
        spacer_item = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Diseño de los botones
        layout_h.addItem(spacer_item)
        layout.addLayout(layout_h)
        self.setLayout(layout)

    def return_worker_data(self) -> bool | list[str | Any]:
        # Validar los campos de QComboBox
        if not validate_combobox(self.area_field):
            return False

        if not validate_combobox(self.departamento_field):
            return False

        if not validate_combobox(self.job_position_field):
            return False

        # Obtener los valores de los campos del formulario
        name = self.nombre_field.text()

        if not name:
            QMessageBox.warning(self, "Warning", "El campo Nombre no puede estar vacío.")
            return False

        middle_name = self.segundo_nombre_field.text()

        last_name = self.apellido_field.text()
        second_last_name = self.segundo_apellido_field.text()

        if not last_name:
            QMessageBox.warning(self, "Warning", "El campo Apellido no puede estar vacío.")
            return False

        if not second_last_name:
            QMessageBox.warning(self, "Warning", "El campo Segundo Apellido no puede estar vacío.")
            return False
        
        ci = self.ci_field.text()
        if check_ci_input_user(ci) and len(ci) == 11:
            pass
        elif not ci:
            a = QMessageBox.warning(self, "Warning", "El campo Carnet de Identidad no puede estar vacío.")
            return False
        else:
            QMessageBox.warning(self, "Warning", "El campo Carnet de Identidad debe tener 11 dígitos.")
            return False

        phone = self.telefono_field.text()

        if not phone:
            QMessageBox.warning(self, "Warning", "El campo Número Telefónico no puede estar vacío.")
            return False
        elif len(phone) < 8:
            QMessageBox.warning(self, "Warning", "El campo Número Telefónico debe tener 8 dígitos.")
            return False
        else:
            pass

        area = self.area_field.currentText()
        department = self.departamento_field.currentText()
        job_position = self.job_position_field.currentText()
        degree = self.nivel_academico_field.currentText()
        gender = self.genero_field.currentText()
        province = self.province_field.currentText()
        municipality = self.municipality_field.currentText()
        
        worker_list = [name, middle_name, last_name, second_last_name, ci, area,
                       department, job_position, degree, gender, phone, province, 
                       municipality]
        return worker_list

    def update_departments(self):
        selected_area = self.area_field.currentText()
        selected_departments = self.departments.get(selected_area, [])

        self.departamento_field.clear()
        self.departamento_field.addItems(selected_departments)
        self.departamento_field.setEnabled(bool(selected_departments))

        self.update_job_positions()

    def update_job_positions(self):
        selected_area = self.area_field.currentText()
        selected_job_positions = self.job_positions.get(selected_area, [])

        self.job_position_field.clear()
        self.job_position_field.addItems(selected_job_positions)
        self.job_position_field.setEnabled(bool(selected_job_positions))

    def update_municipalities(self):
        selected_province = self.province_field.currentText()
        municipalities = self.provinces_cuba[selected_province]
        self.municipality_field.clear()
        self.municipality_field.addItems(municipalities)

    def set_values_form(self, worker):
        worker = list(map(str, worker))
        self.nombre_field.setText(worker[1])
        self.segundo_nombre_field.setText(worker[2])
        self.apellido_field.setText(worker[3])
        self.segundo_apellido_field.setText(worker[4])
        self.ci_field.setText(worker[5])
        self.area_field.setCurrentText(worker[6])
        self.departamento_field.setCurrentText(worker[7])
        self.job_position_field.setCurrentText(worker[8])
        self.nivel_academico_field.setCurrentText(worker[9])
        self.genero_field.setCurrentText(worker[10])
        self.telefono_field.setText(worker[11])
        self.province_field.setCurrentText(worker[12])
        self.municipality_field.setCurrentText(worker[13])

    def reset_form(self):
        self.nombre_field.clear()
        self.segundo_nombre_field.clear()
        self.apellido_field.clear()
        self.segundo_apellido_field.clear()
        self.ci_field.clear()
        self.telefono_field.clear()


def validate_combobox(combo_box: QComboBox) -> bool:
    """
    Validate a QComboBox to ensure that an item has been selected.

    Parameters
    ----------
    combo_box : QComboBox
        The QComboBox to validate.

    Returns
    -------
    bool
        True if an item has been selected, False otherwise.
    """
    selected_index = combo_box.currentIndex()
    if selected_index == -1:
        QMessageBox.warning(None, "Warning", "You must select an item in the combo box.")
        return False
    return True


if __name__ == "__main__":
    app = QApplication([])
    window = AdminPanel()
    window.show()
    app.exec()
