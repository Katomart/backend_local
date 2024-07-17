from abc import ABC, abstractmethod
import time
import json
import requests

from database import get_session
from servidor.models.courses import Platform, PlatformAuth, PlatformURL


def set_hotmart_urls():
    current_time = int(time.time())
    db_session = get_session()

    LOGIN = 'https://app-vlc.hotmart.com'
    



def set_platform_urls():
    pass

class Account(ABC):
    """
    Classe abstrata que representa uma conta genérica e gerencia a sessão de autenticação.

    Atributos e métodos desta classe devem ser estendidos por classes específicas
    de plataformas de cursos.
    """
    def __init__(self, account_id: int = 0, platform_id: int = 0):
        self.db_session = get_session()
        self.account_id = account_id
        self.platform_id = platform_id
        self.session = self.restart_requests_session()

    def get_current_time(self) -> int:
        """
        Retorna o tempo atual em segundos.
        """
        return int(time.time())

    def dump_json_data(self, data) -> str:
        """
        Serializa dados da conta em formato JSON.
        """
        return json.dumps(data, indent=4, ensure_ascii=False)

    def clone_main_session_as_requests(self) -> requests.Session:
        """
        Clona a sessão principal da conta para uso temporário em requisições
        que podem mudar dados da sessão principal.
        """
        new_session = requests.Session()
        new_session.headers.update(self.session.headers)
        new_session.cookies.update(self.session.cookies)

        return new_session

    def restart_requests_session(self) -> requests.Session:
        """
        Inicia uma sessão limpa da biblioteca requests com configurações básicas.
        """
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'})
        return session

    def __del__(self):
        self.logout()

    @abstractmethod
    def login(self):
        """
        Método abstrato para realizar o login na plataforma.
        """

    @abstractmethod
    def logout(self):
        """
        Método abstrato para realizar o logout na plataforma.
        """

    @abstractmethod
    def refresh_auth_token(self):
        """
        Método abstrato para renovar o token de acesso.
        """

    @abstractmethod
    def list_account_courses(self, get_extra_info: bool = False):
        """
        Método abstrato para obter os cursos associados à conta.
        """

    @abstractmethod
    def format_account_course(self, account_course: dict = None):
        """
        Método abstrato para formatar um curso ao padrão Módulo/Aula/Arquivos
        """

    @abstractmethod
    def get_course_information(self, course_id : str | int, other_data=None):
        """
        Método abstrato para obter informações de um curso específico.
        """

    @abstractmethod
    def get_course_modules(self, course_info: dict, other_data=None):
        """
        Método abstrato para obter os módulos de um curso.
        """

    @abstractmethod
    def get_course_module_info(self, course_info: dict, module_id: str | int, other_data=None):
        """
        Método abstrato para obter os módulos de um curso.
        """

    @abstractmethod
    def get_module_lessons(self, course_id: str | int, module_id: str | int, other_data=None):
        """
        Método abstrato para obter as lições de um módulo.
        """

    @abstractmethod
    def get_module_lesson_info(self, course_id: str | int, module_id: str | int, lesson_id: str | int, other_data=None):
        """
        Método abstrato para obter as lições de um módulo.
        """

    @abstractmethod
    def get_lesson_files(self, course_id: str | int, module_id: str | int, lesson_id: str | int, other_data=None):
        """
        Método abstrato para obter os arquivos de uma lição.
        """

    @abstractmethod
    def get_lesson_file_info(self, file_info: dict, other_data=None):
        """
        Método abstrato para baixar um arquivo.
        """
