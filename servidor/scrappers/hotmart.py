import time

from servidor.models.courses import PlatformAuth
from servidor.models.dblog import Log

from . import Account


class Hotmart(Account):
    """
    Representa um usuário da Hotmart, especializando a classe Account para
    lidar com as especificidades desta plataforma.
    """
    
    def __init__(self, account_id: int):
        """
        Inicializa uma instância de Hotmart com autenticação via ORM.

        :param account_id: Identificador da conta no banco de dados.
        :param session: Sessão SQLAlchemy para interações com o banco de dados.
        """
        super().__init__(account_id=account_id)
        self.platform_auth = self.load_platform_auth()
        self.session = self._restart_requests_session()
        self.login()

    def load_platform_auth(self):
        """
        Carrega as informações de autenticação da plataforma a partir do banco de dados.
        """
        return self.db_session.query(PlatformAuth).filter_by(id=self.account_id).one()

    def login(self):
        """
        Realiza o login na conta da Hotmart, autenticando o usuário e obtendo tokens de acesso.
        """
        if not self.platform_auth.token or self.platform_auth.token_expires_at < time.time():
            login_data = {
                'grant_type': 'password',
                'username': self.platform_auth.username,
                'password': self.platform_auth.password
            }
            response = self.session.post(self.platform_auth.login_url, data=login_data)

            if response.status_code != 200:
                self.db_session.add(Log(
                    level='error',
                    message=f'Erro ao acessar {response.url}: Status Code {response.status_code}'
                ))
                self.db_session.commit()
                raise Exception(f'Erro ao acessar {response.url}: Status Code {response.status_code}')

            response_data = response.json()
            self.platform_auth.token = response_data['access_token']
            self.platform_auth.token_expires_at = time.time() + response_data['expires_in']
            self.platform_auth.refresh_token = response_data['refresh_token']
            self.platform_auth.is_logged_in = True

            self.db_session.add(self.platform_auth)
            self.db_session.commit()

    def refresh_auth_token(self):
        """
        Renova o token de acesso da conta.
        """
        # Implementar a lógica de renovação de token aqui
        pass
