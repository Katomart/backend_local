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
        default_config_set = Configuration(configuration_group_name='setup', key='default_config_set', title='', value=True if has_set_config else False)
        db_session.add(default_config_set)

        # Path Stuff
        download_conf, char_conf = set_download_path()
        db_session.add(download_conf)
        db_session.add(char_conf)

        user_local_consent = Configuration(configuration_group_name='setup', key='setup_user_local_consent', title='', value=False, description='', value_type='bool', hidden=True)
        db_session.add(user_local_consent)

        last_execution = Configuration(configuration_group_name='setup', key='info_last_execution', title='', value='0', description='', value_type='int', hidden=True)
        db_session.add(last_execution)

        default_user_agent = Configuration(configuration_group_name='setup', key='default_user_agent', title='', value='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0', description='', value_type='str', hidden=False)
        db_session.add(default_user_agent)

        download_from_widevine = Configuration(configuration_group_name='setup', key='download_from_widevine', title='', value=False, description='', value_type='bool', hidden=False)
        db_session.add(download_from_widevine)

        cdm_path = Configuration(configuration_group_name='setup', key='setup_cdm_path', title='', value='', description='', value_type='str', hidden=False)
        db_session.add(cdm_path)

        use_original_media_name = Configuration(configuration_group_name='filesystem', key='use_original_media_name', title='', value=False, description='', value_type='bool', hidden=False)
        db_session.add(use_original_media_name)

        avoid_path_name_explosion_by_rooting = Configuration(configuration_group_name='filesystem', key='avoid_path_name_explosion_by_rooting', title='', value=True, description='', value_type='bool', hidden=False)
        db_session.add(avoid_path_name_explosion_by_rooting)

        avoid_path_name_shortening = Configuration(configuration_group_name='filesystem', key='avoid_path_name_shortening', title='', value=False, description='', value_type='bool', hidden=False)
        db_session.add(avoid_path_name_shortening)

        aggressive_path_name_shortening = Configuration(configuration_group_name='filesystem', key='aggressive_path_name_shortening', title='', value=False, description='', value_type='bool', hidden=False)
        db_session.add(aggressive_path_name_shortening)

        max_path_name_length = Configuration(configuration_group_name='filesystem', key='max_path_name_length', title='', value='45', description='', value_type='int', hidden=False)
        db_session.add(max_path_name_length)

        on_path_explode_fail_all = Configuration(configuration_group_name='filesystem', key='on_path_explode_fail_all', title='', value=False, description='', value_type='bool', hidden=False)
        db_session.add(on_path_explode_fail_all)

        on_path_explode_cut_course_name = Configuration(configuration_group_name='filesystem', key='on_path_explode_cut_course_name', title='', value=False, description='', value_type='bool', hidden=False)
        db_session.add(on_path_explode_cut_course_name)

        on_path_explode_cut_module_name = Configuration(configuration_group_name='filesystem', key='on_path_explode_cut_module_name', title='', value=True, description='', value_type='bool', hidden=False)
        db_session.add(on_path_explode_cut_module_name)

        on_path_explode_cut_lesson_name = Configuration(configuration_group_name='filesystem', key='on_path_explode_cut_lesson_name', title='', value=True, description='', value_type='bool', hidden=False)
        db_session.add(on_path_explode_cut_lesson_name)

        on_path_explode_cut_file_name = Configuration(configuration_group_name='filesystem', key='on_path_explode_cut_file_name', title='', value=True, description='', value_type='bool', hidden=False)
        db_session.add(on_path_explode_cut_file_name)

        on_path_explode_use_name_fallback = Configuration(configuration_group_name='filesystem', key='on_path_explode_use_name_fallback', title='', value=True, description='', value_type='bool', hidden=False)
        db_session.add(on_path_explode_use_name_fallback)

        enumerate_files = Configuration(configuration_group_name='filesystem', key='enumerate_files', title='', value=True, description='', value_type='bool', hidden=False)
        db_session.add(enumerate_files)

        media_name_fallback = Configuration(configuration_group_name='filesystem', key='media_name_fallback', title='', value='{file_type}', description='', value_type='str', hidden=True)
        db_session.add(media_name_fallback)

        use_custom_ffmpeg_arguments = Configuration(configuration_group_name='ffmpeg', key='use_custom_ffmpeg_arguments', title='', value=False, description='', value_type='bool', hidden=False)
        db_session.add(use_custom_ffmpeg_arguments)

        custom_ffmpeg_arguments = Configuration(configuration_group_name='ffmpeg', key='custom_ffmpeg_arguments', title='', value='-i,"{input_file}",-c:v,libx264,-crf,23,-c:a,aac,-b:a,192k,"{output_file}"', description='', value_type='str', hidden=False)
        db_session.add(custom_ffmpeg_arguments)

        use_fast_ffmpeg_hls_conversion = Configuration(configuration_group_name='ffmpeg', key='fast_ffmpeg_hls_conversion', title='', value=False, description='', value_type='bool', hidden=False)
        db_session.add(use_fast_ffmpeg_hls_conversion)

        fast_ffmpeg_hls_conversion_arguments = Configuration(configuration_group_name='ffmpeg', key='fast_ffmpeg_hls_conversion_arguments', title='', value='-i,"{input_file}",-c,copy,"{output_file}"', description='', value_type='str', hidden=False)
        db_session.add(fast_ffmpeg_hls_conversion_arguments)

        video_download_format = Configuration(configuration_group_name='ffmpeg', key='video_format', title='', value='mp4', description='', value_type='select', hidden=False)
        db_session.add(video_download_format)

        download_subtitles = Configuration(configuration_group_name='download', key='download_subtitles', title='', value=False, description='', value_type='bool', hidden=False)
        db_session.add(download_subtitles)

        subtitle_language = Configuration(configuration_group_name='download', key='subtitle_language', title='', value='pt', description='', value_type='select', hidden=False)
        db_session.add(subtitle_language)

        download_quality = Configuration(configuration_group_name='download', key='video_quality', title='', value='1080p', description='', value_type='select', hidden=False)
        db_session.add(download_quality)

        download_quality_fallback = Configuration(configuration_group_name='download', key='video_quality_fallback', title='', value='best', description='', value_type='select', hidden=False)
        db_session.add(download_quality_fallback)

        download_threads = Configuration(configuration_group_name='download', key='segment_threads', title='', value='1', description='', value_type='int', hidden=True)
        db_session.add(download_threads)

        download_maximum_retries_per_file = Configuration(configuration_group_name='download', key='max_retries_per_file', title='', value='5', description='', value_type='int', hidden=False)
        db_session.add(download_maximum_retries_per_file)

        stream_prefer_ytdlp = Configuration(configuration_group_name='download', key='stream_prefer_ytdlp', title='', value=True, description='', value_type='bool', hidden=False)
        db_session.add(stream_prefer_ytdlp)

        download_await_time = Configuration(configuration_group_name='download', key='pause_time_between_files', title='', value='5', description='', value_type='int', hidden=False)
        db_session.add(download_await_time)

        download_await_on_fail = Configuration(configuration_group_name='download', key='pause_on_fail', title='', value='5', description='', value_type='int', hidden=False)
        db_session.add(download_await_on_fail)

        reauth_on_fail = Configuration(configuration_group_name='download', key='abort_on_fail', title='', value=False, description='', value_type='bool', hidden=False)
        db_session.add(reauth_on_fail)

        reauth_fail_threshold = Configuration(configuration_group_name='download', key='abort_on_fail_threshold', title='', value='3', description='', value_type='int', hidden=False)
        db_session.add(reauth_fail_threshold)

        download_stream_segment_in_order = Configuration(configuration_group_name='download', key='stream_segment_in_order', title='', value=True, description='', value_type='bool', hidden=False)
        db_session.add(download_stream_segment_in_order)

        downloaded_videos_from_html_files = Configuration(configuration_group_name='download', key='videos_from_text_files', title='', value=False, description='', value_type='bool', hidden=False)
        db_session.add(downloaded_videos_from_html_files)

        # API CONFIGURATION
        allow_remote_api_communication = Configuration(configuration_group_name='remote', key='allow_api_communication', title='', value=False, description='', value_type='bool', hidden=False)
        db_session.add(allow_remote_api_communication)

        unhashed_hwid, hashed_hwid = generate_hwid()
        public_hwid = Configuration(configuration_group_name='remote', key='public_hwid', title='', value=hashed_hwid, description='', value_type='str', hidden=False)
        db_session.add(public_hwid)
        registration_uuid = Configuration(configuration_group_name='remote', key='registration_uuid', title='', value=unhashed_hwid, description='', value_type='str', hidden=True)
        db_session.add(registration_uuid)
        public_pgp_key = Configuration(configuration_group_name='remote', key='public_pgp_key', title='', value='Cadastrar', description='', value_type='str', hidden=False)
        db_session.add(public_pgp_key)
        api_username = Configuration(configuration_group_name='remote', key='api_username', title='', value='Cadastrar', description='', value_type='str', hidden=False)
        db_session.add(api_username)
        api_password = Configuration(configuration_group_name='remote', key='api_password', title='', value='Cadastrar', description='', value_type='str', hidden=False)
        db_session.add(api_password)
        api_token = Configuration(configuration_group_name='remote', key='api_token', title='', value='Cadastrar', description='', value_type='str', hidden=False)
        db_session.add(api_token)
        api_consent = Configuration(configuration_group_name='remote', key='api_consent', title='', value=False, description='', value_type='bool', hidden=True)
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

    download_conf = Configuration(configuration_group_name='', key='dl_storage_path', title='', value=download_path, description='', value_type='str', hidden=False, editable=True)
    char_conf = Configuration(configuration_group_name='', key='dl_remaining_save_length', title='', value=remaining, description='', value_type='int', hidden=False, editable=False)

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
    home_conf = Configuration(configuration_group_name='remote', key='remote_home_address', title='', value=home_address, description='', value_type='str', hidden=False, editable=False)
    repo_conf = Configuration(configuration_group_name='remote', key='remote_repository_url', title='', value=repo_url, description='', value_type='str', hidden=False, editable=False)
    dev_conf = Configuration(configuration_group_name='remote', key='remote_development_org', title='', value=development_org, description='', value_type='str', hidden=False, editable=False)

    return home_conf, repo_conf, dev_conf
