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
                    + colorama.Style.RESET_ALL + 'Nem todas as ferramentas são necessárias, mas, melhoram a experiência!',
        'check_python_version': colorama.Fore.YELLOW + 'Verificando sua versão do Python (versão mínima: 3.12)...' + colorama.Style.RESET_ALL,
        'python_version_not_supported': colorama.Fore.RED + '\tDesculpe, sua versão do Python não é suportada por este aplicativo.\nAtualize-a (este script não interfere com o Python do usuário por risco de quebrar aplicações terceiras).' + colorama.Style.RESET_ALL,
        'python_version_supported': colorama.Fore.GREEN + '\tSua versão do Python é suportada por este aplicativo!' + colorama.Style.RESET_ALL,
        'check_user_os': colorama.Fore.YELLOW + 'Verificando seu sistema operacional...' + colorama.Style.RESET_ALL,
        'unsupported_os': colorama.Fore.RED + '\tDesculpe, seu sistema operacional não é suportado por este aplicativo.\nSaindo.' + colorama.Style.RESET_ALL,
        'supported_os': colorama.Fore.GREEN + '\tSeu sistema operacional é suportado por este aplicativo!' + colorama.Style.RESET_ALL,
        'cli_tool_introduction': colorama.Fore.YELLOW + 'Agora, vamos verificar se você possui as ferramentas de sistema instaladas e explicar uma por uma.\n' + colorama.Style.RESET_ALL,
        'check_for_cli_tool': '\tVerificando se a ferramenta "{}" está instalada...',
        'cli_tool_not_located': colorama.Fore.RED + '\tA ferramenta "{}" não foi localizada.\n' + colorama.Style.RESET_ALL +
                                colorama.Fore.GREEN + '\t\tDigite "download" para indicar que o programa deverá tentar realizar o download da ferramenta.\n' + colorama.Style.RESET_ALL +
                                colorama.Fore.MAGENTA + '\t\tDigite "man" para ler as instruções de download manual da ferramenta\n' + colorama.Style.RESET_ALL +
                                colorama.Fore.YELLOW + '\t\tDigite "skip" para ignorar a instalação desta ferramenta.\n' + colorama.Style.RESET_ALL,
        'cli_tool_located': colorama.Fore.GREEN + '\tA ferramenta "{}" foi localizada em seu sistema com sucesso!' + colorama.Style.RESET_ALL,
        'ffmpeg_introduction': colorama.Fore.YELLOW + 'O FFMPEG é uma ferramenta que permite a manipulação de arquivos de áudio e vídeo. '
                                'Ele é necessário para a execução de algumas funcionalidades do Katomart que lidam com a codificação e normalização de vídeos.\n' + colorama.Style.RESET_ALL,
    },
    'en': {
        'unsupported_os': colorama.Fore.RED + 'Sorry, your operating system is not supported by this software.\nExiting.' + colorama.Style.RESET_ALL,
        'which_language': colorama.Fore.YELLOW + '[en] Type in the language you want to use (to continue in english, type: en):' + colorama.Style.RESET_ALL,
        'welcome': colorama.Fore.CYAN + "Welcome to Katomart's setup script!\n\n" + colorama.Style.RESET_ALL
                    + "This tool will make sure that you've got all the needed third party tools installed in your "
                    "system to run this Software\n\t" + colorama.Fore.YELLOW + 'If you are missing some, you will receive '
                    'an explanation as to why it is needed and will be given the option to attempt an auto-installation, or '
                    'be guided on how to download it yourself.\n\n'
                    + colorama.Style.RESET_ALL + 'Not all tools are required to run this software, but they are highly recommended!',
        'check_python_version': colorama.Fore.YELLOW + 'Checking your Python version (minimum version: 3.12),,,' + colorama.Style.RESET_ALL,
        'python_version_not_supported': colorama.Fore.RED + '\tSorry, your Python version is not supported by this software.\nPlease update it (this script does not interfere with the user\'s Python to avoid breaking third party applications).' + colorama.Style.RESET_ALL,
        'python_version_supported': colorama.Fore.GREEN + '\tYour Python version is supported by this software!' + colorama.Style.RESET_ALL,
        'check_user_os': colorama.Fore.YELLOW + 'Checking your operating system...' + colorama.Style.RESET_ALL,
        'unsupported_os': colorama.Fore.RED + '\tSorry, your operating system is not supported by this software.\nExiting.' + colorama.Style.RESET_ALL,
        'supported_os': colorama.Fore.GREEN + '\tYour operating system is supported by this software!' + colorama.Style.RESET_ALL,
        'cli_tool_introduction': colorama.Fore.YELLOW + 'Now, we will be checking if you\'ve got the necessary third party system tools, as well as explain the need for each\n' + colorama.Style.RESET_ALL,
        'check_for_cli_tool': '\tchecking if the tool "{}" is installed...',
        'cli_tool_not_located': colorama.Fore.RED + '\tThe tool "{}" was not found on your system.\n' + colorama.Style.RESET_ALL +
                        colorama.Fore.GREEN + '\t\tType "download" to flag this tool as desirable and for the software to attempt installing it in your system.\n' + colorama.Style.RESET_ALL +
                        colorama.Fore.MAGENTA + '\t\tType "man" to read how to manually download and install this tool.\n' + colorama.Style.RESET_ALL +
                        colorama.Fore.YELLOW + '\t\tType "skip" to ignore this tool completely.\n' + colorama.Style.RESET_ALL,
        'cli_tool_located': colorama.Fore.GREEN + '\tThe tool "{}" was successfully located in your system!' + colorama.Style.RESET_ALL,
        'ffmpeg_introduction': colorama.Fore.YELLOW + 'FFMPEG is a tool that allows for the manipulation of audio and video files. '
                                'It is required for some of Katomart\'s functionalities that deal with video encoding and normalization.\n' + colorama.Style.RESET_ALL,
    }
}