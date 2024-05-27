from . import Base
from sqlalchemy import Column, Integer, String, Boolean

class Configuracao(Base):
    __tablename__ = 'configs'
    id = Column(Integer, primary_key=True)
    chave = Column(String(100), nullable=False, unique=True)
    valor = Column(String(255))
    ativo = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Configuracao(chave='{self.chave}', valor='{self.valor}', ativo={self.ativo})>"
