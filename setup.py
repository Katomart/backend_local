import setup_utils
from setup_texts import SETUP_TEXTS

USER_LANGUAGE = None
USER_OS = None
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