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
    DATABASE_URL = 'sqlite:///dev.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
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

    for key, value in setup_config.items():
        config = Configuration(key=key, value= 'True' if value == 1 else 'False' if value == 0 else value)
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
        default_config_set = Configuration(key='default_config_set', value='True' if has_set_config else 'False')
        db_session.add(default_config_set)

        # Path Stuff
        download_conf, char_conf = set_download_path()
        db_session.add(download_conf)
        db_session.add(char_conf)

        user_local_consent = Configuration(key='setup_user_local_consent', value='False', value_type='bool', hidden=True)
        db_session.add(user_local_consent)

        user_local_consent_date = Configuration(key='setup_user_local_consent_date', value='0', value_type='int', hidden=True)
        db_session.add(user_local_consent_date)

        last_execution = Configuration(key='info_last_execution', value='0', value_type='int', hidden=True)
        db_session.add(last_execution)

        use_original_media_name = Configuration(key='dl_use_original_media_name', value='False', value_type='bool', hidden=False)
        db_session.add(use_original_media_name)

        avoid_path_name_explosion_by_rooting = Configuration(key='dl_avoid_path_name_explosion_by_rooting', value='True', value_type='bool', hidden=False)
        db_session.add(avoid_path_name_explosion_by_rooting)

        avoid_path_name_shortening = Configuration(key='dl_avoid_path_name_shortening', value='False', value_type='bool', hidden=False)
        db_session.add(avoid_path_name_shortening)

        aggressive_path_name_shortening = Configuration(key='dl_aggressive_path_name_shortening', value='False', value_type='bool', hidden=False)
        db_session.add(aggressive_path_name_shortening)

        max_path_name_length = Configuration(key='dl_max_path_name_length', value='45', value_type='int', hidden=False)
        db_session.add(max_path_name_length)

        on_path_explode_fail_all = Configuration(key='dl_on_path_explode_fail_all', value='False', value_type='bool', hidden=False)
        db_session.add(on_path_explode_fail_all)

        on_path_explode_cut_course_name = Configuration(key='dl_on_path_explode_cut_course_name', value='False', value_type='bool', hidden=False)
        db_session.add(on_path_explode_cut_course_name)

        on_path_explode_cut_module_name = Configuration(key='dl_on_path_explode_cut_module_name', value='True', value_type='bool', hidden=False)
        db_session.add(on_path_explode_cut_module_name)

        on_path_explode_cut_lesson_name = Configuration(key='dl_on_path_explode_cut_lesson_name', value='True', value_type='bool', hidden=False)
        db_session.add(on_path_explode_cut_lesson_name)

        on_path_explode_cut_file_name = Configuration(key='dl_on_path_explode_cut_file_name', value='True', value_type='bool', hidden=False)
        db_session.add(on_path_explode_cut_file_name)

        on_path_explode_use_name_fallback = Configuration(key='dl_on_path_explode_use_name_fallback', value='True', value_type='bool', hidden=False)
        db_session.add(on_path_explode_use_name_fallback)

        enumerate_files = Configuration(key='dl_enumerate_files', value='True', value_type='bool', hidden=False)
        db_session.add(enumerate_files)

        media_name_fallback = Configuration(key='dl_media_name_fallback', value='{file_type}', value_type='str', hidden=True)
        db_session.add(media_name_fallback)

        use_custom_ffmpeg_arguments = Configuration(key='dl_use_custom_ffmpeg_arguments', value='False', value_type='bool', hidden=False)
        db_session.add(use_custom_ffmpeg_arguments)

        custom_ffmpeg_arguments = Configuration(key='dl_custom_ffmpeg_arguments', value='-i,"{input_file}",-c:v,libx264,-crf,23,-c:a,aac,-b:a,192k,"{output_file}"', value_type='str', hidden=False)
        db_session.add(custom_ffmpeg_arguments)

        use_fast_ffmpeg_hls_conversion = Configuration(key='dl_fast_ffmpeg_hls_conversion', value='False', value_type='bool', hidden=False)
        db_session.add(use_fast_ffmpeg_hls_conversion)

        fast_ffmpeg_hls_conversion_arguments = Configuration(key='dl_fast_ffmpeg_hls_conversion_arguments', value='-i,"{input_file}",-c,copy,"{output_file}"', value_type='str', hidden=False)
        db_session.add(fast_ffmpeg_hls_conversion_arguments)

        download_subtitles = Configuration(key='dl_download_subtitles', value='False', value_type='bool', hidden=False)
        db_session.add(download_subtitles)

        subtitle_language = Configuration(key='dl_subtitle_language', value='pt', value_type='select', hidden=False)
        db_session.add(subtitle_language)

        download_quality = Configuration(key='dl_video_quality', value='1080p', value_type='select', hidden=False)
        db_session.add(download_quality)

        download_quality_fallback = Configuration(key='dl_video_quality_fallback', value='best', value_type='select', hidden=False)
        db_session.add(download_quality_fallback)

        video_download_format = Configuration(key='dl_video_format', value='mp4', value_type='select', hidden=False)
        db_session.add(video_download_format)

        download_threads = Configuration(key='dl_threads', value='1', value_type='int', hidden=True)
        db_session.add(download_threads)

        stream_download_threads = Configuration(key='dl_stream_threads', value='5', value_type='int', hidden=False)
        db_session.add(stream_download_threads)

        stream_prefer_ytdlp = Configuration(key='dl_stream_prefer_ytdlp', value='True', value_type='bool', hidden=False)
        db_session.add(stream_prefer_ytdlp)

        download_maximum_retries_per_file = Configuration(key='dl_max_retries_per_file', value='5', value_type='int', hidden=False)
        db_session.add(download_maximum_retries_per_file)

        download_await_time = Configuration(key='dl_await_time', value='5', value_type='int', hidden=False)
        db_session.add(download_await_time)

        download_await_on_fail = Configuration(key='dl_await_on_fail', value='5', value_type='int', hidden=False)
        db_session.add(download_await_on_fail)

        reauth_on_fail = Configuration(key='dl_reauth_on_fail', value='False', value_type='bool', hidden=False)
        db_session.add(reauth_on_fail)

        reauth_fail_threshold = Configuration(key='dl_reauth_fail_threshold', value='3', value_type='int', hidden=False)
        db_session.add(reauth_fail_threshold)

        reauth_await_time = Configuration(key='dl_reauth_await_time', value='180', value_type='int', hidden=False)
        db_session.add(reauth_await_time)

        reauth_maximum_retries = Configuration(key='dl_reauth_maximum_retries', value='2', value_type='int', hidden=False)
        db_session.add(reauth_maximum_retries)

        download_stream_segment_in_order = Configuration(key='dl_stream_segment_in_order', value='True', value_type='bool', hidden=False)
        db_session.add(download_stream_segment_in_order)

        default_user_agent = Configuration(key='setup_default_user_agent', value='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0', value_type='str', hidden=False)
        db_session.add(default_user_agent)

        download_from_widevine = Configuration(key='setup_download_from_widevine', value='False', value_type='bool', hidden=False)
        db_session.add(download_from_widevine)

        cdm_path = Configuration(key='setup_cdm_path', value='', value_type='str', hidden=False)
        db_session.add(cdm_path)

        downloaded_videos_from_html_files = Configuration(key='dl_videos_from_text_files', value='False', value_type='bool', hidden=False)
        db_session.add(downloaded_videos_from_html_files)

        # API CONFIGURATION
        allow_remote_api_communication = Configuration(key='remote_allow_home_api_communication', value='False', value_type='bool', hidden=False)
        db_session.add(allow_remote_api_communication)

        unhashed_hwid, hashed_hwid = generate_hwid()
        public_hwid = Configuration(key='remote_public_hwid', value=hashed_hwid, value_type='str', hidden=False)
        db_session.add(public_hwid)
        registration_uuid = Configuration(key='remote_registration_uuid', value=unhashed_hwid, value_type='str', hidden=True)
        db_session.add(registration_uuid)
        public_pgp_key = Configuration(key='remote_public_pgp_key', value='Cadastrar', value_type='str', hidden=False)
        db_session.add(public_pgp_key)
        api_username = Configuration(key='remote_api_username', value='Cadastrar', value_type='str', hidden=False)
        db_session.add(api_username)
        api_password = Configuration(key='remote_api_password', value='Cadastrar', value_type='str', hidden=False)
        db_session.add(api_password)
        api_token = Configuration(key='remote_api_token', value='Cadastrar', value_type='str', hidden=False)
        db_session.add(api_token)
        api_consent = Configuration(key='remote_api_consent', value='False', value_type='bool', hidden=True)
        db_session.add(api_consent)
        api_consent_date = Configuration(key='remote_api_consent_date', value='0', value_type='int', hidden=True)
        db_session.add(api_consent_date)

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

    download_conf = Configuration(key='dl_storage_path', value=download_path, value_type='str', hidden=False, editable=True)
    char_conf = Configuration(key='dl_remaining_save_length', value=remaining, value_type='int', hidden=False, editable=False)

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
    home_conf = Configuration(key='remote_home_address', value=home_address, value_type='str', hidden=False, editable=False)
    repo_conf = Configuration(key='remote_repository_url', value=repo_url, value_type='str', hidden=False, editable=False)
    dev_conf = Configuration(key='remote_development_org', value=development_org, value_type='str', hidden=False, editable=False)

    return home_conf, repo_conf, dev_conf
