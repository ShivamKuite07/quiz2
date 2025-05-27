# core/fake_data.py


import random
from faker import Faker
import os
import django
import sys

# Set up path to root directory of project (where manage.py is)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz2.settings")
django.setup()


from core.models import Department, Employee, Attendance, Performance
from datetime import timedelta, datetime

fake = Faker()

def seed_departments(n=3):
    departments = []
    for _ in range(n):
        dept = Department.objects.create(
            name=fake.unique.job(),
            manager=fake.name(),
            location=fake.city()
        )
        departments.append(dept)
    return departments

def seed_employees(n=5, departments=None):
    employees = []
    for _ in range(n):
        emp = Employee.objects.create(
            name=fake.name(),
            email=fake.unique.email(),
            phone=fake.phone_number(),
            department=random.choice(departments),
            join_date=fake.date_between(start_date='-2y', end_date='today'),
            role=fake.job(),
            salary=round(random.uniform(30000, 120000), 2)
        )
        employees.append(emp)
    return employees

def seed_attendance(employees, days=10):
    for employee in employees:
        for _ in range(days):
            date = fake.date_between(start_date='-15d', end_date='today')
            check_in_time = fake.time_object()
            check_out_time = (datetime.combine(datetime.today(), check_in_time) + timedelta(hours=8)).time()
            status = random.choice(['Present', 'Absent', 'Leave'])
            worked_hours = round(random.uniform(0, 8), 2) if status == 'Present' else 0
            Attendance.objects.create(
                employee=employee,
                date=date,
                check_in=check_in_time,
                check_out=check_out_time,
                status=status,
                worked_hours=worked_hours
            )

def seed_performance(employees):
    current_year = datetime.now().year
    for employee in employees:
        for month in ['January', 'February', 'March']:
            Performance.objects.create(
                employee=employee,
                month=month,
                year=current_year,
                rating=random.randint(1, 5),
                achievements=fake.sentence(),
                remarks=fake.text(max_nb_chars=100),
                reviewer=fake.name()
            )

if __name__ == "__main__":
    print("Seeding data...")

    Department.objects.all().delete()
    Employee.objects.all().delete()
    Attendance.objects.all().delete()
    Performance.objects.all().delete()

    departments = seed_departments()
    employees = seed_employees(departments=departments)
    seed_attendance(employees)
    seed_performance(employees)

    print("✅ Done seeding data.")
