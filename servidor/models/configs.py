import json

from . import Base
from sqlalchemy import Column, Integer, String, Boolean, Text, Enum

class Configuration(Base):
    __tablename__ = 'configs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), nullable=False, unique=True)
    value = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    value_type = Column(Enum('str', 'int', 'float', 'bool', 'list', 'json', 'select', name='value_type'), nullable=False, default='str')
    voidable = Column(Boolean, default=False)
    editable = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Configuration(key='{self.key}', value='{self.value}', description='{self.description}', value_type='{self.value_type}', voidable='{self.voidable}', can_edit='{self.editable}' enabled={self.enabled})>"

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

        if isinstance(self.value_type, bytes):
            normalized_value_type = self.value_type.decode('utf-8')
        else:
            normalized_value_type = self.value_type

        return {
            'id': int(self.id),
            'key': str(self.key),
            'value': normalized_value,
            'description': normalized_description,
            'value_type': normalized_value_type,
            'voidable': bool(self.voidable),
            'editable': bool(self.editable),
            'enabled': bool(self.enabled)
        }
