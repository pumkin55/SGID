from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Worker, Base

# Create an instance of the Engine class to establish a connection to the database
engine = create_engine('sqlite:///database.db')

# Create all tables defined in the model
Base.metadata.create_all(engine)

# Create a database session
Session = sessionmaker(bind=engine)
session = Session()

# Create instances of the Worker class with test data and add them to the session

workers_data = [
    {
        'name': 'Raikol',
        'middle_name': '',
        'last_name': 'Alvarez',
        'second_last_name': 'Leon',
        'ci': '98093004908',
        'work_area': 'Information Technology',
        'department': 'Software Development',
        'job_position': 'Software Engineer',
        'gender': 'Male',
        'phone': '55555555',
        'province': 'La Habana',
        'municipality': 'Playa',
    },  # 1
    {
        'name': 'Jane',
        'middle_name': 'Doe',
        'last_name': 'Johnson',
        'second_last_name': 'Doe',
        'ci': '97093004911',
        'work_area': 'Human Resources',
        'department': 'Employee Relations',
        'job_position': 'FEU President',
        'gender': 'Female',
        'phone': '44444444',
        'province': 'La Habana',
        'municipality': 'Playa',
    },  # 2
    {
        'name': 'John',
        'middle_name': 'Doe',
        'last_name': 'Smith',
        'second_last_name': 'Doe',
        'ci': '97093004912',
        'work_area': 'Security',
        'department': 'Emergency Response',
        'job_position': 'Police',
        'gender': 'Male',
        'phone': '61833438',
        'province': 'La Habana',
        'municipality': 'Playa',
    },  # 3
    {
        'name': 'Juliet',
        'middle_name': 'Smith',
        'last_name': 'Johnson',
        'second_last_name': 'Doe',
        'ci': '89093004567',
        'work_area': 'Security',
        'department': 'Campus Patrol',
        'job_position': 'Custodio',
        'gender': 'Female',
        'phone': '31485760',
        'province': 'La Habana',
        'municipality': 'Playa',
    },  # 4
    {
        'name': 'Michael',
        'middle_name': 'Smith',
        'last_name': 'Brown',
        'second_last_name': 'Johnson',
        'ci': '95083012134',
        'work_area': 'Information Technology',
        'department': 'Technical Support',
        'job_position': 'Technical Support Manager',
        'gender': 'Male',
        'phone': '00862468',
        'province': 'La Habana',
        'municipality': 'Playa',
    },  # 5
    {
        'name': 'Emily',
        'middle_name': 'Taylor',
        'last_name': 'Anderson',
        'second_last_name': 'Davis',
        'ci': '00010100000',
        'work_area': 'Human Resources',
        'department': 'Recruitment',
        'job_position': 'HR Manager',
        'gender': 'Female',
        'phone': '50590167',
        'province': 'La Habana',
        'municipality': 'Playa',
    },  # 6
    {
        'name': 'Daniel',
        'middle_name': 'Wilson',
        'last_name': 'Thomas',
        'second_last_name': 'Wilson',
        'ci': '99123199999',
        'work_area': 'Academic Affairs',
        'department': 'Quality Assurance',
        'job_position': 'Supervisor',
        'gender': 'Male',
        'phone': '61381291',
        'province': 'La Habana',
        'municipality': 'Playa',
    },  # 7
    {
        'name': 'Sarah',
        'middle_name': 'Jackson',
        'last_name': 'Miller',
        'second_last_name': 'Taylor',
        'ci': '97012001067',
        'work_area': 'Academic Affairs',
        'department': 'Faculty Affairs',
        'job_position': 'Dean',
        'gender': 'Female',
        'phone': '77558037',
        'province': 'La Habana',
        'municipality': 'Playa',
    },  # 8
    {
        'name': 'Robert',
        'middle_name': 'Brown',
        'last_name': 'Davis',
        'second_last_name': 'Miller',
        'ci': '94051203218',
        'work_area': 'Information Technology',
        'department': 'Database Management',
        'job_position': 'Warehouse Manager',
        'gender': 'Male',
        'phone': '39295659',
        'province': 'La Habana',
        'municipality': 'Playa',
    },  # 9
    {
        'name': 'Emma',
        'middle_name': 'Anderson',
        'last_name': 'Wilson',
        'second_last_name': 'Smith',
        'ci': '99872804123',
        'work_area': 'Information Technology',
        'department': 'Network Administration',
        'job_position': 'Software Engineer',
        'gender': 'Female',
        'phone': '12251031',
        'province': 'La Habana',
        'municipality': 'Playa',
    },  # 10
    {
        'name': 'David',
        'middle_name': 'Taylor',
        'last_name': 'Johnson',
        'second_last_name': 'Brown',
        'ci': '96020111834',
        'work_area': 'Human Resources',
        'department': 'HR Information Systems',
        'job_position': 'Senior HR Information Systems',
        'gender': 'Male',
        'phone': '16044368',
        'province': '',
        'municipality': '',
    },  # 11
    {
        'name': 'Olivia',
        'middle_name': 'Thomas',
        'last_name': 'Smith',
        'second_last_name': 'Wilson',
        'ci': '97062803356',
        'work_area': 'Human Resources',
        'department': 'Recruitment',
        'job_position': 'HR Assistant',
        'gender': 'Female',
        'phone': '80462014',
        'province': 'La Habana',
        'municipality': 'Playa',
    },  # 12
    {
        'name': 'Liam',
        'middle_name': 'Wilson',
        'last_name': 'Martinez',
        'second_last_name': 'Garcia',
        'ci': '91040504768',
        'work_area': 'Facilities Management',
        'department': 'Custodial Services',
        'job_position': 'Custodio',
        'gender': 'Male',
        'phone': '55515585',
        'province': 'La Habana',
        'municipality': 'Playa',
    },  # 13
    {
        'name': 'Sophia',
        'middle_name': 'Gonzalez',
        'last_name': 'Lopez',
        'second_last_name': 'Hernandez',
        'ci': '92071204980',
        'work_area': 'Academic Affairs',
        'department': 'Registrar\'s Office',
        'job_position': 'Professor',
        'gender': 'Female',
        'phone': '34253228',
        'province': 'La Habana',
        'municipality': 'Playa',
    },  # 14
    {
        'name': 'Jackson',
        'middle_name': 'Smith',
        'last_name': 'Robinson',
        'second_last_name': 'Clark',
        'ci': '93052403879',
        'work_area': 'Information Technology',
        'department': 'Software Development',
        'job_position': 'System Analyst',
        'gender': 'Male',
        'phone': '86444234',
        'province': 'La Habana',
        'municipality': 'Playa',
    },  # 15
    {
        'name': 'Ava',
        'middle_name': 'Johnson',
        'last_name': 'Taylor',
        'second_last_name': 'Moore',
        'ci': '95080304217',
        'work_area': 'Human Resources',
        'department': 'Compensation and Benefits',
        'job_position': 'Operations Manager',
        'gender': 'Female',
        'phone': '53449931',
        'province': 'La Habana',
        'municipality': 'Playa',
    },  # 16
    {
        'name': 'Lucas',
        'middle_name': 'Brown',
        'last_name': 'Young',
        'second_last_name': 'Sanchez',
        'ci': '96091003654',
        'work_area': 'Human Resources',
        'department': 'Recruitment',
        'job_position': 'Recruiter',
        'gender': 'Male',
        'phone': '27005817',
        'province': '',
        'municipality': '',
    },  # 17
    {
        'name': 'Mia',
        'middle_name': 'Davis',
        'last_name': 'Walker',
        'second_last_name': 'Rodriguez',
        'ci': '98020404120',
        'work_area': 'Facilities Managemen',
        'department': 'Maintenance',
        'job_position': 'Maintenance Boss',
        'gender': 'Female',
        'phone': '42357240',
        'province': 'La Habana',
        'municipality': 'Playa',
    },  # 18
    {
        'name': 'Noah',
        'middle_name': 'Miller',
        'last_name': 'Garcia',
        'second_last_name': 'Clark',
        'ci': '99070203984',
        'work_area': 'Information Technology',
        'department': 'Training and Development',
        'job_position': 'IT Manager',
        'gender': 'Male',
        'phone': '56948777',
        'province': 'La Habana',
        'municipality': 'Habana Vieja',
    },  # 19
    {
        'name': 'Isabella',
        'middle_name': 'Rodriguez',
        'last_name': 'Young',
        'second_last_name': 'Sanchez',
        'ci': '00121503429',
        'work_area': 'Security',
        'department': 'Investigations',
        'job_position': 'Auditor',
        'gender': 'Female',
        'phone': '82296920',
        'province': 'La Habana',
        'municipality': 'Cerro',
    },  # 20
    {
        'name': 'Ethan',
        'middle_name': 'Clark',
        'last_name': 'Moore',
        'second_last_name': 'Davis',
        'ci': '01100203908',
        'work_area': 'Facilities Management',
        'department': 'Groundskeeping',
        'job_position': 'Maintenance Professional',
        'gender': 'Male',
        'phone': '23465223',
        'province': 'La Habana',
        'municipality': 'Centro Habana',
    },  # 21
    {
        'name': 'Charlotte',
        'middle_name': 'Sanchez',
        'last_name': 'Lopez',
        'second_last_name': 'Wilson',
        'ci': '02110804357',
        'work_area': 'Human Resources',
        'department': 'Employee Relations',
        'job_position': 'Compensation Analyst',
        'gender': 'Female',
        'phone': '22265153',
        'province': 'Artemisa',
        'municipality': 'Candelaria',
    },  # 22
]

for data in workers_data:
    worker = Worker(**data)
    session.add(worker)

try:
    # Commit the changes to the database
    session.commit()
except:
    session.rollback()
    raise
finally:
    # Close the session and the connection to the database
    session.close()
    engine.dispose()
