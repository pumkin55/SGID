"""
    Module name: registry.py
    1. summary
    2. extended summary
    3. routine listings
    4. see also
    5. notes
    6. references
    7. examples
"""
import os
import sys
from datetime import datetime

import xlsxwriter
from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QIcon, Qt, QPixmap, QPainter, QFont
from PySide6.QtWidgets import (QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                               QFrame, QGridLayout, QPushButton, QHBoxLayout,
                               QSpacerItem, QSizePolicy, QApplication, QComboBox,
                               QHeaderView, QMessageBox, QFileDialog, QWidget,
                               QVBoxLayout, QCalendarWidget,QDialog
                               )
from sgid.models import data_access


def get_path_image(nombre_imagen):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = os.path.join(script_dir, '..', '..', 'resources')
    imagen_path = os.path.join(resources_dir, nombre_imagen)

    if os.path.exists(imagen_path):
        return imagen_path
    else:
        raise FileNotFoundError(f"No se encontró la imagen: {nombre_imagen}")


class SignatureSheet(QWidget):
    def __init__(self):
        super().__init__()
        # Crear QFrame para el área de filtrado
        self.worker_record = None
        filter_frame = QFrame()
        filter_frame.setObjectName("FilterFrame")  # Establecer un nombre de objeto para aplicar estilo CSS
        filter_frame.setFrameShape(QFrame.StyledPanel)  # Establecer el estilo del panel
        # Crear layout vertical para los widgets de filtrado
        filter_layout = QGridLayout(filter_frame)
        # Crear widgets de filtrado
        self.label_name = QLabel("Nombre:")
        self.qle_name = QLineEdit()
        self.qle_name.setFixedWidth(100)  # Establecer un ancho fijo para filter_name

        self.label_last_name = QLabel("Apellido:")
        self.qle_last_name = QLineEdit()
        self.qle_last_name.setFixedWidth(100)  # Establecer un ancho fijo para qle_last_name

        self.label_second_last_name = QLabel("2do Apellido:")
        self.qle_second_last_name = QLineEdit()
        self.qle_second_last_name.setFixedWidth(100)  # Establecer un ancho fijo para qle_second_last_name

        self.label_area = QLabel("\u00C1rea de Trabajo:")
        self.combo_box_area = QComboBox()
        
        self.combo_box_area.insertItem(0, "")
        self.combo_box_area.addItem("Human Resources")
        self.combo_box_area.addItem("Informatizaci\u00F3n")
        self.combo_box_area.addItem("Academic Affairs")
        self.combo_box_area.addItem("Administration")
        self.combo_box_area.addItem("Facilities Management")
        self.combo_box_area.addItem("Security")
        self.combo_box_area.currentIndexChanged.connect(self.update_departments)
        self.combo_box_area.setFixedWidth(140)
        self.label_department = QLabel("Departamento:")
        self.combo_box_department = QComboBox()
        self.combo_box_department.setFixedWidth(170) 

        self.departments = {
            "Human Resources": ["Recruitment", "Training and Development",
                                "Employee Relations",
                                "Compensation and Benefits",
                                "HR Information Systems"],
            "Informatizaci\u00F3n": ["Direcci\u00F3n de Informatizaci\u00F3n",
                                     "Seguridad Inform\u00E1tica",
                                     "Educaci\u00F3n a Distancia",
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

        self.update_departments()

        self.label_gender = QLabel("G\u00E9nero:")
        self.combo_box_gender = QComboBox()
        self.combo_box_gender.insertItem(0, "")
        self.combo_box_gender.addItem("Masculino")
        self.combo_box_gender.addItem("Femenino")

        self.label_province = QLabel("Provincia:")
        self.provinces_cuba = {
            "Pinar del Río": ["Pinar del Río", "San Juan y Martínez", "San Luis", "Consolación del Sur", "Guane",
                              "Minas de Matahambre", "Mantua"],
            "Artemisa": ["Artemisa", "Bahía Honda", "Candelaria", "Mariel", "San Cristóbal", "Guanajay", "Caimito",
                         "Bauta", "San Antonio de los Baños"],
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
        self.combo_box_province = QComboBox()
        self.combo_box_province.setFixedWidth(140)
        # Insert an empty string as the first item
        self.combo_box_province.insertItem(0, "")
        self.combo_box_province.addItems(self.provinces_cuba.keys())
        self.combo_box_province.currentIndexChanged.connect(self.update_municipalities)

        self.label_municipality = QLabel("Municipio:")
        self.combo_box_municipality = QComboBox()
        self.combo_box_municipality.setFixedWidth(170) 

        self.update_municipalities()

        self.search_button = QPushButton(self)
        self.search_button.setToolTip(str("Buscar"))
        self.search_button.setIcon(QIcon(get_path_image("search.svg")))
        self.search_button.setFixedSize(100, 25)
        self.search_button.setStyleSheet("background-color: lightblue;")
        filter_layout.addWidget(self.search_button, 7, 6, alignment=Qt.AlignLeft)

        self.refresh_button = QPushButton(self)
        self.refresh_button.setToolTip(str("Actualizar tabla"))
        self.refresh_button.setIcon(QIcon(get_path_image("arrow-clockwise.svg")))
        self.refresh_button.setFixedSize(100, 25)
        self.refresh_button.setStyleSheet("background-color: lightgrey;")
        filter_layout.addWidget(self.refresh_button, 7, 7, )

        filter_layout.addWidget(self.label_name, 0, 0, alignment=Qt.AlignLeft)
        filter_layout.addWidget(self.qle_name, 0, 1, alignment=Qt.AlignLeft)

        filter_layout.addWidget(self.label_last_name, 0, 2, alignment=Qt.AlignLeft)
        filter_layout.addWidget(self.qle_last_name, 0, 3, alignment=Qt.AlignLeft)

        filter_layout.addWidget(self.label_second_last_name, 0, 4, alignment=Qt.AlignLeft)
        filter_layout.addWidget(self.qle_second_last_name, 0, 5, alignment=Qt.AlignLeft)

        filter_layout.addWidget(self.label_area, 4, 0, alignment=Qt.AlignLeft)
        filter_layout.addWidget(self.combo_box_area, 4, 1, alignment=Qt.AlignLeft)

        filter_layout.addWidget(self.label_department, 4, 2, alignment=Qt.AlignLeft)
        filter_layout.addWidget(self.combo_box_department, 4, 3, alignment=Qt.AlignLeft)

        filter_layout.addWidget(self.label_gender, 4, 4, alignment=Qt.AlignLeft)
        filter_layout.addWidget(self.combo_box_gender, 4, 5, alignment=Qt.AlignLeft)

        filter_layout.addWidget(self.label_province, 5, 0, alignment=Qt.AlignLeft)
        filter_layout.addWidget(self.combo_box_province, 5, 1, alignment=Qt.AlignLeft)

        filter_layout.addWidget(self.label_municipality, 5, 2, alignment=Qt.AlignLeft)
        filter_layout.addWidget(self.combo_box_municipality, 5, 3, alignment=Qt.AlignLeft)

        self.table = QTableWidget()

        columnas = ["Nombre", "2do Nombre", "Apellido", "2do Apellido", "Año",
                    "% Ausencias", "Área de Trabajo", "Departamento", "Cargo"]

        self.table.setColumnCount(len(columnas))

        self.table.setHorizontalHeaderLabels(columnas)

        self.table.horizontalHeader().setStyleSheet("""
                    background-color: rgb(200, 200, 200);
                    color: black;
                    font-weight: bold;
                """)

        for column in range(self.table.columnCount()):
            self.table.resizeColumnToContents(column)

        # Ajustar el tamaño de la encabezado horizontal para ocupar solo el espacio necesario
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # Establecer las dos últimas columnas para ocupar el espacio restante de forma uniforme
        last_column = self.table.columnCount() - 1
        department_column = last_column - 1
        area_column = last_column - 2
        name_column = last_column - 8
        self.table.horizontalHeader().setSectionResizeMode(name_column, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(area_column, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(department_column, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(last_column, QHeaderView.Stretch)
        # Crear layout vertical para la sección de la tabla
        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table)
        # Cuando agregas un QSpacerItem flexible al principio y al final del QHBoxLayout, estos elementos
        # actúan como "resortes" que empujan los botones hacia el centro del diseño.
        # La manera en que esto ocurre es la siguiente:
        # Al agregar el primer QSpacerItem al principio del QHBoxLayout, este espacio flexible intenta expandirse para
        # llenar cualquier espacio adicional. Como resultado, empuja a los botones hacia la derecha, ya que el espacio
        # flexible se expande ocupando ese espacio adicional.
        # Luego, cuando agregas el segundo QSpacerItem al final del QHBoxLayout, este espacio flexible también intenta
        # expandirse para llenar cualquier espacio adicional. Ahora hay espacio adicional a la izquierda de los botones,
        # ya que el primer QSpacerItem ha empujado los botones hacia la derecha.
        # Como ambos QSpacerItem son flexibles y están configurados para expandirse equitativamente en la dirección
        # horizontal, se produce la expansión simétrica y centrada. Ambos QSpacerItem se expanden desde los extremos
        # hacia el centro, empujando los botones hacia el centro del QHBoxLayout.
        btn_second_layout = QHBoxLayout()
        self.btn_xlsx = QPushButton(self)  # Create a QPushButton instance and set 'self' as its parent
        self.btn_xlsx.setToolTip(str("Exportar tabla .xlsx"))
        # Create a QIcon instance with the path to the SVG image
        icon = QIcon(get_path_image("filetype-xlsx.svg"))
        # Create a QPixmap from the SVG image with the desired size for the button
        pixmap = icon.pixmap(QSize(55, 20))
        # Set the QPixmap as the icon for the button
        self.btn_xlsx.setIcon(QIcon(pixmap))
        # Set the size of the button's icon to match the size of the QPixmap
        self.btn_xlsx.setIconSize(pixmap.size())
        # Set the fixed size of the button to 100x100 pixels
        self.btn_xlsx.setFixedSize(70, 30)
        # Set the background color of the button using CSS styling
        self.btn_xlsx.setStyleSheet(
            "background-color: lightgreen;")
        # Add the button to the layout, aligned to the right
        btn_second_layout.addWidget(self.btn_xlsx, alignment=Qt.AlignRight)
        # Crear layout principal de la ventana
        layout = QVBoxLayout(self)
        layout.addWidget(filter_frame)
        layout.addLayout(table_layout)
        layout.addLayout(btn_second_layout)
        filter_frame.setStyleSheet("""
                    QFrame#FilterFrame {
                        border: 2px solid #000000;  /* Establecer un borde de 2 píxeles de ancho en color negro */
                        border-radius: 5px;  /* Redondear las esquinas del borde */
                        background-color: #F0F0F0;  /* Establecer un color de fondo para resaltar el área */
                        margin: 10px;  /* Agregar un margen para separar el área del borde de la ventana */
                    }
                """)

        self.w = data_access.get_all_workers()
        # Events
        # Conexión de la señal cellClicked a un método
        self.table.cellClicked.connect(self.show_worker_records)
        self.show_all_table_values()
        self.refresh_button.clicked.connect(self.show_all_table_values)
        self.search_button.clicked.connect(self.filter_data_in_the_interface)
        self.btn_xlsx.clicked.connect(self.export_to_xlsx)

    def show_worker_records(self, row):
        """Show the WorkerRecords window."""
        # Define the custom keys for the selected items
        custom_keys = ['name', 'middle_name', 'last_name', 'second_last_name']
        # Create a dictionary of selected items using custom keys and table values
        selected_items = {key: self.table.item(row, col).text()
                          for col, key in enumerate(custom_keys)}
        # Retrieve the records by year based on the selected items
        w_id, records = data_access.show_records_by_year(selected_items)
        print(records)
        result = data_access.calculate_absence_percentage(w_id)
        # Create a list to store the sheet IDs associated with the worker
        sheet_ids = [dic['sheet_id'] for data in records.values() for dic in data if 'sheet_id' in dic]
        # Create an instance of the WorkerRecords window with the sheet IDs and selected items
        self.worker_record = WorkerRecords(sheet_ids, selected_items, result)
        # Show the WorkerRecords window
        if records == {}:
            QMessageBox.warning(None, "Warning", "El trabajador seleccionado no presenta registros.")
        else:
            self.worker_record.show()

    def update_departments(self):
        selected_area = self.combo_box_area.currentText()
        try:
            selected_departments = self.departments.get(selected_area, [])
        except KeyError:
            selected_departments = []

        self.combo_box_department.clear()
        self.combo_box_department.addItems(selected_departments)
        self.combo_box_department.setEnabled(bool(selected_departments))

    def update_municipalities(self):
        selected_province = self.combo_box_province.currentText()
        try:
            municipalities = self.provinces_cuba[selected_province]
        except KeyError:
            municipalities = []
        self.combo_box_municipality.clear()
        self.combo_box_municipality.addItems(municipalities)
        self.combo_box_municipality.setEnabled(bool(selected_province))

    def show_all_table_values(self):
        self.w = data_access.get_all_workers()
        self.show_values_in_table(self.w)

    def filter_data_in_the_interface(self):
        filter_params = {
            'name': self.qle_name.text(),
            'last_name': self.qle_last_name.text(),
            'second_last_name': self.qle_second_last_name.text(),
            'work_area': self.combo_box_area.currentText(),
            'department': self.combo_box_department.currentText(),
            'province': self.combo_box_province.currentText(),
            'municipality': self.combo_box_municipality.currentText(),
            'gender': self.combo_box_gender.currentText(),
            #'gender': gender,
        }
        result = data_access.filter_worker_records(**filter_params)
        self.show_values_in_table(result)

    def show_values_in_table(self, w: dict):
        all_records = []
        for w_id, w_data in w.items():
            signature_sheets = data_access.filter_signature_sheets_records(w_id)
            result = data_access.calculate_absence_percentage(w_id)

            if signature_sheets:
                tmp, worker_signature_sheets_by_year = data_access.show_records_by_year({'id': w_id})
                for k, v in worker_signature_sheets_by_year.items():
                    for sheet_data in v:
                        for n, m in sheet_data.items():
                            if n == 'date':
                                date_obj = m
                                year = date_obj.year
                                record = create_table_record(w_data, year, result[1])
                                all_records.append(record)
                        break
            else:
                record = create_table_record(w_data, "", " ")
                all_records.append(record)

        self.table.setRowCount(len(all_records))
        for row, record in enumerate(all_records):
            for col, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignVCenter)
                self.table.setItem(row, col, item)

    def export_to_xlsx(self):
        months = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }
        # diccionario para mostrar todos los datos
        dicc = {}
        # diccionario con la informacion especifica de las ausencias de cada usuario
        dict_data = {}

        for w_id, w_data in self.w.items():
            result = data_access.calculate_absence_percentage(w_id)
            dict_data[w_id] = {
                'month_absences_percentage': result[0],
                'month_workdays_count': result[3],
                'month_absences_count': result[2],
            }
            dicc[w_id] = {
                'name': w_data['name'],
                'middle_name': w_data['middle_name'],
                'last_name': w_data['last_name'],
                'second_last_name': w_data['second_last_name'],
                'year': 2024,
                'year_absences': result[1],
                'month': dict_data[w_id],
                'work_area': w_data['work_area'],
                'department': w_data['department'],
                'job_position': w_data['job_position'],
            }

        for k, v in dicc.items():
            print(k, v)

        global folder_selected

        try:
            # Usar el diálogo de selección de directorio para obtener el directorio de destino
            folder_dialog = QFileDialog()
            folder_dialog.setFileMode(QFileDialog.Directory)
            folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)
            folder_selected = folder_dialog.getExistingDirectory(self, "Seleccionar directorio")
        except:
            print('Hubo un problema a la hora de guardar el archivo')

        selected_month = "January"  # Mes seleccionado (puedes cambiarlo según tus necesidades)

        if folder_selected:
            current_date = QDate.currentDate().toString("yyyy_MM_dd")
            filename = f"{current_date}_Registro_de_Asistencia_Laboral.xlsx"
            filepath = os.path.join(folder_selected, filename)

            workbook = xlsxwriter.Workbook(filepath)

            header_widths = [10, 12, 10, 14, 8, 10, 10, 12, 12, 12, 25, 25, 25]

            title_format = workbook.add_format({
                'bold': True,
                'font_size': 18,
                'bg_color': '#D3D3D3',
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
            })

            header_format = workbook.add_format({
                'bold': True,
                'bg_color': 'yellow',
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
            })

            content_format = workbook.add_format({
                'align': 'center',
                'border': 1,
            })

            for month, month_number in months.items():
                worksheet_month = workbook.add_worksheet(month)

                worksheet_month.merge_range('D2:P3', 'Registro Anual', title_format)

                headers = ['Nombre', '2do Nombre', 'Apellido', '2do Apellido', 'Año', '% Ausencias Anual', 'Mes',
                           '% Ausencias',
                           'Asistencias', 'Ausencias', 'Área', 'Departamento', 'Cargo']

                for col, header in enumerate(headers, start=3):
                    worksheet_month.set_column(col, col, header_widths[col - 3])
                    worksheet_month.write(3, col, header, header_format)

                row = 4  # Fila inicial para escribir los datos

                for user_id, user_data in dicc.items():
                    user_month_data = user_data['month']
                    user_name = user_data['name']
                    user_middle_name = user_data['middle_name']
                    user_last_name = user_data['last_name']
                    user_second_last_name = user_data['second_last_name']
                    user_year = user_data['year']
                    user_year_absences = user_data['year_absences']
                    user_work_area = user_data['work_area']
                    user_department = user_data['department']
                    user_job_position = user_data['job_position']

                    worksheet_month.write(row, 3, user_name, content_format)
                    worksheet_month.write(row, 4, user_middle_name, content_format)
                    worksheet_month.write(row, 5, user_last_name, content_format)
                    worksheet_month.write(row, 6, user_second_last_name, content_format)
                    worksheet_month.write(row, 7, user_year, content_format)
                    worksheet_month.write(row, 8, user_year_absences, content_format)
                    worksheet_month.write(row, 9, month, content_format)
                    worksheet_month.write(row, 10, user_month_data['month_absences_percentage'].get(month, ''),
                                          content_format)
                    worksheet_month.write(row, 11, user_month_data['month_workdays_count'].get(month, ''),
                                          content_format)
                    worksheet_month.write(row, 12, user_month_data['month_absences_count'].get(month, ''),
                                          content_format)
                    worksheet_month.write(row, 13, user_work_area, content_format)
                    worksheet_month.write(row, 14, user_department, content_format)
                    worksheet_month.write(row, 15, user_job_position, content_format)

                    row += 1

            workbook.close()
        pass


class WorkerRecords(QDialog):
    def __init__(self, signature_id: list, selected_items: dict, result: tuple):
        super().__init__()
        self.setWindowTitle("Registro del Trabajador")
        self.setModal(True)
        self.setFixedWidth(980)
        self.setFixedHeight(500)
        self.month_percentage = result[0]
        self.month_absences_count = result[2]
        self.month_workdays_count = result[3]
        # Create the necessary UI elements
        self.calendar_widget = CustomCalendarWidget(signature_id, selected_items)
        self.leyend_widget = LegendWidget()
        # 1st Area: Worker name (0,0)
        self.label_name = QLabel(self)
        # Mostrar datos en la ventana auxiliar del trabajador
        full_name = str(
            selected_items['name'] + " " + selected_items['middle_name'] + " " + selected_items[
                'last_name'] + " " + selected_items['second_last_name'])
        self.label_name.setText(full_name)
        # Set the font style
        font = QFont("Verdana", 18)
        self.label_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_name.setFont(font)
        # 2 Area: QLabel Foto (0,1)
        label_photo_title = QLabel(self)
        label_photo_title.setText("Foto")
        label_photo_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Set the font style
        font = QFont("Verdana", 18)
        label_photo_title.setFont(font)
        # 3 Area: CalendarWidget (1,0)
        self.calendar_widget.setFixedWidth(700)
        self.calendar_widget.setFixedHeight(300)
        # 4 Area: Worker's Photo (1,1)
        self.label_worker_photo = QLabel(self)
        photo_path = get_path_image("unknow.png")
        pixmap = QPixmap(photo_path).scaled(250, 200, Qt.AspectRatioMode.KeepAspectRatio)
        self.label_worker_photo.setPixmap(pixmap)
        self.label_worker_photo.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align the photo to the center
        # 5 Area: QLabel (2,0)
        self.label_leyenda = QLabel(self)
        self.label_leyenda.setText("Leyenda")
        self.boton_cerrar = QPushButton(self, text="Cerrar")
        self.boton_cerrar.setFixedSize(100, 30)  # Establecemos el tamaño del botón
        self.boton_cerrar.setStyleSheet("background-color: lightgray;")
        # Create a QGridLayout to hold the UI elements
        layout = QGridLayout()
        layout.addWidget(self.label_name, 0, 0)
        # rowsapn and column span --> si es 1 se ocupa el mismo widget,
        # si es mayor que 1 se ocupa el widget y el resto de los espacios
        layout.addWidget(self.calendar_widget, 1, 0, 1, 2)
        layout.addWidget(label_photo_title, 0, 2, 1, 2)
        layout.addWidget(self.label_worker_photo, 1, 2, 1, 2)
        layout.addWidget(self.label_leyenda, 2, 0, 1, 2)
        layout.addWidget(self.leyend_widget, 3, 0, 1, 2)
        layout.addWidget(self.boton_cerrar, 3, 3, 1, 2)
        self.setLayout(layout)
        # Events
        # Connect the currentPageChanged signal of the calendar widget to the handle_page_changed slot
        self.update_legend_widget_labels()
        self.calendar_widget.currentPageChanged.connect(self.update_legend_widget_labels)
        self.boton_cerrar.clicked.connect(self.close)

    def update_legend_widget_labels(self):
        current_month = self.return_current_month()
        for k2, v2 in self.month_percentage.items():
            if k2 == current_month:
                self.leyend_widget.update_labels(
                    self.month_workdays_count[current_month],
                    self.month_absences_count[current_month],
                    v2
                )

    def return_current_month(self):
        current_month_number = self.calendar_widget.monthShown()
        current_month_name = get_month_name(current_month_number)
        return current_month_name


class CustomCalendarWidget(QCalendarWidget):
    def __init__(self, signature_ids, filters):
        super().__init__()
        self.lista = data_access.signature_sheets_without_absences(signature_ids)
        w_id, self.w_signature = data_access.show_records_by_year(filters)
        self.result = []
        for key, values in self.w_signature.items():
            for record in values:
                self.result.append({'sheet_id': record['sheet_id'], 'date': record['date']})

    def paintCell(self, painter: QPainter, rect, date):
        painter.save()
        # Check if it's a Saturday or Sunday
        if date.dayOfWeek() == 6 or date.dayOfWeek() == 7:
            # No drawing needed for Saturdays and Sundays
            pass
        else:
            # Check if the date has a corresponding sheet_id in self.result
            date_str = date.toString("yyyy-MM-dd")
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            matching_dates = [record['date'] for record in self.result if record['sheet_id'] in self.lista]
            if date_obj in matching_dates:
                pixmap = QPixmap(get_path_image("accept.png"))
            else:
                pixmap = QPixmap(get_path_image("remove.png"))
            # Resize the pixmap to 15x15 pixels
            pixmap = pixmap.scaled(15, 15)
            # Calculate the position to draw the image
            image_x = rect.left() + (rect.width() - pixmap.width()) // 2
            image_y = rect.top() + (rect.height() - pixmap.height()) // 2
            # Draw the image in the center of the cell
            painter.drawPixmap(image_x, image_y, pixmap)
            # Set the font for drawing the cell text
            font = QFont()
            font.setPointSize(8)
            painter.setFont(font)
            # Calculate the position to draw the cell text
            text_x = rect.left() + 2
            text_y = rect.top() + 12
            # Draw the cell text
            painter.drawText(text_x, text_y, str(date.day()))
        painter.restore()


class LegendWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Leyenda")
        self.square1 = QLabel(self)
        photo_path = get_path_image("accept.png")
        pixmap = QPixmap(photo_path)
        pixmap = pixmap.scaled(20, 20)
        self.square1.setPixmap(pixmap)
        self.square1.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Align the photo to the center
        self.square2 = QLabel(self)
        photo_path = get_path_image("remove.png")
        pixmap = QPixmap(photo_path)
        pixmap = pixmap.scaled(20, 20)
        self.square2.setPixmap(pixmap)
        self.square2.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Align the photo to the center
        self.label1 = QLabel("Asistencias: ")
        self.label2 = QLabel("Ausencias: ")
        self.label3 = QLabel(f"%     Porct. de Ausencias: ", )
        # Crear el diseño de cuadrícula y agregar los elementos
        layout = QGridLayout()
        layout.addWidget(self.square1, 0, 0, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.label1, 0, 1, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.square2, 1, 0, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.label2, 1, 1, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.label3, 2, 0, 1, 10,
                         alignment=Qt.AlignmentFlag.AlignTop)  # Span 2 columnas para el QLabel
        # Agregar espaciador vertical al final del diseño
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer, 3, 0, 1, 2)
        # Establecer la política de tamaño de los elementos
        self.square1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.label1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.square2.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.label2.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.label3.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setLayout(layout)

    def update_labels(self, value1, value2, value3):
        self.label1.setText(f"Asistencias: {value1}")
        self.label2.setText(f"Ausencias: {value2}")
        self.label3.setText(f"%     Porct. de Ausencias: {value3}")


def get_month_name(month_number):
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    return month_names[month_number - 1]


def create_table_record(w_data: dict, year,
                        year_percentage):
    record = [
        w_data['name'],
        w_data['middle_name'],
        w_data['last_name'],
        w_data['second_last_name'],
        year,
        year_percentage,
        w_data['work_area'],
        w_data['department'],
        w_data['job_position'],
    ]
    return record


if __name__ == "__main__":
    app = QApplication(sys.argv)
    legend_widget = SignatureSheet()
    legend_widget.show()
    sys.exit(app.exec())
