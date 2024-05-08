"""
Module: data_access.py
"""

import os
import pickle
from datetime import date, datetime

from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from .models import Worker, Absence, SignatureSheet

# Get the absolute path of the current module's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

#
hora_actual = datetime.now().strftime("%H:%M:%S")

try:
    # Concatenate the database file path
    db_path = os.path.join(current_dir, 'database.db')
    print('db_path: ', db_path)
    # Create an instance of the SQLAlchemy engine
    engine = create_engine(f'sqlite:///{db_path}', echo=True)

    # Create a session class using the engine
    Session = sessionmaker(bind=engine)

    # Create a scoped session
    session = Session()
except SQLAlchemyError as e:
    # Handle the exception
    print(f"An error occurred during the database connection: {str(e)}")


def is_user_in_worker(ci: str) -> bool:
    """
    Checks if a user with the given CI exists in the database.

    Args:
        ci (str): The CI of the user to check.

    Returns:
        bool: True if the user exists, False otherwise.
    """

    # Perform the query to search for the CI in the Worker table
    worker = session.query(Worker).filter_by(ci=ci).first()

    # Close the session and the database connection
    session.close()

    if worker:
        print('The user is in the worker\'s table')
        return True
    else:
        print('The user is not in the worker\'s table')
        return False

def is_user_phone_in_worker(phone: str) -> bool:
    # Perform the query to search for the CI in the Worker table
    worker = session.query(Worker).filter_by(phone=phone).first()
    # Close the session and the database connection
    session.close()
    if worker:
        print('The user phone is in the worker\'s table')
        return True
    else:
        print('The user phone is not in the worker\'s table')
        return False

def get_fields_by_ci(ci: str) -> dict:
    """Gets all fields from the table that match the provided CI and stores them in a dictionary"""
    try:
        # Perform the query to retrieve the fields
        workers = session.query(Worker).filter(Worker.ci == ci).all()

        field_dict = {}  # Initialize the field dictionary as empty

        if workers:
            # Assuming you only expect one worker with the given CI
            worker = workers[0]  
            field_dict['id'] = worker.id
            field_dict['name'] = worker.name
            field_dict['middle_name'] = worker.middle_name
            field_dict['last_name'] = worker.last_name
            field_dict['second_last_name'] = worker.second_last_name
            field_dict['ci'] = worker.ci
            field_dict['work_area'] = worker.work_area
            field_dict['department'] = worker.department
            field_dict['job_position'] = worker.job_position
            field_dict['academic_degree'] = worker.academic_degree
            field_dict['gender'] = worker.gender
            field_dict['phone'] = worker.phone
            field_dict['province'] = worker.province
            field_dict['municipality'] = worker.municipality

        return field_dict
    except SQLAlchemyError as e:
        # Handle the error
        print(f"An error occurred while retrieving fields from the database: {str(e)}")
        return {}
    except NameError as e:
        print(f"An error occurred while accessing fields from the database: {str(e)}")
        print(f"ci value: {str(ci)}")
        return {}


def get_all_workers():
    """Return a list of a list"""
    workers = session.query(Worker).all()
    results = {}
    for worker in workers:
        worker_dict = {
            'id': worker.id,
            "name": worker.name,
            "middle_name": worker.middle_name,
            "last_name": worker.last_name,
            "second_last_name": worker.second_last_name,
            "ci": worker.ci,
            "work_area": worker.work_area,
            "department": worker.department,
            "job_position": worker.job_position,
            "gender": worker.gender,
            "phone": worker.phone,
            "province": worker.province,
            "municipality": worker.municipality,
        }
        results[worker.id] = worker_dict

    return results


def create_worker(name, 
                  middle_name, 
                  last_name, 
                  second_last_name, 
                  ci,
                  work_area, 
                  department, 
                  job_position, 
                  academic_degree, 
                  gender, 
                  phone,
                  province, 
                  municipality
                  ):
    worker = Worker(name=name, 
                    middle_name=middle_name, 
                    last_name=last_name,
                    second_last_name=second_last_name, 
                    ci=ci, 
                    work_area=work_area,
                    department=department, 
                    job_position=job_position,
                    academic_degree=academic_degree,
                    gender=gender, 
                    phone=phone, 
                    province=province,
                    municipality=municipality
                    )
    session.add(worker)
    try:
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()  # optional, depends on use case
    print("Worker created successfully.")
    return worker


def update_worker(worker_id, 
                  name, 
                  middle_name, 
                  last_name, 
                  second_last_name,
                  ci, 
                  work_area, 
                  department, 
                  job_position,
                  academic_degree, 
                  gender, 
                  phone,
                  province, 
                  municipality):
    worker = session.query(Worker).get(worker_id)
    if worker:
        worker.name = name
        worker.middle_name = middle_name
        worker.last_name = last_name
        worker.second_last_name = second_last_name
        worker.ci = ci
        worker.work_area = work_area
        worker.department = department
        worker.job_position = job_position
        worker.academic_degree = academic_degree
        worker.gender = gender
        worker.phone = phone
        worker.province = province
        worker.municipality = municipality
        try:
            session.commit()
            print("Worker updated successfully.")
        except:
            session.rollback()
            raise
        finally:
            session.close()  # optional, depends on use case
    else:
        print("Worker not found.")


def delete_worker(worker_id):
    worker = session.query(Worker).get(worker_id)
    if worker:
        session.delete(worker)
        session.commit()
        print("Worker deleted successfully.")
    else:
        print("Worker not found.")


def filter_worker_records(**kwargs):
    if all((value is None) or (value == '') for value in kwargs.values()):
        return {}

    worker_query = session.query(Worker)
    filters = []

    for field, value in kwargs.items():
        filters.append(getattr(Worker, field).ilike(f'%{value}%'))

    gender = kwargs.get('gender', '')
    if gender != '':
        filters.append(Worker.gender.ilike(gender))

    if filters:
        worker_query = worker_query.filter(and_(*filters))

    workers = worker_query.all()
    results = {}
    for worker in workers:
        worker_dict = {
            "name": worker.name,
            "middle_name": worker.middle_name,
            "last_name": worker.last_name,
            "second_last_name": worker.second_last_name,
            "ci": worker.ci,
            "work_area": worker.work_area,
            "department": worker.department,
            "job_position": worker.job_position,
            "gender": worker.gender,
            "phone": worker.phone,
            "province": worker.province,
            "municipality": worker.municipality,
        }
        results[worker.id] = worker_dict
    return results


def filter_signature_sheets_records(id_worker):
    worker = session.query(Worker).get(id_worker)
    if not worker:
        return {}  # Retorna un diccionario vacío si no se encuentra el trabajador

    signature_sheets = {sheet.id: {
        'entry_time': sheet.entry_time,
        'exit_time': sheet.exit_time,
        'date': sheet.date,
        'location': sheet.location,
        'notes': sheet.notes
    } for sheet in worker.signature_sheets}

    return signature_sheets


def get_signature_sheet_by_id(signature_sheet_id):
    try:
        # Perform the query to retrieve the signature sheet
        signature_sheet = session.query(SignatureSheet).filter(SignatureSheet.id == signature_sheet_id).first()

        field_dict = {}  # Initialize the field dictionary as empty

        if signature_sheet:
            field_dict['id'] = signature_sheet.id
            field_dict['worker_id'] = signature_sheet.worker_id
            field_dict['entry_time'] = signature_sheet.entry_time
            field_dict['exit_time'] = signature_sheet.exit_time
            field_dict['date'] = signature_sheet.date
            field_dict['location'] = signature_sheet.location
            field_dict['notes'] = signature_sheet.notes

        return field_dict
    except SQLAlchemyError as e:
        # Handle the error
        print(f"An error occurred while retrieving fields from the database: {str(e)}")
        return {}
    except Exception as e:
        print(f"An error occurred while accessing fields from the database: {str(e)}")
        return {}


def show_records_by_year(filter_params) -> tuple:
    worker_results = filter_worker_records(**filter_params)
    w_id = next(iter(worker_results.keys()))
    dict_signature_sheets_by_month = {}
    for worker_id, worker_data in worker_results.items():
        signature_sheets = filter_signature_sheets_records(worker_id)
        for sheet_id, sheet_data in signature_sheets.items():
            date_obj = sheet_data['date']
            year = date_obj.year
            # month = date_obj.strftime("%B")
            worker_key = worker_id
            sheet_info = {
                'sheet_id': sheet_id,
                'worker_id': filter_params,
                'entry_time': sheet_data['entry_time'],
                'exit_time': sheet_data['exit_time'],
                'date': sheet_data['date'],
                'location': sheet_data['location'],
                'notes': sheet_data['notes'],
            }
            if worker_key not in dict_signature_sheets_by_month:
                dict_signature_sheets_by_month[worker_key] = [sheet_info]
            else:
                dict_signature_sheets_by_month[worker_key].append(sheet_info)
    # aqui obtengo las hojas de firmas por meses con el id asociado a su trabajador
    # y en worker_results obtengo directamente el id del trabajador
    return w_id, dict_signature_sheets_by_month


def signature_sheets_without_absences(signature_sheet_ids):
    """
    Retrieve a list of signature sheets without any associated absences.

    Parameters
    ----------
    signature_sheet_ids : list
        A list of signature sheet IDs for which to check absence associations.

    Returns
    -------
    list
        A list of signature sheet IDs that do not have any associated absences.
    """
    # Initialize a list to store the signature sheets without absences
    sheets_without_absences = []

    for signature_sheet_id in signature_sheet_ids:
        # Query the database to check if the signature sheet has any absence associated
        absence = session.query(Absence).filter_by(signature_sheet_id=signature_sheet_id).first()

        if absence is None:
            sheets_without_absences.append(signature_sheet_id)

    return sheets_without_absences


def calculate_absence_percentage(worker_id: str) -> tuple:
    month_percentage = {}
    year_percentage = 0.0
    month_absences_count = {}
    month_workdays_count = {}
    worker = session.query(Worker).filter_by(id=worker_id).first()
    if worker:
        total_absences = session.query(Absence).join(Absence.signature_sheet).filter(
            SignatureSheet.worker_id == worker_id
        ).count()

        total_workdays = session.query(SignatureSheet).filter(
            SignatureSheet.worker_id == worker_id,
            func.extract('year', SignatureSheet.date) == date.today().year
        ).count()
        try:
            year_percentage = (total_absences / total_workdays) * 100
            year_percentage = "{:.2f}".format(year_percentage)
        except ZeroDivisionError:
            print("El trabajador con ID {} no tiene días laborales cumplidos.".format(worker_id))

        english_month_names = [
            "",
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ]
        for month in range(1, 13):
            month_name = english_month_names[month]  # Obtener el nombre del mes en inglés
            print(month_name)
            month_absences = session.query(Absence).join(Absence.signature_sheet).filter(
                SignatureSheet.worker_id == worker_id,
                func.extract('year', SignatureSheet.date) == date.today().year,
                func.extract('month', SignatureSheet.date) == month
            ).count()
            month_workdays = session.query(SignatureSheet).filter(
                SignatureSheet.worker_id == worker_id,
                func.extract('year', SignatureSheet.date) == date.today().year,
                func.extract('month', SignatureSheet.date) == month
            ).count()
            try:
                month_percentage[month_name] = (month_absences / month_workdays) * 100
                month_percentage[month_name] = "{:.2f}".format(month_percentage[month_name])
                month_absences_count[month_name] = month_absences
                month_workdays_count[month_name] = month_workdays
            except ZeroDivisionError:
                print(
                    "El trabajador con ID {} no tiene días laborales cumplidos "
                    "en el mes {}.".format(worker_id, month_name))
                continue
    else:
        print("No se encontró ningún trabajador con el ID especificado:", worker_id)
    return month_percentage, year_percentage, month_absences_count, month_workdays_count


def create_signature_sheet(worker_id, entry_time, exit_time, date, location, notes):
    """
        Create a new SignatureSheet.

        Parameters:
            worker_id (int): The ID of the associated worker.
            entry_time (str): The entry time.
            exit_time (str): The exit time.
            date (date): The date of the signature sheet.
            location (str): The location where the worker signed in.
            notes (str): Additional notes or comments related to the signature sheet.

        Returns:
            SignatureSheet: The created SignatureSheet object.
    """
    signature_sheet = SignatureSheet(worker_id=worker_id, entry_time=entry_time, exit_time=exit_time,
                                     date=date, location=location, notes=notes)
    session.add(signature_sheet)
    session.commit()
    return signature_sheet.id


def read_all_signature_sheets():
    signature_sheets = session.query(SignatureSheet).all()
    return signature_sheets


def read_signature_sheet_by_id(signature_sheet_id):
    signature_sheet = session.query(SignatureSheet).get(signature_sheet_id)
    return signature_sheet


def update_signature_sheet(signature_sheet_id: str,
                           entry_time=hora_actual,
                           exit_time=hora_actual,
                           date=date,
                           location='Oficina1',
                           notes='Nota gen\u00E9rica'):
    signature_sheet = session.query(SignatureSheet).get(signature_sheet_id)
    if signature_sheet:
        signature_sheet.entry_time = entry_time
        signature_sheet.exit_time = exit_time
        signature_sheet.date = date
        signature_sheet.location = location
        signature_sheet.notes = notes
        session.commit()
        print("Signature updated successfully.")
    else:
        print("Signature sheet not found.")


def delete_signature_sheet(signature_sheet_id):
    signature_sheet = session.query(SignatureSheet).get(signature_sheet_id)
    if signature_sheet:
        session.delete(signature_sheet)
        session.commit()
        print("Signature deleted successfully.")
    else:
        print("Signature sheet not found.")


def create_absence(signature_sheet_id, date, reason):
    """
        Create a new Absence.

        Parameters:
            signature_sheet_id (int): The ID of the associated signature sheet.
            date (date): The date of the absence.
            reason (str): The reason for the absence.

        Returns:
            Absence: The created Absence object.
    """
    absence = Absence(signature_sheet_id=signature_sheet_id, date=date, reason=reason)
    session.add(absence)
    session.commit()
    return absence


def read_all_absences():
    absences = session.query(Absence).all()
    return absences


def read_absence_by_id(absence_id):
    absence = session.query(Absence).get(absence_id)
    return absence


def update_absence(absence_id, date, reason):
    absence = session.query(Absence).get(absence_id)
    absence.date = date
    absence.reason = reason
    session.commit()


def delete_absence(absence_id):
    absence = session.query(Absence).get(absence_id)
    if absence:
        session.delete(absence)
        session.commit()
        print("Absence deleted successfully.")
    else:
        print("Absence sheet not found.")


def get_ids_not_in_pkl():
    """
        Retrieve the IDs of workers in the database that are not present in the .pkl file.

        Args:

        Returns:
            A list of worker IDs that are in the database but not in the .pkl file.
    """
    try:
        pkl_file_path = os.path.join(current_dir, '../usuarios_autenticados.pkl')
        with open(pkl_file_path, 'rb') as f:
            data_pkl = pickle.load(f)
        ids_pkl = list(data_pkl.keys())
    except FileNotFoundError:
        print('No existe archivo .pkl')
        ids_pkl = []

    # Consultar los IDs de los usuarios en la base de datos
    query = session.query(Worker.id).all()
    ids_db = [id_[0] for id_ in query]

    # Obtener los IDs de los usuarios que están en la base de datos pero no están en el archivo .pkl
    ids_not_in_pkl = [id_db for id_db in ids_db if id_db not in ids_pkl]

    return ids_not_in_pkl
