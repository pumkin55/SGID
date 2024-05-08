"""
Module: models.py
This module defines the SQLAlchemy models for the database schema.

It includes the following classes:

- Worker: Represents the 'worker' table in the database, storing information about workers.
- SignatureSheet: Represents the 'signature_sheet' table, recording entry and exit times of workers.
- Absence: Represents the 'absence' table, storing information about worker absences.
- VacationAbsence: Represents the 'vacation_absence' table, a child table of 'absence' for vacation-specific details.
- SickLeaveAbsence: Represents the 'sick_leave_absence' table, a child table of 'absence' for sick leave-specific
details.

These models are used to create the corresponding database tables and establish relationships between them.

Worker has a relation of 1:M with SignatureSheet. A worker can have many signature sheet, and a signature sheet can have
only one worker.
SignatureSheet has a relation of 1:M with Absence. A signature sheet can have many absence, and an absence can have
only one SignatureSheet

Note: This module assumes the use of SQLAlchemy as the ORM (Object-Relational Mapping) tool.
"""

import uuid

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()


class Worker(Base):
    """
    Represents the 'worker' table in the database.

    Columns:
        id (String): The worker's unique identifier (UUID).
        name (String): The name of the worker.
        middle_name (String): The middle name of the worker.
        last_name (String): The last name of the worker.
        second_last_name (String): The second last name of the worker.
        ci (Integer): Worker's CI
        year (Integer): The year of birth of the worker.
        month (Integer): The month of birth of the worker.
        day (Integer): The day of birth of the worker.
        work_area (String): The worker's work area.
        department (String): The worker's department.
        job_position (String): The worker's job position.
        gender (String): The worker's gender.

    Relationships:
        signature_sheets (List[SignatureSheet]): Relationship to the 'SignatureSheet' table.
    """
    __tablename__ = 'worker'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    name = Column(String(30), nullable=False)
    middle_name = Column(String)
    last_name = Column(String(30), nullable=False)
    second_last_name = Column(String(30), nullable=False)
    ci = Column(Integer, nullable=False, unique=True)
    work_area = Column(String(50), nullable=False)
    department = Column(String(50), nullable=False)
    job_position = Column(String(50), nullable=False)
    academic_degree = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=False)
    phone = Column(Integer, nullable=False, unique=True)
    province = Column(String(50), nullable=False)
    municipality = Column(String(50), nullable=False)

    signature_sheets = relationship('SignatureSheet', back_populates='worker', cascade='all, delete')

    __table_args__ = (
        UniqueConstraint('id', 'ci', name='_worker_id_uc'),
        UniqueConstraint('phone', name='_phone_id_uc'),
        CheckConstraint('name IS NOT NULL', name='_worker_name_not_null'),
        CheckConstraint('last_name IS NOT NULL', name='_worker_last_name_not_null'),
        CheckConstraint('second_last_name IS NOT NULL', name='_worker_second_last_name_not_null'),
        CheckConstraint('work_area IS NOT NULL', name='_worker_work_area_not_null'),
        CheckConstraint('department IS NOT NULL', name='_worker_department_not_null'),
        CheckConstraint('job_position IS NOT NULL', name='_worker_job_position_not_null'),
        CheckConstraint('gender IS NOT NULL', name='_worker_gender_not_null'),
    )

    def __repr__(self):
        return ("User id: '{self.id}', "
                "Name: '{self.name}', "
                "Middle name: '{self.middle_name}', "
                "Last name: '{self.last_name}', "
                "Second Last name: '{self.second_last_name}', "
                "User ci: '{self.ci}', "
                "work_area: '{self.work_area}', "
                "Department: '{self.department}', "
                "Job_position: '{self.job_position}', "
                "Academic Degree: '{self.academic_degree}', "
                "Gender: '{self.gender}', "
                "Phone: '{self.phone}', "
                "Province: '{self.province}', "
                "Municipality: '{self.municipality}', \n".format(self=self))


class SignatureSheet(Base):
    """
    Represents the 'signature_sheet' table in the database.

    Columns:
        id (String): The worker's unique identifier (UUID).
        worker_id (Integer): Foreign key corresponding to worker's id.
        entry_time (String): The entry time.
        exit_time (String): The exit time.
        date (Date): Signature sheet date entry.
        location (String): The location where the worker signed in.
        notes (String): Additional notes or comments related to the signature sheet.

    Relationships:
        worker (Worker): Relationship to the 'Worker' table.
        absences (List[Absence]): Relationship to the 'Absence' table.
    """
    __tablename__ = 'signature_sheet'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    worker_id = Column(Integer, ForeignKey('worker.id'))
    entry_time = Column(String)
    exit_time = Column(String)
    date = Column(Date)
    location = Column(String)
    notes = Column(String)

    worker = relationship('Worker', back_populates='signature_sheets')
    absences = relationship('Absence', back_populates='signature_sheet', cascade='all, delete')

    __table_args__ = (UniqueConstraint('id', name='_signature_sheet_id_uc'),)

    def __repr__(self):
        return ("User id: '{self.worker_id}', "
                "ID: '{self.id}', "
                "Entry time: '{self.entry_time}', "
                "Exit time: '{self.exit_time}', "
                "Date: '{self.date}', "
                "Location: '{self.location}', "
                "Notes: '{self.notes}' \n".format(self=self))


class Absence(Base):
    """
    Represents the 'absence' table in the database.

    Columns:
        id (String): The worker's unique identifier (UUID).
        signature_sheet_id (Integer): Foreign key corresponding to signature sheet.
        date (Date): The date of the absence.
        reason (String): The reason for the absence.

    Relationships:
        signature_sheet (SignatureSheet): Relationship to the 'SignatureSheet' table.
    """
    __tablename__ = 'absence'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    signature_sheet_id = Column(Integer, ForeignKey('signature_sheet.id'))
    date = Column(Date)
    reason = Column(String)

    signature_sheet = relationship('SignatureSheet', back_populates='absences')

    __table_args__ = (UniqueConstraint('id', name='_absence_id_uc'),)


class VacationAbsence(Absence):
    """
    Represents the 'vacation_absence' table, which is a child table of 'absence' table.

    Additional Columns:
        vacation_type (String): The type of vacation absence.
        duration (Integer): The duration of the vacation absence in days.
    """
    __tablename__ = 'vacation_absence'

    id = Column(String, ForeignKey('absence.id'), primary_key=True, default=lambda: str(uuid.uuid4()))
    vacation_type = Column(String)
    duration = Column(Integer)

    __table_args__ = (UniqueConstraint('id', name='_vacation_absence_id_uc'),)


class SickLeaveAbsence(Absence):
    """
    Represents the 'sick_leave_absence' table, which is a child table of 'absence' table.

    Additional Columns:
        doctor_name (String): The name of the doctor for sick leave.
        diagnosis (String): The diagnosis for the sick leave.
    """
    __tablename__ = 'sick_leave_absence'

    id = Column(String, ForeignKey('absence.id'), primary_key=True, default=str(uuid.uuid4()))
    doctor_name = Column(String)
    diagnosis = Column(String)

    __table_args__ = (UniqueConstraint('id', name='_sick_leave_absence_id_uc'),)


# Asegurar que las tablas se creen solo cuando se ejecute directamente este módulo
if __name__ == "__main__":
    Base.metadata.create_all(engine)
