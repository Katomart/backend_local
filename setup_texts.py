import colorama


colorama.init(autoreset=True)

SETUP_TEXTS = {
    'pt': {
        'unsupported_os': colorama.Fore.RED + 'Desculpe, seu sistema operacional não é suportado por este aplicativo.\nSaindo.' + colorama.Style.RESET_ALL,
        'which_language': colorama.Fore.YELLOW + '[pt] Digite o idioma que deseja utilizar (para continuar em português, digite: pt):' + colorama.Style.RESET_ALL,
        'welcome': colorama.Fore.CYAN + 'Boas vindas ao utilitário de instalação do Katomart!\n\n' + colorama.Style.RESET_ALL
                    + 'Este utilitário irá verificar se você possui as ferramentas de sistema necessárias para '
                    'executar o Katomart\n\t' + colorama.Fore.YELLOW + 'Caso você não possua alguma das ferramentas, '
                    'o utilitário irá te explicar sua necessidade e te perguntar se você deseja tentar uma instalacao '
                    'automática, ou, te guiar em como instalar cada uma manualmente.\n\n'
                    + colorama.Style.RESET_ALL + 'Nem todas as ferramentas são necessárias, mas, melhoram a experiência!'
    },
    'en': {
        'unsupported_os': colorama.Fore.RED + 'Sorry, your operating system is not supported by this software.\nExiting.' + colorama.Style.RESET_ALL,
        'which_language': colorama.Fore.YELLOW + '[en] Type in the language you want to use (to continue in english, type: en):' + colorama.Style.RESET_ALL,
        'welcome': colorama.Fore.CYAN + "Welcome to Katomart's setup script!\n\n" + colorama.Style.RESET_ALL
                    + "This tool will make sure that you've got all the needed third party tools installed in your "
                    "system to run this Software\n\t" + colorama.Fore.YELLOW + 'If you are missing some, you will receive '
                    'an explanation as to why it is needed and will be given the option to attempt an auto-installation, or '
                    'be guided on how to download it yourself.\n\n'
                    + colorama.Style.RESET_ALL + 'Not all tools are required to run this software, but they are highly recommended!'

    }
}