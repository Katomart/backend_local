# tests/test_models/test_course_structure.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from servidor.models.courses import Base, Platform, Course, Module, Lesson, File

@pytest.fixture(scope='module')
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture(scope='module')
def session(engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_platform_course_relationship(session):
    platform = Platform(name="Udemy")
    course = Course(name="Python Programming", platform=platform)
    session.add(platform)
    session.commit()
    assert course.platform is not None, "Course should have a platform"
    assert course.platform.name == "Udemy", "Platform name should be 'Udemy'"
    assert len(platform.courses) > 0, "Platform should have at least one course"
    assert platform.courses[0].name == "Python Programming", "Course name should match"

def test_course_module_lesson_file_structure(session):
    course = Course(name="Advanced Python")
    module = Module(name="Concurrency", course=course)
    lesson = Lesson(name="AsyncIO Basics", module=module)
    file = File(name="example_code.py", lesson=lesson)
    session.add(course)
    session.commit()
    assert module.course is not None, "Module should have a course"
    assert lesson.module is not None, "Lesson should have a module"
    assert file.lesson is not None, "File should have a lesson"
    assert module.course.name == "Advanced Python", "Course name should be 'Advanced Python'"
    assert lesson.module.name == "Concurrency", "Module name should be 'Concurrency'"
    assert file.lesson.name == "AsyncIO Basics", "Lesson name should be 'AsyncIO Basics'"