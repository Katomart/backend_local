import shutil
import sys

def check_for_cli_tool(tool_name: str=''):
    """Check if a CLI tool is installed"""
    return shutil.which(tool_name) is not None

def get_operating_system() -> str:
    """Get the operating system name"""
    operating_system = sys.platform
    return operating_system if operating_system in ['linux', 'win32', 'darwin'] else 'unsupported'
