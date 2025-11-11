import faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade
import random
from datetime import datetime

engine = create_engine('postgresql://postgres:testpassword0123@localhost/postgres')
Session = sessionmaker(bind=engine)
session = Session()

fake = faker.Faker()

# Create groups
for _ in range(3):
    group = Group(name=fake.word())
    session.add(group)
session.commit()

# Create teachers
for _ in range(5):
    teacher = Teacher(name=fake.name())
    session.add(teacher)
session.commit()

# Create subjects
teachers = session.query(Teacher).all()
for _ in range(8):
    subject = Subject(name=fake.word(), teacher=random.choice(teachers))
    session.add(subject)
session.commit()

# Create students
groups = session.query(Group).all()
for _ in range(50):
    student = Student(name=fake.name(), group=random.choice(groups))
session.commit()

print("Generated Groups:", [g.name for g in session.query(Group).limit(3).all()])
print("Generated Teachers:", [t.name for t in session.query(Teacher).limit(3).all()])
print("Generated Subjects:", [s.name for s in session.query(Subject).limit(3).all()])
print("Generated Students:", [s.name for s in session.query(Student).limit(3).all()])

# Create grades
students = session.query(Student).all()
subjects = session.query(Subject).all()
for student in students:
    for _ in range(random.randint(10, 20)):
        grade = Grade(
            student=student,
            subject=random.choice(subjects),
            grade=random.randint(1, 100),
            date=fake.date_between(start_date='-1y', end_date='today')
        )
        session.add(grade)
session.commit()
