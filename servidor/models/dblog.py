import datetime

from sqlalchemy import Column, Integer, ForeignKey, Text, Enum, BigInteger
from sqlalchemy.orm import relationship

from . import Base
from .courses import Platform, PlatformAuth, Course, Module, Lesson, File

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    event_type = Column(Enum(
                            'application_start',
                            'application_stop',
                            'phone_home',
                            'informational',
                            'warning',
                            'authentication',
                            'log_out',
                            'course_list',
                            'module_list',
                            'lesson_list',
                            'file_list',
                            'file_download',
                            'file_upload',
                            'download_error',
                            'upload_error',
                            'catch_all_error',
                            name='event_types'), nullable=False)
    message = Column(Text)
    created_at = Column(BigInteger, default=lambda: int(datetime.datetime.now().timestamp()))

    # Chaves estrangeiras existentes
    platform_auth_id = Column(Integer, ForeignKey('platform_auths.id'))
    platform_id = Column(Integer, ForeignKey('platforms.id'))

    # Chaves estrangeiras adicionadas para Course, Module, Lesson, e File
    course_id = Column(Integer, ForeignKey('courses.id'))
    module_id = Column(Integer, ForeignKey('modules.id'))
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    file_id = Column(Integer, ForeignKey('files.id'))

    # Relacionamentos
    platform = relationship("Platform", backref="logs")
    platform_auth = relationship("PlatformAuth", backref="logs")
    course = relationship("Course", backref="logs")
    module = relationship("Module", backref="logs")
    lesson = relationship("Lesson", backref="logs")
    file = relationship("File", backref="logs")

    def __repr__(self):
        return f"<Log(event_type={self.event_type}, message={self.message}, timestamp={self.created_at}, platform_id={self.platform_id}, platform_auth_id={self.platform_auth_id}, course_id={self.course_id}, module_id={self.module_id}, lesson_id={self.lesson_id}, file_id={self.file_id})>"
