import os
import shutil
import subprocess
import sys


SUPPORTED_LANGUAGES = {
    'portugues': 'pt',
    'english': 'en'
}

def clear_screen(user_os: str='win32') -> None:
    """Clear the screen
    Params:
        tool_name (str): The name of the tool
    """
    if user_os == 'win32':
        os.system('cls')
    elif user_os in ('linux', 'darwin'):
        os.system('clear')

def check_python_support(major: int=3, minor: int=12) -> bool:
    """Check if the Python version is supported
    Params:
        major (int): The major version of Python
        minor (int): The minor version of Python
    """
    return sys.version_info.major == major and sys.version_info.minor >= minor

def check_for_cli_tool(tool_name: str=''):
    """Check if a CLI tool is installed
    Params:
        tool_name (str): The name of the tool
    """
    return shutil.which(tool_name) is not None

def get_operating_system() -> str:
    """Get the operating system name
    Returns:
        str: The operating system name
    """
    operating_system = sys.platform
    return operating_system if operating_system in ['linux', 'win32', 'darwin'] else 'unsupported'

def get_user_third_party_optin(tool_name: str='') -> tuple[bool, bool]:
    """Get the user's choice for installing a third party tool
    Params:
        tool_name (str): The name of the tool
    Returns:
        bool: Whether the user wants to install the tool
        bool: Whether the user wants to download the tool
    """
    user_input = input()
    if user_input.lower() == 'download':
        return True, True
    elif user_input.lower() == 'man':
        return True, False
    elif user_input.lower() == 'skip':
        return False, False
    else:
        raise ValueError

def create_venv(venv_path: str='.') -> None:
    """Create a virtual environment in the specified path."""
    subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)
