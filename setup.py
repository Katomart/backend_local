import setup_utils
from setup_texts import SETUP_TEXTS

USER_LANGUAGE = None

for language in SETUP_TEXTS:
    print(SETUP_TEXTS[language]['which_language'])
    USER_LANGUAGE = input()
    if USER_LANGUAGE not in setup_utils.SUPPORTED_LANGUAGES.values():
        print('Unsupported language. Defaulting to English.')
        USER_LANGUAGE = 'en'
