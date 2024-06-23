import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, BigInteger, JSON, Float
from sqlalchemy.orm import relationship

from . import Base


class PlatformAuth(Base):
    __tablename__ = 'platform_auths'

    id = Column(Integer, primary_key=True)
    platform_id = Column(Integer, ForeignKey('platforms.id'))
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    token = Column(String)
    account_domain = Column(String)
    refresh_token = Column(String)
    token_expires_at = Column(BigInteger)
    extra_data = Column(JSON)
    is_logged_in = Column(Boolean, default=False)
    valid_combination = Column(Boolean, default=True)
    created_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()))
    updated_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()), onupdate=lambda: int(datetime.datetime.now().timestamp()))

    platform = relationship("Platform", back_populates="auths")

class Platform(Base):
    __tablename__ = 'platforms'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    base_url = Column(String)
    auths = relationship("PlatformAuth", back_populates="platform")
    courses = relationship("Course", back_populates="platform")

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher = Column(String)
    price = Column(Float)
    description = Column(String)
    platform_id = Column(Integer, ForeignKey('platforms.id'))
    platform  = relationship("Platform", back_populates="courses")
    modules = relationship("Module", back_populates="course")

class Module(Base):
    __tablename__ = 'modules'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    course_id = Column(Integer, ForeignKey('courses.id'))
    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module")

class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    module_id = Column(Integer, ForeignKey('modules.id'))
    module = relationship("Module", back_populates="lessons")
    files = relationship("File", back_populates="lesson")

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    file_size = Column(Integer)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    lesson = relationship("Lesson", back_populates="files")
