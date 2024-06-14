import pathlib

from setup_utils import get_execution_path, get_operating_system, remaining_path_length, read_and_delete_config_file

from .database import db_session

from servidor.models.configs import Configuration
from servidor.models.courses import PlatformAuth, Platform, Course, Module, Lesson, File

from .sec import generate_hwid


class Config:
    SECRET_KEY = 'katomart'
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = 'sqlite:///dev.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = 'sqlite:///katomart.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///katomart.db'
    SECRET_KEY = 'katomart'


SERVER_PATH = get_execution_path()
OPERATING_SYSTEM = get_operating_system()

def set_config_from_setup() -> None:
    """Set the configuration from the setup
    """
    setup_config = read_and_delete_config_file()

    if not setup_config:
        return

    for key, value in setup_config.items():
        config = Configuration(key=key, value=value)
        db_session.add(config)

    db_session.commit()

    return True

def has_default_configs_set():
    """Check if the default configurations have already been set in the database."""
    # Assuming there's a specific key in your Configuration table that is only added by set_default_configs
    config_exists = db_session.query(Configuration).filter_by(key='default_config_set').first()
    return config_exists is not None

def set_default_config() -> None:
    """Set the default application configuration
    """
    if not has_default_configs_set():
        # DEFAULT CONFIGURATION
        set_config_from_setup()

        default_config_set = Configuration(key='default_config_set', value='True')
        db_session.add(default_config_set)

        # Path Stuff
        download_conf, char_conf = set_download_path()
        db_session.add(download_conf)
        db_session.add(char_conf)

        # Home Stuff
        home_conf, repo_conf, dev_conf = set_home_address()
        db_session.add(home_conf)
        db_session.add(repo_conf)
        db_session.add(dev_conf)

        user_local_consent = Configuration(key='user_local_consent', value='False')
        db_session.add(user_local_consent)

        user_local_consent_date = Configuration(key='user_local_consent_date', value='0')
        db_session.add(user_local_consent_date)

        last_execution = Configuration(key='last_execution', value='0')
        db_session.add(last_execution)

        enable_local_katomart_api = Configuration(key='enable_local_katomart_api', value='False')
        db_session.add(enable_local_katomart_api)

        enable_local_katomart_user_registration = Configuration(key='enable_local_katomart_user_registration', value='False')
        db_session.add(enable_local_katomart_user_registration)

        use_original_media_name = Configuration(key='use_original_media_name', value='False')
        db_session.add(use_original_media_name)

        avoid_path_name_explosion_by_rooting = Configuration(key='avoid_path_name_explosion_by_rooting', value='True')
        db_session.add(avoid_path_name_explosion_by_rooting)

        avoid_path_name_shortening = Configuration(key='avoid_path_name_shortening', value='False')
        db_session.add(avoid_path_name_shortening)

        aggressive_path_name_shortening = Configuration(key='aggressive_path_name_shortening', value='False')
        db_session.add(aggressive_path_name_shortening)

        max_path_name_length = Configuration(key='max_path_name_length', value='45')
        db_session.add(max_path_name_length)

        on_path_explode_fail_all = Configuration(key='on_path_explode_fail_all', value='False')
        db_session.add(on_path_explode_fail_all)

        on_path_explode_cut_course_name = Configuration(key='on_path_explode_cut_course_name', value='False')
        db_session.add(on_path_explode_cut_course_name)

        on_path_explode_cut_module_name = Configuration(key='on_path_explode_cut_module_name', value='True')
        db_session.add(on_path_explode_cut_module_name)

        on_path_explode_cut_lesson_name = Configuration(key='on_path_explode_cut_lesson_name', value='True')
        db_session.add(on_path_explode_cut_lesson_name)

        on_path_explode_cut_file_name = Configuration(key='on_path_explode_cut_file_name', value='True')
        db_session.add(on_path_explode_cut_file_name)

        on_path_explode_use_name_fallback = Configuration(key='on_path_explode_use_name_fallback', value='True')
        db_session.add(on_path_explode_use_name_fallback)

        use_custom_ffmpeg_arguments = Configuration(key='use_custom_ffmpeg_arguments', value='False')
        db_session.add(use_custom_ffmpeg_arguments)

        custom_ffmpeg_arguments = Configuration(key='custom_ffmpeg_arguments', value='-i,"{input_file}",-c:v,libx264,-crf,23,-c:a,aac,-b:a,192k,"{output_file}"')
        db_session.add(custom_ffmpeg_arguments)

        use_fast_ffmpeg_hls_conversion = Configuration(key='fast_ffmpeg_hls_conversion', value='False')
        db_session.add(use_fast_ffmpeg_hls_conversion)

        fast_ffmpeg_hls_conversion_arguments = Configuration(key='fast_ffmpeg_hls_conversion_arguments', value='-i,"{input_file}",-c,copy,"{output_file}"')
        db_session.add(fast_ffmpeg_hls_conversion_arguments)

        media_name_fallback = Configuration(key='media_name_fallback', value='{file_type}')
        db_session.add(media_name_fallback)

        enumerate_files = Configuration(key='enumerate_files', value='True')
        db_session.add(enumerate_files)

        download_subtitles = Configuration(key='download_subtitles', value='False')
        db_session.add(download_subtitles)

        subtitle_language = Configuration(key='subtitle_language', value='pt')
        db_session.add(subtitle_language)

        download_quality = Configuration(key='download_quality', value='1080p')
        db_session.add(download_quality)

        download_quality_fallback = Configuration(key='download_quality_fallback', value='best')
        db_session.add(download_quality_fallback)

        video_download_format = Configuration(key='video_download_format', value='mp4')
        db_session.add(video_download_format)

        download_threads = Configuration(key='download_threads', value='1')
        db_session.add(download_threads)

        stream_download_threads = Configuration(key='stream_download_threads', value='5')
        db_session.add(stream_download_threads)

        stream_prefer_ytdlp = Configuration(key='stream_prefer_ytdlp', value='False')
        db_session.add(stream_prefer_ytdlp)

        download_maximum_retries_per_file = Configuration(key='download_maximum_retries_per_file', value='5')
        db_session.add(download_maximum_retries_per_file)

        download_await_time = Configuration(key='download_await_time', value='5')
        db_session.add(download_await_time)

        download_await_on_fail = Configuration(key='download_await_on_fail', value='5')
        db_session.add(download_await_on_fail)

        reauth_on_fail = Configuration(key='reauth_on_fail', value='False')
        db_session.add(reauth_on_fail)

        reauth_fail_threshold = Configuration(key='reauth_fail_threshold', value='3')
        db_session.add(reauth_fail_threshold)

        reauth_await_time = Configuration(key='reauth_await_time', value='180')
        db_session.add(reauth_await_time)

        reauth_maximum_retries = Configuration(key='reauth_maximum_retries', value='2')
        db_session.add(reauth_maximum_retries)

        download_stream_segment_in_order = Configuration(key='download_stream_segment_in_order', value='True')
        db_session.add(download_stream_segment_in_order)

        default_user_agent = Configuration(key='default_user_agent', value='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0')
        db_session.add(default_user_agent)

        download_from_widevine = Configuration(key='download_from_widevine', value='False')
        db_session.add(download_from_widevine)

        cdm_path = Configuration(key='cdm_path', value='')
        db_session.add(cdm_path)

        downloaded_videos_from_html_files = Configuration(key='downloaded_videos_from_html_files', value='False')
        db_session.add(downloaded_videos_from_html_files)

        auth_threads = Configuration(key='auth_threads', value='1')
        db_session.add(auth_threads)

        # API CONFIGURATION
        allow_remote_api_communication = Configuration(key='allow_remote_api_communication', value='False')
        db_session.add(allow_remote_api_communication)

        unhashed_hwid, hashed_hwid = generate_hwid()
        public_hwid = Configuration(key='public_hwid', value=hashed_hwid)
        db_session.add(public_hwid)
        registration_uuid = Configuration(key='registration_uuid', value=unhashed_hwid)
        db_session.add(registration_uuid)
        public_pgp_key = Configuration(key='public_pgp_key', value='Cadastrar')
        db_session.add(public_pgp_key)
        api_username = Configuration(key='api_username', value='Cadastrar')
        db_session.add(api_username)
        api_password = Configuration(key='api_password', value='Cadastrar')
        db_session.add(api_password)
        api_token = Configuration(key='api_token', value='Cadastrar')
        db_session.add(api_token)
        api_consent = Configuration(key='api_consent', value='False')
        db_session.add(api_consent)
        api_consent_date = Configuration(key='api_consent_date', value='0')
        db_session.add(api_consent_date)

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

    download_conf = Configuration(key='download_path', value=download_path)
    char_conf = Configuration(key='remaining_save_length', value=remaining)

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
    home_conf = Configuration(key='home_address', value=home_address)
    repo_conf = Configuration(key='repository_url', value=repo_url)
    dev_conf = Configuration(key='development_org', value=development_org)

    return home_conf, repo_conf, dev_conf
