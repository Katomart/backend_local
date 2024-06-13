# tests/test_models/test_course_structure.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from servidor.models.courses import Base, PlatformAuth, Platform, Course, Module, Lesson, File

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

def test_platform_auth_creation_with_all_required_fields(session):
    complete_auth = PlatformAuth(
        login_url="http://example.com/login",
        username="user_example",
        password="secure_password",
        is_logged_in=False
    )
    session.add(complete_auth)
    session.commit()
    
    # Verifica inserções
    inserted_auth = session.query(PlatformAuth).filter_by(username="user_example").first()
    assert inserted_auth is not None
    assert inserted_auth.password == "secure_password"
    assert inserted_auth.is_logged_in is False

def test_platform_auth(session):
    session.query(PlatformAuth).delete()  # Clear all test data
    auth = PlatformAuth(
        username="user",
        password="password",
        token="12345",
        token_expires_at=9999999999,  # Epoch time in seconds
        is_logged_in=True
    )
    session.add(auth)
    session.commit()

    fetched_auth = session.query(PlatformAuth).first()
    assert fetched_auth.token == "12345"
    assert fetched_auth.token_expires_at == 9999999999
    assert fetched_auth.is_logged_in == True
