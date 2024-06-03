import pathlib

from setup_utils import get_execution_path, get_operating_system, remaining_path_length

from servidor import db_session

from models.configs import Configuration


SERVER_PATH = get_execution_path()
OPERATING_SYSTEM = get_operating_system()

def set_default_config() -> None:
    """Set the default application configuration
    """
    # Path Stuff
    download_conf, char_conf = set_download_path()
    db_session.add(download_conf)
    db_session.add(char_conf)

    # Home Stuff
    home_conf, repo_conf = set_home_address()
    db_session.add(home_conf)
    db_session.add(repo_conf)

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
                      repo_url: str='https://github.com/katomaro/katomart') -> tuple[Configuration, Configuration]:
    """Set the home address for the application
    Params:
        home_address (str): The adress to which the application should phone to
        repo_url (str): The URL of the repository
    Returns:
        tuple[Configuration, Configuration]: The home address and the repository URL
    """
    home_conf = Configuration(key='home_address', value=home_address)
    repo_conf = Configuration(key='repository_url', value=repo_url)
    return home_conf, repo_conf
