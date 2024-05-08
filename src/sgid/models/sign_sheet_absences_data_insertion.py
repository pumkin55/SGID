import random
from datetime import date, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Worker, SignatureSheet, Absence

# Create an instance of the Engine class to establish a connection to the database
engine = create_engine('sqlite:///database.db')

# Create a database session
Session = sessionmaker(bind=engine)
session = Session()

# Obtener el trabajador con el ID especificado
worker_id = '51718eff-7557-4470-be1a-3bdfa6c01c68'
worker = session.query(Worker).filter_by(id=worker_id).first()

if worker:
    for month in range(1, 13):
        first_day_of_month = date(date.today().year, month, 1)

        for day in range(31):
            record_date = first_day_of_month + timedelta(days=day)

            # Verificar si el día es laboral (no sábado ni domingo)
            if record_date.weekday() < 5:
                # Generar registro de hoja de firma
                sheet = SignatureSheet(
                    worker=worker,
                    entry_time='09:00',
                    exit_time='17:00',
                    date=record_date,
                    location='Oficina',
                    notes='Registro {}'.format(day + 1)
                )
                session.add(sheet)

                # Generar registro de ausencia de forma aleatoria
                if random.random() < 0.1:
                    absence = Absence(
                        signature_sheet=sheet,
                        date=record_date,
                        reason='Ausencia {}'.format(day + 1)
                    )
                    session.add(absence)

    session.commit()
    print("Se han ingresado registros de hojas de firma y ausencias para cada día laboral del trabajador con ID:",
          worker_id)
else:
    print("No se encontró ningún trabajador con el ID especificado:", worker_id)
