from abc import ABC, abstractmethod
import time
import json
import requests


class Account(ABC):
    """
    Classe abstrata que representa uma conta genérica e gerencia a sessão de autenticação.

    Atributos e métodos desta classe devem ser estendidos por classes específicas
    de plataformas de cursos.
    """
    def __init__(self, account_id: int = 0, platform_id: int = 0):
        self.account_id = account_id
        self.platform_id = platform_id
        self.session = self._restart_requests_session()

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

    def clone_main_session(self) -> requests.Session:
        """
        Clona a sessão principal da conta para uso temporário em requisições
        que podem mudar dados da sessão principal.
        """
        new_session = requests.Session()
        new_session.headers.update(self.session.headers)
        new_session.cookies.update(self.session.cookies)

        new_session.auth = self.session.auth

        if self.session.proxies:
            new_session.proxies.update(self.session.proxies)
        new_session.verify = self.session.verify

        return new_session

    def __del__(self):
        self.logout()

    def _restart_requests_session(self) -> requests.Session:
            """
            Inicia uma sessão limpa da biblioteca requests com configurações básicas.
            """
            session = requests.Session()
            session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'})
            return session

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
    def list_account_products(self, get_extra_info: bool = False):
        """
        Método abstrato para obter os produtos associados à conta.
        """

    @abstractmethod
    def format_account_product(self, account_products: dict = None):
        """
        Método abstrato para formatar um produto ao padrão Módulo/Aula/Arquivos
        """

    @abstractmethod
    def get_product_information(self, product_id : str | int, other_data=None):
        """
        Método abstrato para obter informações de um produto específico.
        """

    @abstractmethod
    def get_content_modules(self, product_info: dict, other_data=None):
        """
        Método abstrato para obter os módulos de um produto.
        """

    @abstractmethod
    def get_content_module_info(self, product_info: dict, module_id: str | int, other_data=None):
        """
        Método abstrato para obter os módulos de um produto.
        """

    @abstractmethod
    def get_module_lessons(self, content_id: str | int, module_id: str | int, other_data=None):
        """
        Método abstrato para obter as lições de um módulo.
        """

    @abstractmethod
    def get_module_lesson_info(self, content_id: str | int, module_id: str | int, lesson_id: str | int, other_data=None):
        """
        Método abstrato para obter as lições de um módulo.
        """

    @abstractmethod
    def get_lesson_files(self, content_id: str | int, module_id: str | int, lesson_id: str | int, other_data=None):
        """
        Método abstrato para obter os arquivos de uma lição.
        """

    @abstractmethod
    def get_lesson_file_info(self, file_info: dict, other_data=None):
        """
        Método abstrato para baixar um arquivo.
        """
