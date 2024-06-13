import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from servidor.models.configs import Configuration, Base

@pytest.fixture(scope='module')
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture(scope='module')
def tables(engine):
    Base.metadata.create_all(engine)
    return engine

def test_criacao_configuracao(tables):
    engine = tables
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Criando uma nova configuração
    config = Configuration(key="intervalo_scraping", value="3600", enabled=True)
    session.add(config)
    session.commit()
    
    # Buscando e verificando a configuração inserida
    config_inserida = session.query(Configuration).first()
    assert config_inserida.key == "intervalo_scraping"
    assert config_inserida.value == "3600"
    assert config_inserida.enabled is True
    session.close()

def test_atualizacao_configuracao(tables):
    engine = tables
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Atualizando a configuração
    config = session.query(Configuration).filter_by(key="intervalo_scraping").first()
    config.value = "1800"
    session.commit()
    
    # Verificando a atualização
    config_atualizada = session.query(Configuration).first()
    assert config_atualizada.value == "1800"
    session.close()
