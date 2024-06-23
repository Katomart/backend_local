import json

from . import Base
from sqlalchemy import Column, Integer, String, Boolean, Text

class Configuration(Base):
    __tablename__ = 'configs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), nullable=False, unique=True)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    enabled = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Configuration(key='{self.key}', value='{self.value}', enabled={self.enabled})>"

    def to_dict(self):
        if isinstance(self.value, bytes):
            normalized_value = self.value.decode('utf-8')
        if isinstance(self.description, bytes):
            normalized_description = self.description.decode('utf-8')

        normalized_value = json.loads(self.normalized_value)
        return {
            'id': int(self.id),
            'key': str(self.key),
            'value': normalized_value,
            'description': normalized_description if self.description else '',
            'enabled': bool(self.enabled)
        }
