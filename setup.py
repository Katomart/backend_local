import setup_utils
from setup_texts import SETUP_TEXTS

USER_LANGUAGE = None
USER_OS = None

HAS_FFMPEG = None
INSTALL_FFMPEG = None

HAS_MP4DECRYPT = None
INSTALL_MP4DECRYPT = None

SUPPORTED_PYTHON_VERSION = (3, 12)
SUPPORTED_OS = ('win32', 'linux', 'darwin')

for language in SETUP_TEXTS:
    print(SETUP_TEXTS[language]['which_language'])
USER_LANGUAGE = input()

if USER_LANGUAGE not in setup_utils.SUPPORTED_LANGUAGES.values():
    print('Unsupported language. Defaulting to English.')
    USER_LANGUAGE = 'en'

print(SETUP_TEXTS[USER_LANGUAGE]['welcome'])

print(SETUP_TEXTS[USER_LANGUAGE]['check_python_version'])
if not setup_utils.check_python_support(*SUPPORTED_PYTHON_VERSION):
    raise Exception(SETUP_TEXTS[USER_LANGUAGE]['python_version_not_supported'])
print(SETUP_TEXTS[USER_LANGUAGE]['python_version_supported'])

print(SETUP_TEXTS[USER_LANGUAGE]['check_user_os'])
if setup_utils.get_operating_system() not in SUPPORTED_OS:
    raise Exception(SETUP_TEXTS[USER_LANGUAGE]['unsupported_os'])
print(SETUP_TEXTS[USER_LANGUAGE]['supported_os'])

# CLI TOOLS
print(SETUP_TEXTS[USER_LANGUAGE]['cli_tool_introduction'])

# FFMPEG
print(SETUP_TEXTS[USER_LANGUAGE]['ffmpeg_introduction'])
print(SETUP_TEXTS[USER_LANGUAGE]['check_for_cli_tool'].format('ffmpeg'))
HAS_FFMPEG = setup_utils.check_for_cli_tool('ffmpeg')
if not HAS_FFMPEG:
    print(SETUP_TEXTS[USER_LANGUAGE]['cli_tool_not_located'].format('ffmpeg'))
else:
    print(SETUP_TEXTS[USER_LANGUAGE]['cli_tool_located'].format('ffmpeg'))
    INSTALL_FFMPEG = False
while True:
    try:
        HAS_FFMPEG, INSTALL_FFMPEG = setup_utils.get_user_third_party_optin(tool_name='ffmpeg')
        break
    except ValueError:
        print(SETUP_TEXTS[USER_LANGUAGE]['cli_tool_optin_input_error'])
        continue
if HAS_FFMPEG and not INSTALL_FFMPEG:
    print(SETUP_TEXTS[USER_LANGUAGE]['ffmpeg_download_instructions'])

# MP4DECRYPT
print(SETUP_TEXTS[USER_LANGUAGE]['mp4decrypt_introduction'])
print(SETUP_TEXTS[USER_LANGUAGE]['check_for_cli_tool'].format('mp4decrypt'))
HAS_MP4DECRYPT = setup_utils.check_for_cli_tool('mp4decrypt')
if not HAS_MP4DECRYPT:
    print(SETUP_TEXTS[USER_LANGUAGE]['cli_tool_not_located'].format('mp4decrypt'))
else:
    print(SETUP_TEXTS[USER_LANGUAGE]['cli_tool_located'].format('mp4decrypt'))
    INSTALL_MP4DECRYPT = False
while True:
    try:
        HAS_MP4DECRYPT, INSTALL_MP4DECRYPT = setup_utils.get_user_third_party_optin(tool_name='mp4decrypt')
        break
    except ValueError:
        print(SETUP_TEXTS[USER_LANGUAGE]['cli_tool_optin_input_error'])
        continue
if HAS_MP4DECRYPT and not INSTALL_MP4DECRYPT:
    print(SETUP_TEXTS[USER_LANGUAGE]['mp4decrypt_download_instructions'])
