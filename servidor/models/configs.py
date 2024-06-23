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
        else:
            normalized_value = self.value

        if isinstance(self.description, bytes):
            normalized_description = self.description.decode('utf-8')
        else:
            normalized_description = self.description

        try:
            normalized_value = json.loads(normalized_value)
        except json.JSONDecodeError:
            try:
                normalized_value = eval(normalized_value)
            except:
                normalized_value = normalized_value

        if not normalized_description:
            normalized_description = 'Sem descrição fornecida pelo autor!'

        return {
            'id': int(self.id),
            'key': str(self.key),
            'value': normalized_value,
            'description': normalized_description,
            'enabled': bool(self.enabled)
        }
