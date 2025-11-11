from sqlalchemy import func, desc
from models import Student, Group, Teacher, Subject, Grade
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:testpassword0123@localhost/postgres')
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    return session.query(Student.name, func.avg(Grade.grade).label('avg_grade')) \
        .join(Grade) \
        .group_by(Student.id) \
        .order_by(desc('avg_grade')) \
        .limit(5) \
        .all()

def select_2(subject_name):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    return session.query(Student.name, func.avg(Grade.grade).label('avg_grade')) \
        .join(Grade) \
        .join(Subject) \
        .filter(Subject.name == subject_name) \
        .group_by(Student.id) \
        .order_by(desc('avg_grade')) \
        .first()

def select_3(subject_name):
    """Знайти середній бал у групах з певного предмета."""
    return session.query(Group.name, func.avg(Grade.grade).label('avg_grade')) \
        .select_from(Grade) \
        .join(Student) \
        .join(Group) \
        .join(Subject) \
        .filter(Subject.name == subject_name) \
        .group_by(Group.name) \
        .all()

def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    return session.query(func.avg(Grade.grade)).scalar()

def select_5(teacher_name):
    """Знайти які курси читає певний викладач."""
    return session.query(Subject.name) \
        .join(Teacher) \
        .filter(Teacher.name == teacher_name) \
        .all()

def select_6(group_name):
    """Знайти список студентів у певній групі."""
    return session.query(Student.name) \
        .join(Group) \
        .filter(Group.name == group_name) \
        .all()

def select_7(group_name, subject_name):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    return session.query(Student.name, Grade.grade) \
        .join(Grade) \
        .join(Group) \
        .join(Subject) \
        .filter(Group.name == group_name, Subject.name == subject_name) \
        .all()

def select_8(teacher_name):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    return session.query(func.avg(Grade.grade)) \
        .join(Subject) \
        .join(Teacher) \
        .filter(Teacher.name == teacher_name) \
        .scalar()

def select_9(student_name):
    """Знайти список курсів, які відвідує певний студент."""
    return session.query(Subject.name) \
        .distinct() \
        .join(Grade) \
        .join(Student) \
        .filter(Student.name == student_name) \
        .all()

def select_10(student_name, teacher_name):
    """Список курсів, які певному студенту читає певний викладач."""
    return session.query(Subject.name) \
        .distinct() \
        .join(Grade) \
        .join(Student) \
        .join(Teacher) \
        .filter(Student.name == student_name, Teacher.name == teacher_name) \
        .all()

if __name__ == '__main__':
    print("Select 1:", select_1())
    print("Select 2:", select_2('determine'))
    print("Select 3:", select_3('determine'))
    print("Select 5:", select_5('Ryan Diaz'))
    print("Select 6:", select_6('find'))
    print("Select 7:", select_7('find', 'determine'))
    print("Select 8:", select_8('Ryan Diaz'))
    print("Select 9:", select_9('Robert Johnson'))
    print("Select 10:", select_10('Robert Johnson', 'Ryan Diaz'))
