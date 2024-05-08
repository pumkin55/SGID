"""
    Module name: daily_authentication.py
    1. summary
    2. extended summary
    3. routine listings
    4. see also
    5. notes
    6. references
    7. examples
"""
import pickle
import re
import sys
import time
from datetime import date
from datetime import datetime
from pathlib import Path

import cv2
from PySide6.QtCore import QTimer, QRegularExpression
from PySide6.QtGui import Qt, QImage, QPixmap, QRegularExpressionValidator
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                               QGridLayout, QHBoxLayout, QSizePolicy,
                               QMessageBox, QApplication
                               )
from pyzbar import pyzbar

from sgid.models import data_access

# Variable global para realizar el seguimiento de si la función ya se ejecutó hoy
already_executed = False


def qr_to_list(decoded_objects):
    """Devuelve la informacion del QR en forma de lista"""
    # data
    data = []
    for obj in decoded_objects:
        # Decodificar el contenido del código de barras en formato UTF-8
        text = obj.data.decode('utf-8')
        text = str(text)
        print(text)
        data = text.split()

    return data


def eliminar_campos_none(texto):
    """Elimina los campos None y establece un texto vacío"""
    if texto is None or texto.lower() == "none":
        return ""
    return texto


def obtener_hora():
    """Obtiene la hora actual"""
    hora_actual = datetime.now().strftime("%H:%M:%S")
    return hora_actual


def get_data_worker(ci: str) -> tuple:
    """Me devuelve el user_id y user_data de una entidad worker con ci = ci"""
    result = data_access.get_fields_by_ci(ci)
    if result:
        v = [
            result['name'],  # name
            result['middle_name'],  # middle name
            result['last_name'],  # last name
            result['second_last_name'],  # second last name
            result['work_area'],  # work_area
            None,  # entry time
            None,  # departure time
        ]
        return result['id'], v
    else:
        return None, None


def loading_animation():
    animation = "|/-\\"
    dots = ""

    while True:
        for char in animation:
            sys.stdout.write("\rLoading " + dots + char)
            sys.stdout.flush()
            time.sleep(0.1)

        if len(dots) < 5:
            dots += "."
        else:
            dots = ""


def check_seven_am():
    global already_executed

    if not already_executed:
        current_time = datetime.now().time()
        if current_time.hour == 16 and current_time.minute >= 36:
            worker_list_absences = data_access.get_ids_not_in_pkl()
            for k in worker_list_absences:
                s_id = data_access.create_signature_sheet(k, obtener_hora(), obtener_hora(),
                                                          datetime.now().date(), '',
                                                          '')
                data_access.create_absence(s_id, datetime.now().date(), 'Enfermedad')

            already_executed = True
    else:
        pass


class MainDaily(QWidget):

    def __init__(self, campos: dict):
        super().__init__()

        self.setWindowTitle("Sistema de autenticación")

        # Inicializar variables
        self.scan_enabled = True
        # Variable para almacenar el CI escaneado
        self.scanned_ci = None
        # Inicializar variables
        self.process_label = QLabel("Procesando.../", self)
        self.process_label.setFixedSize(350, 350)
        self.process_label.setAlignment(Qt.AlignCenter)
        self.process_label.setStyleSheet("color: green; font-size: 24px")
        self.process_label.hide()
        self.scan_enabled = True
        self.animation_index = 0
        self.animation_chars = "|/-\\"

        self.not_camera_label = QLabel("No se reconoce cámara", self)
        self.not_camera_label.setFixedSize(350, 350)
        self.not_camera_label.setAlignment(Qt.AlignCenter)
        self.not_camera_label.setStyleSheet("color: gray; font-size: 24px")
        self.not_camera_label.hide()

        self.video_feed = QLabel(self)
        self.video_feed.setFixedSize(350, 350)  # Establecer tamaño fijo del cuadro de video
        self.timer = QTimer(self)
        self.capture = cv2.VideoCapture(0)

        if not self.capture.isOpened():
            self.capture = None
            print("Cannot open camera", self.capture)
            # exit()
        else:
            pass

        self.nombre = str
        self.apellido = str
        # Varialbe campos pasado por parametros
        self.campos = campos

        # Conectar eventos
        self.timer.timeout.connect(self.show_scan)

        # Configurar diseño de ventana
        layout = QGridLayout(self)
        layout.addWidget(self.video_feed, 0, 0, 1, 1, Qt.AlignRight)
        layout.addWidget(self.process_label, 0, 0, 1, 1, Qt.AlignRight)
        layout.addWidget(self.not_camera_label, 0, 0, 1, 1, Qt.AlignRight)

        input_container = QWidget()  # Contenedor para el QHBoxLayout
        input_layout = QHBoxLayout(input_container)
        input_layout.addWidget(QLabel("Introducir CI:"))
        self.ci_input = QLineEdit()
        self.ci_input.setMaxLength(11)
        # Expresión regular para permitir solo números del 0 al 9
        regex = QRegularExpression("^[0-9]{11}$")
        # Validador de expresión regular
        validator = QRegularExpressionValidator(regex)
        # Establecer el validador en el campo de texto
        self.ci_input.setValidator(validator)

        input_layout.addWidget(self.ci_input)
        input_container.setFixedHeight(input_layout.sizeHint().height())  # Establecer altura fija del contenedor
        input_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Establecer política de tamaño fija
        layout.addWidget(input_container, 1, 0, 1, 1, Qt.AlignRight)  # Alinear a la izquierda

        second_input_container = QWidget()  # Contenedor para el QVBoxLayout
        v1_layout = QVBoxLayout(second_input_container)

        v1_layout.addWidget(QLabel("Nombre:"))
        v1_layout.addWidget(QLabel("Apellidos:"))
        v1_layout.addWidget(QLabel("Hora de Entrada:"))
        v1_layout.addWidget(QLabel("Hora de Salida:"))

        third_input_container = QWidget()  # Contenedor para el segundo QVBoxLayout
        v2_layout = QVBoxLayout(third_input_container)

        self.nombre_output = QLabel()
        self.apellido_output = QLabel()
        self.hora_entrada_output = QLabel()
        self.hora_salida_output = QLabel()

        v2_layout.addWidget(self.nombre_output)
        v2_layout.addWidget(self.apellido_output)
        v2_layout.addWidget(self.hora_entrada_output)
        v2_layout.addWidget(self.hora_salida_output)

        output_container = QWidget()  # Contenedor para el QHBoxLayout
        output_layout = QHBoxLayout(output_container)

        output_layout.addWidget(second_input_container)
        output_layout.addWidget(third_input_container, Qt.AlignLeft)

        # layout.addWidget(second_input_container, 0, 1, 1, 1, Qt.AlignTop)  # Alinear a la izquierda
        # layout.addLayout(v_layout, 0, 1, 1, 1)

        layout.addWidget(output_container, 0, 1, 1, 1, Qt.AlignTop | Qt.AlignLeft)  # Alinear a la izquierda

        self.setLayout(layout)

        # Configurar políticas de tamaño para los widgets
        self.video_feed.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Connect the Enter key press event of ci_input to the ci_input_user method
        self.ci_input.returnPressed.connect(self.main_method_ci_input_user)
        self.ci_input.returnPressed.connect(self.clear_input)

        self.timer2 = QTimer(self)
        # para verificar la hora automaticamente para registrar de forma automatica las ausencias
        self.timer3 = QTimer(self)

        # Save the authenticated users data to file
        self.timer3.timeout.connect(check_seven_am)

        # Iniciar temporizador para mostrar el video
        self.timer3.start(10000)

        # Save the authenticated users data to file
        self.timer2.timeout.connect(self.save_registered_users)

        # Iniciar temporizador para mostrar el video
        self.timer2.start(3000)

        # Iniciar temporizador para mostrar el video
        self.timer.start(30)

    def show_scan(self):
        if self.capture is None:
            self.show_not_camera()
        else:
            # Este código utiliza el objeto self.capture para leer un fotograma del video capturado.
            # Devuelve dos valores:
            # ret, que indica si se pudo leer correctamente el fotograma, y frame, que contiene el fotograma capturado.
            ret, frame = self.capture.read()

            # Verifica si se pudo leer correctamente el fotograma.
            # Si es así, continúa ejecutando el código dentro del bloque if.
            if ret:
                # Convertir el frame a formato RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Crear un objeto QImage a partir del frame RGB
                image = QImage(frame_rgb, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)
                # Mostrar la imagen en el cuadro de video
                self.video_feed.setPixmap(QPixmap.fromImage(image))

                # Convierte el fotograma capturado a escala de grises utilizando cv2.cvtColor().
                # Esto se hace para poder decodificar los códigos de barras presentes en el fotograma.
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Decodificar los códigos de barras presentes en el frame en escala de grises
                decoded_objects = pyzbar.decode(gray)
                #
                data = qr_to_list(decoded_objects)

                if not data:
                    pass
                else:
                    if self.scan_enabled:
                        for obj in data:
                            if obj.startswith("CI"):
                                self.scan_enabled = False
                                self.scanned_ci = obj[3:]
                                self.main_method_ci_input_user()
                                # aqui hago de nuevo None a la varialbe para limpiar el registro para los nuevos valores
                                self.scanned_ci = None
                                QTimer.singleShot(2000, self.enable_scan)  # Pausa de 3 segundos
                                self.show_loading_animation()
        pass

    def show_not_camera(self):
        self.video_feed.hide()
        self.not_camera_label.show()
        pass

    def show_loading_animation(self):
        self.video_feed.hide()
        self.process_label.show()
        self.timer.timeout.connect(self.update_loading_label)
        self.timer.start(100)

    def update_loading_label(self):
        self.process_label.setText("Loading " + self.animation_chars[self.animation_index])
        self.animation_index = (self.animation_index + 1) % len(self.animation_chars)

    def enable_scan(self):
        self.scan_enabled = True
        self.reset_loading_animation()

    def reset_loading_animation(self):
        self.process_label.hide()
        self.video_feed.show()

    def show_data(self, user_data: list) -> None:
        """Muestra la informacion del QR en la GUI"""

        if user_data == {}:
            pass
        else:
            first_name = user_data[0]
            second_name = user_data[1]
            name = first_name + " " + second_name

            last_name = user_data[2]
            second_last_name = user_data[3]
            full_last_name = last_name + " " + second_last_name

            hora_llegada = eliminar_campos_none(user_data[5])
            hora_salida = eliminar_campos_none(user_data[6])

            self.nombre_output.setText(name)
            self.apellido_output.setText(full_last_name)
            self.hora_entrada_output.setText(hora_llegada)
            self.hora_salida_output.setText(hora_salida)
        pass

    def check_ci_input_user(self, ci) -> bool:
        """Valida el ci introducido por el usuario"""
        regex = re.compile(r'^[0-9]{11}$')

        if ci == '':
            return False

        if not regex.match(ci):
            print("Introduzca un valor válido", ci)
            QMessageBox.warning(self, "Advertencia", "Introduzca un valor válido.")
            return False

        return True

    def is_registered(self, user_id: str, user_data: list) -> bool:
        """
        Este método se encarga de verificar si un usuario se encuentra registrado.
        Si el usuario está registrado, actualiza los valores de hora de entrada y salida.
        Muestra un mensaje de error en caso de que el usuario ya se haya registrado.
        """
        try:
            if self.campos[user_id][6] is not None:  # El usuario ya se registró en entrada y salida
                mensaje_error = (
                    'Ya se registró y autenticó en el día. Hable con su supervisor o anótese en una libreta si '
                    'tuvo que salir por algún motivo y volver a su puesto. Este sistema solo reconoce una '
                    'entrada y una salida por persona. Disculpe las molestias. Gracias!')
                print(mensaje_error)
                QMessageBox.warning(self, "Advertencia", mensaje_error)
                return True

            if self.campos[user_id][5] is not None:  # Si el usuario se encuentra registrado
                print('El usuario se encuentra registrado')
                self.campos[user_id][6] = obtener_hora()
                print('User', user_id, '. Departure time --> ', self.campos[user_id][5])
                return True

        except KeyError:
            print('Se ha manejado la excepción KeyError')

        # El usuario no se encuentra registrado
        self.campos[user_id] = user_data
        print('Se acaba de registrar el usuario', user_id)

        self.campos[user_id][5] = obtener_hora()
        print('User', user_id, '. Entry time --> ', self.campos[user_id][4])
        return False

    def main_method_ci_input_user(self):
        """This method had all the main process"""

        ci = self.scanned_ci if self.scanned_ci is not None else self.ci_input.text()
        signature_date = date.today()

        if self.check_ci_input_user(ci):
            if data_access.is_user_in_worker(ci):
                user_id, user_data = get_data_worker(ci)

                if self.is_registered(user_id, user_data):
                    entry_time = self.campos[user_id][5]
                    exit_time = self.campos[user_id][6]
                    data_access.create_signature_sheet(user_id, entry_time, exit_time, signature_date,
                                                       "Oficina",
                                                       "Nota genérica")
                self.show_data(user_data=self.campos[user_id])
            else:
                text = f"El usuario {ci} no está registrado en el sistema."
                QMessageBox.warning(self, "Advertencia", text)

    def clear_input(self) -> None:
        self.ci_input.clear()

    def save_registered_users(self) -> None:
        """Guardar los datos de usuarios autenticados en un archivo"""
        try:
            with open('usuarios_autenticados.pkl', 'wb') as archivo:
                pickle.dump(self.campos, archivo)
            # print("Datos guardados exitosamente.")
        except Exception:
            print("Ha ocurrido un problema al guardar los datos de usuarios autenticados.")

    def get_campos(self):
        """Devuelve el valor actual de la variable campos"""
        return self.campos

    def clear_campos(self):
        self.campos = {}


if __name__ == "__main__":
    app = QApplication(sys.argv)
    campos = {}
    legend_widget = MainDaily(campos)
    legend_widget.show()

    sys.exit(app.exec())
