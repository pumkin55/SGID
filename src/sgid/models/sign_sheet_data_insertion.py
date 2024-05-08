from datetime import date, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Worker, SignatureSheet

# Create an instance of the Engine class to establish a connection to the database
engine = create_engine('sqlite:///database.db')

# Create a database session
Session = sessionmaker(bind=engine)
session = Session()

# Obtener el trabajador con el ID especificado
worker_id = '58405d02-ea01-4918-92c8-f929d99e8476'
worker = session.query(Worker).filter_by(id=worker_id).first()

if worker:
    # Generate records for each month
    for month in range(1, 13):  # Loop through each month (from 1 to 12)
        # Calculate the first day of the current month
        first_day_of_month = date(date.today().year, month, 1)

        # Generate 30 records for the current month
        for day in range(30):
            # Calculate the date for the current record
            record_date = first_day_of_month + timedelta(days=day)

            sheet = SignatureSheet(
                worker=worker,
                entry_time='09:00',
                exit_time='17:00',
                date=record_date,
                location='Oficina',
                notes='Registro {}'.format(day + 1)
            )
            session.add(sheet)

    session.commit()
    print("Se han ingresado 30 hojas de registros para cada mes del trabajador con ID:", worker_id)
else:
    print("No se encontró ningún trabajador con el ID especificado:", worker_id)
