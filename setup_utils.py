import shutil

def check_for_cli_tool(tool_name: str=''):
    """Check if a CLI tool is installed"""
    return shutil.which(tool_name) is not None
