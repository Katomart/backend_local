import pathlib

from setup_utils import get_execution_path, get_operating_system, remaining_path_length, read_and_delete_config_file

from .database import get_session

from servidor.models.configs import Configuration
from servidor.models.courses import PlatformAuth, Platform, Course, Module, Lesson, File
from servidor.models.dblog import Log

from .sec import generate_hwid


class Config:
    SECRET_KEY = 'katomart'
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = 'sqlite:///katomart.sec'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///katomart.sec'
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = 'sqlite:///katomart.sec'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///katomart.sec'
    SECRET_KEY = 'katomart'


SERVER_PATH = get_execution_path()
OPERATING_SYSTEM = get_operating_system()

def set_config_from_setup() -> None:
    """Set the configuration from the setup
    """
    setup_config = read_and_delete_config_file()

    # TODO
    if not setup_config:
        return

    db_session = get_session()

    # Incluir no front uma mensagem de que as configurações foram definidas no setup
    # Para as alterar, o recomendado é deletar o arquivo katomart.sec e executar o setup novamente.
    for key, value in setup_config.items():
        config = Configuration(configuration_group_name='setup', key=key, title='Esta configuração foi denida no setup!', value= True if value == 1 else False if value == 0 else value)
        db_session.add(config)

    db_session.commit()

    return True

def has_default_configs_set():
    """Check if the default configurations have already been set in the database."""
    db_session = get_session()
    config_exists = db_session.query(Configuration).filter_by(key='default_config_set').first()
    return config_exists is not None

def set_default_config() -> None:
    """Set the default application configuration
    """
    if not has_default_configs_set():
        # DEFAULT CONFIGURATION
        has_set_config= set_config_from_setup()
        db_session = get_session()
        default_config_set = Configuration(configuration_group_name='setup', key='default_config_set', title='Configurações Padrões Definidas?', description='Se este valor for definido para falso, o programa tentará ler um arquivo chamado "configs.json" ao ser inicializado.',  value=True if has_set_config else False)
        db_session.add(default_config_set)

        # Path Stuff
        download_conf, char_conf = set_download_path()
        db_session.add(download_conf)
        db_session.add(char_conf)

        user_local_consent = Configuration(configuration_group_name='setup', key='setup_user_local_consent', title='O usuário leu e concordou com os termos de uso.', description='Define se o aplicativo se torna funcional ou não.',  value=False, value_type='bool', hidden=True)
        db_session.add(user_local_consent)

        last_execution = Configuration(configuration_group_name='setup', key='info_last_execution', title='Última execução do Software.', description='A data que o usuário utilizou o programa pela última vez (teve seu front acessado).',  value='0', value_type='int', hidden=True)
        db_session.add(last_execution)

        default_user_agent = Configuration(configuration_group_name='setup', key='default_user_agent', title='Navegador a ser simulado (User-Agent)', description='Servidores web podem controlar a exibição de informações com base no navegador a ser utilizado. O valor aqui contido define qual navegador o aplicativo tenta se passar por.',  value='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0', value_type='str', hidden=False)
        db_session.add(default_user_agent)

        default_mobile_user_agent = Configuration(configuration_group_name='setup', key='default_mobile_user_agent', title='Navegador MOBILE a ser simulado (User-Agent)', description='Servidores web podem controlar a exibição de informações com base no navegador a ser utilizado. O valor aqui contido define qual navegador o aplicativo tenta se passar por (versão mobile).',  value='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0', value_type='str', hidden=False)
        db_session.add(default_mobile_user_agent)

        download_from_widevine = Configuration(configuration_group_name='setup', key='download_from_widevine', title='Baixar conteúdo protegido pelo Widevine?', description='Widevine é uma tecnologia de proteção de conteúdo. Para realizar o download de forma efetiva, o usuário deve pesquisar sobre CDM. Não tente usar CDM genérica, nem fique chorando, extraia de um celular Android ou desista, é perca de tempo.',  value=False, value_type='bool', hidden=False)
        db_session.add(download_from_widevine)

        cdm_path = Configuration(configuration_group_name='setup', key='setup_cdm_path', title='Caminho da CDM a ser utilizada para o Widevine', description='Deve ser o caminho completo para a pasta. Se você não tem uma, não adianta preencher aqui. Não existe valor mágico.',  value='', value_type='str', hidden=False)
        db_session.add(cdm_path)

        use_original_media_name = Configuration(configuration_group_name='filesystem', key='use_original_media_name', title='Usar nome original das mídias?', description='Se ativada, o programa irá optar por salvar os arquivos utilizando o nome original do arquivo ENVIADO PELO PROFESSOR À PLATAFORMA. Muitas vezes estes nomes não tem sentido algum, sendo algo como "m!a1.mp4", ou, "742194721941.png". Lembre-se: O programa padroniza os arquivos em nome do curso/nome do módulo/nome da aula, os nomes são as pastas!',  value=False, value_type='bool', hidden=False)
        db_session.add(use_original_media_name)

        avoid_path_name_explosion_by_rooting = Configuration(configuration_group_name='filesystem', key='avoid_path_name_explosion_by_rooting', title='Evitar problemas de path utilizando a raiz do disco (mover os arquivos relevantes para a raiz antes de tratar o nome e após isso, mover para o destino final aplicando um cálculo com base no total de caracteres. Ativar se optar por utilizar o nome original de mídias!)', description='Para utilizar esta opção, você deve executar o Katomart como admin na maioria das vezes, ou, permitir que todos tenham acesso à raiz do seu disco. Recomendado deixar ativado a menos que o seu curso utilize nomes pequenos e a opção de nomes originais esteja desativada.',  value=True, value_type='bool', hidden=False)
        db_session.add(avoid_path_name_explosion_by_rooting)

        avoid_path_name_shortening = Configuration(configuration_group_name='filesystem', key='avoid_path_name_shortening', title='Evitar encurtar nome de Módulo/Aula', description='Se ativado, o programa tentará encurtar apenas o nome do curso e o nome de arquivos para tentar salvar todo o conteúdo.',  value=False, value_type='bool', hidden=False)
        db_session.add(avoid_path_name_shortening)

        aggressive_path_name_shortening = Configuration(configuration_group_name='filesystem', key='aggressive_path_name_shortening', title='Sempre encurtar os nomes', description='Se ativado, o programa sempre irá encurtar os nomes dos caminhos/arquivos até o limite definido abaixo.',  value=False, value_type='bool', hidden=False)
        db_session.add(aggressive_path_name_shortening)

        max_course_name_length = Configuration(configuration_group_name='filesystem', key='max_course_name_length', title='Tamanho máximo para o nome da pasta do curso', description='Enumerador é um tamanho fixo que é contabilizado com o restante do nome. Esta configuração é utilizada quando é necessário encurtar algo.',  value='45', value_type='int', hidden=False)
        db_session.add(max_course_name_length)

        max_module_name_length = Configuration(configuration_group_name='filesystem', key='max_module_name_length', title='Tamanho máximo para o nome da pasta do módulo', description='Enumerador é um tamanho fixo que é contabilizado com o restante do nome. Esta configuração é utilizada quando é necessário encurtar algo.',  value='45', value_type='int', hidden=False)
        db_session.add(max_module_name_length)

        max_lesson_name_length = Configuration(configuration_group_name='filesystem', key='max_lesson_name_length', title='Tamanho máximo para o nome da pasta da aula', description='Enumerador é um tamanho fixo que é contabilizado com o restante do nome. Esta configuração é utilizada quando é necessário encurtar algo.',  value='45', value_type='int', hidden=False)
        db_session.add(max_lesson_name_length)

        max_file_name_length = Configuration(configuration_group_name='filesystem', key='max_file_name_length', title='Tamanho máximo para o nome do arquivo', description='Enumerador é um tamanho fixo que é contabilizado com o restante do nome. Esta configuração é utilizada quando é necessário encurtar algo.',  value='45', value_type='int', hidden=False)
        db_session.add(max_file_name_length)

        create_folder_for_attachments = Configuration(configuration_group_name='filesystem', key='create_folder_for_attachments', title='Criar uma pasta para Anexos da aula', description='Se ativo, o programa terá o comportamento padrão, onde as pastas de aulas terão uma pasta "Anexos" com os arquivos. Se desativado, os anexos ficarão localizados junto dos arquivos de vídeo e/ou textuais.',  value=True, value_type='bool', hidden=False)
        db_session.add(create_folder_for_attachments)

        on_path_explode_fail_all = Configuration(configuration_group_name='filesystem', key='on_path_explode_fail_all', title='Interromper o download por completo ocorra um erro relacionado ao caminho', description='Se o caminho final de algum arquivo for muito extenso, o programa parará de executar',  value=False, value_type='bool', hidden=False)
        db_session.add(on_path_explode_fail_all)

        on_path_explode_cut_course_name = Configuration(configuration_group_name='filesystem', key='on_path_explode_cut_course_name', title='Encurtar o nome do Curso em caso de erro', description='O nome do curso será reduzido drasticamente caso ocorra algum erro ao salvar um arquivo.',  value=False, value_type='bool', hidden=False)
        db_session.add(on_path_explode_cut_course_name)

        on_path_explode_cut_module_name = Configuration(configuration_group_name='filesystem', key='on_path_explode_cut_module_name', title='Encurtar o nome do Módulo em caso de erro', description='O nome do Módulo será reduzido drasticamente caso ocorra algum erro ao salvar um arquivo.',  value=True, value_type='bool', hidden=False)
        db_session.add(on_path_explode_cut_module_name)

        on_path_explode_cut_lesson_name = Configuration(configuration_group_name='filesystem', key='on_path_explode_cut_lesson_name', title='Encurtar o nome da Aula em caso de erro', description='O nome da Aula será reduzida drasticamente caso ocorra algum erro ao salvar um arquivo.',  value=True, value_type='bool', hidden=False)
        db_session.add(on_path_explode_cut_lesson_name)

        on_path_explode_cut_file_name = Configuration(configuration_group_name='filesystem', key='on_path_explode_cut_file_name', title='Encurtar o nome do Arquivo em caso de erro', description='Recomendado. O nome do Arquivo será reduzido drasticamente caso ocorra um erro ao o salvar.',  value=True, value_type='bool', hidden=False)
        db_session.add(on_path_explode_cut_file_name)

        on_path_explode_use_name_fallback = Configuration(configuration_group_name='filesystem', key='on_path_explode_use_name_fallback', title='Utilizar um Fallback de nome caso ocorra um erro de salvamento', description='Se o salvamente de um arquivo resultar em erro, o programa utilizará um nome genérico para garantir o salvamento do conteúdo, tal como "Curso", "Módulo", "Aula", "Arquivo".',  value=True, value_type='bool', hidden=False)
        db_session.add(on_path_explode_use_name_fallback)

        enumerate_files = Configuration(configuration_group_name='filesystem', key='enumerate_files', title='Enumerar conteúdo', description='Esta opção define se os arquivos gerados (e também pastas) terão números no começo para organização (1. Nome, 2. Nome, 3. Nome).',  value=True, value_type='bool', hidden=False)
        db_session.add(enumerate_files)

        use_custom_ffmpeg_arguments = Configuration(configuration_group_name='ffmpeg', key='use_custom_ffmpeg_arguments', title='Utilizar argumentos customizados no FFMPEG para encodar o conteúdo baixado', description='Se ativado, o programa usara o comando que for definido no ffmpeg, isso pode aumentar muito o tempo de download, recomendado utilizar um script externo para o processamento de arquivos.',  value=False, value_type='bool', hidden=False)
        db_session.add(use_custom_ffmpeg_arguments)

        custom_ffmpeg_arguments = Configuration(configuration_group_name='ffmpeg', key='custom_ffmpeg_arguments', title='Argumentos para o FFMPEG', description='Mantenha o padrão. o valor "{input_file}" e o valor "{output_file}" são obrigatórios, e os demais argumentos devem ser separados por ponto e vírgula (;). input_file se refere ao arquivo de entrada, e output_file se refere ao arquivo de saída, ambos são gerenciados pelo programa.',  value='-i;"{input_file}";-c:v;libx264;-crf;23;-c:a;aac;-b:a;192k;"{output_file}"', value_type='str', hidden=False)
        db_session.add(custom_ffmpeg_arguments)

        use_fast_ffmpeg_hls_conversion = Configuration(configuration_group_name='ffmpeg', key='fast_ffmpeg_hls_conversion', title='Concatenar stream de forma rápida pelo FFMPEG', description='Utiliza o FFMPEG para a rápida junção de segmentos de Stream de vídeo.',  value=False, value_type='bool', hidden=False)
        db_session.add(use_fast_ffmpeg_hls_conversion)

        fast_ffmpeg_hls_conversion_arguments = Configuration(configuration_group_name='ffmpeg', key='fast_ffmpeg_hls_conversion_arguments', title='Comando para a concatenação rápida', description='Mantenha o padrão. o valor "{input_file}" e o valor "{output_file}" são obrigatórios, e os demais argumentos devem ser separados por ponto e vírgula (;). input_file se refere ao arquivo de entrada, e output_file se refere ao arquivo de saída, ambos são gerenciados pelo programa.',  value='-i;"{input_file}";-c;copy;"{output_file}"', value_type='str', hidden=False)
        db_session.add(fast_ffmpeg_hls_conversion_arguments)

        download_videos = Configuration(configuration_group_name='download', key='download_videos', title='Se vídeos deverão ser baixados', description='Para definir os players, vá para a seção de definição de conteúdo.',  value=True, value_type='bool', hidden=False)
        db_session.add(download_videos)

        download_attachments = Configuration(configuration_group_name='download', key='download_attachments', title='Se anexos deverão ser baixados', description='Para controlar os tipos e possíveis conversões, vá até a seção de definição de conteúdo.',  value=True, value_type='bool', hidden=False)
        db_session.add(download_attachments)

        video_download_format = Configuration(configuration_group_name='download', key='video_format', title='Formato do vídeo a ser salvo', description='Utilizar a extensão, valores suportados: mp4, avi, mov, webm, gif',  value='mp4', value_type='str', hidden=False)
        db_session.add(video_download_format)

        video_download_quality = Configuration(configuration_group_name='download', key='video_download_quality', title='Qualidade do vídeo a ser baixada', description='O recomendado é 1080. Não utilizar "p" (por exemplo, 1080p). Você pode listar várias qualidades, e também os valores especiais "all" para baixar todas as qualidades, "worst" para baixar apenas a pior qualidade do vídeo, "best" para baixar a melhor qualidade disponível, "audio" para manter apenas o aúdio dos vídeos. Você pode passar várias qualidades separadas por ;, e todas serão baixadas conforme solicitado. Valores comuns: 240, 360, 480, 720, 1080, 4000, 8000. Se nenhum valor for encontrado, ou o formato for inválido, o programa optará pela melhor disponível.',  value='1080', value_type='int', hidden=False)
        db_session.add(video_download_quality)

        download_subtitles = Configuration(configuration_group_name='download', key='download_subtitles', title='Baixar legendas', description='Se as legendas devem ser baixadas',  value=False, value_type='bool', hidden=False)
        db_session.add(download_subtitles)

        subtitle_language = Configuration(configuration_group_name='download', key='subtitle_language', title='Idioma da Legenda', description='Utilizar a sigla unificada i18n (pt,en,es,etc), você pode separar os valores com ;. se você incluir o valor "all", todas as legendas encontradas serão baixadas. Se o campo estiver vazio, ou seu valor for "none", nenhuma legenda será baixada.',  value='pt;en', value_type='str', hidden=False)
        db_session.add(subtitle_language)

        download_threads = Configuration(configuration_group_name='download', key='segment_threads', title='Quantidade de threads para baixar arquivos', description='Basicamente, pensa que o download é uma contagem de 1 até o 100, se você utilizar 4, você pega o valor total e divide por 4, resultando em 25, então criam-se 4 downloads do 1 até o 25, e todas as contagens são feitas ao mesmo tempo. Valores muito altos vão causar bloqueios de rede, nunca ultrapassar 15. Recomendado: 3',  value='3', value_type='int', hidden=True)
        db_session.add(download_threads)

        download_maximum_retries_per_file = Configuration(configuration_group_name='download', key='max_retries_per_file', title='Tentativas por arquivo', description='Quantidad de tentativas por arquivo que deu erro para baixar',  value='5', value_type='int', hidden=False)
        db_session.add(download_maximum_retries_per_file)

        stream_prefer_ytdlp = Configuration(configuration_group_name='download', key='prefer_ytdlp', title='Preferir utilizar o YTDLP onde possível', description='Ao invés de utilizar o algoritmo proprietário do desenvolvedor deste software, utiliza-se o ytdlp onde for possível. *O desenvolvedor também ajuda a manter o youtube-dlp funcionando para todos em sites variados, o downloader proprietário bufferiza arquivo para a memória, assim economizando a vida útil do seu disco de armazenamento, porém, requer uma quantidade alta de RAM, e no momento o código proprietário foi publicado apenas para um grupo seleto de desenvolvedores.',  value=True, value_type='bool', hidden=False)
        db_session.add(stream_prefer_ytdlp)

        scrap_await_time = Configuration(configuration_group_name='download', key='scrap_await_time', title='Tempo de espera entre a descoberta de arquivos (novas requisições, em segundos)', description='Recomenda-se deixar um intervalo de pelo menos 3 segundos entre as requisições de descoberta, isso ajuda a evitar bloqueios por automação. Note que o valor que você inserir aqui será considerado o valor máximo, e um valor aleatório será utilizado dentro dele.',  value='3', value_type='int', hidden=False)
        db_session.add(scrap_await_time)

        download_await_time = Configuration(configuration_group_name='download', key='download_await_time', title='Tempo de espera entre downloads (segundos)', description='Recomenda-se deixar um intervalo de pelo 10 segundos, porém isso depende do restante das demais configurações e a velocidade da sua internet. Quanto mais rápido, maior deve ser este intervalo para sua segurança contra bloqueios, e quanto mais lento, menor este intervalo deve ser',  value='5', value_type='int', hidden=False)
        db_session.add(download_await_time)

        download_await_on_fail = Configuration(configuration_group_name='download', key='download_await_on_fail', title='Tempo de espera antes de tentar baixar um arquivo novamente (em caso de falha, segundos)', description='Recomendado ser bem leniente e esperar pelo menos 60 segundos. Caso a sua autenticação tenha expirado, o downloader irá o avisar.',  value='60', value_type='int', hidden=False)
        db_session.add(download_await_on_fail)

        download_videos_from_html_files = Configuration(configuration_group_name='download', key='download_videos_from_html_files', title='Escanear e baixar vídeos de arquivos textuais', description='Ao ativar, o programa tentará localizar e realizar o download de todos os vídeos dentro de quaisquer arquivos textuais salvos.',  value=True, value_type='bool', hidden=False)
        db_session.add(download_videos_from_html_files)

        # TODO: Definir configurações do YTDLP
        # TODO: Definir a seção de configurações de fonte e tipo de conteúdo.

        # API CONFIGURATION
        allow_remote_api_communication = Configuration(configuration_group_name='remote', key='allow_api_communication', title='',  value=False, value_type='bool', hidden=False)
        db_session.add(allow_remote_api_communication)

        unhashed_hwid, hashed_hwid = generate_hwid()
        public_hwid = Configuration(configuration_group_name='remote', key='public_hwid', title='',  value=hashed_hwid, value_type='str', hidden=False)
        db_session.add(public_hwid)
        registration_uuid = Configuration(configuration_group_name='remote', key='registration_uuid', title='',  value=unhashed_hwid, value_type='str', hidden=True)
        db_session.add(registration_uuid)
        public_pgp_key = Configuration(configuration_group_name='remote', key='public_pgp_key', title='',  value='Cadastrar', value_type='str', hidden=False)
        db_session.add(public_pgp_key)
        api_username = Configuration(configuration_group_name='remote', key='api_username', title='',  value='Cadastrar', value_type='str', hidden=False)
        db_session.add(api_username)
        api_password = Configuration(configuration_group_name='remote', key='api_password', title='',  value='Cadastrar', value_type='str', hidden=False)
        db_session.add(api_password)
        api_token = Configuration(configuration_group_name='remote', key='api_token', title='',  value='Cadastrar', value_type='str', hidden=False)
        db_session.add(api_token)
        api_consent = Configuration(configuration_group_name='remote', key='api_consent', title='',  value=False, value_type='bool', hidden=True)
        db_session.add(api_consent)

        # Home Stuff
        home_conf, repo_conf, dev_conf = set_home_address()
        db_session.add(home_conf)
        db_session.add(repo_conf)
        db_session.add(dev_conf)

        db_session.commit()

def set_download_path(download_path: pathlib.Path=pathlib.Path(SERVER_PATH),
                       user_os: str=OPERATING_SYSTEM) -> tuple[Configuration, Configuration]:
    """Set the download path for the application
    Params:
        download_path (pathlib.Path): The path to download the files to
        user_os (str): The operating system name
    Returns:
        tuple[Configuration, Configuration]: The download path and the remaining path length
    """
    download_path = pathlib.Path(download_path) \
    .resolve() \
    .as_posix() \
    + '/' \
    + 'Cursos'

    remaining = remaining_path_length(pathlib.Path(download_path), user_os)

    download_conf = Configuration(configuration_group_name='', key='dl_storage_path', title='',  value=download_path, value_type='str', hidden=False, editable=True)
    char_conf = Configuration(configuration_group_name='', key='dl_remaining_save_length', title='',  value=remaining, value_type='int', hidden=False, editable=False)

    return download_conf, char_conf

def set_home_address(home_address: str='katomart.com',
                      repo_url: str='https://github.com/katomaro/katomart',
                      development_org: str='https://github.com/katomart') -> tuple[Configuration, Configuration, Configuration]:
    """Set the home address for the application
    Params:
        home_address (str): The adress to which the application should phone to
        repo_url (str): The URL of the repository
        development_org (str): The URL of the development organization
    Returns:
        tuple[Configuration, Configuration, Configuration]: The home address, the repository URL, and the development organization
    """
    home_conf = Configuration(configuration_group_name='remote', key='remote_home_address', title='',  value=home_address, value_type='str', hidden=False, editable=False)
    repo_conf = Configuration(configuration_group_name='remote', key='remote_repository_url', title='',  value=repo_url, value_type='str', hidden=False, editable=False)
    dev_conf = Configuration(configuration_group_name='remote', key='remote_development_org', title='',  value=development_org, value_type='str', hidden=False, editable=False)

    return home_conf, repo_conf, dev_conf
