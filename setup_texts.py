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
                    + colorama.Fore.RED + ' (Este utilitário não instala as ferramentas, apenas verifica a presença delas, e o uso do programa em si deve seguir a jurisdição aplicável no país)' + colorama.Style.RESET_ALL,
        'check_python_version': colorama.Fore.YELLOW + 'Verificando sua versão do Python (versão mínima: 3.12)...' + colorama.Style.RESET_ALL,
        'python_version_not_supported': colorama.Fore.RED + '\tDesculpe, sua versão do Python não é suportada por este aplicativo.\nAtualize-a (este script não interfere com o Python do usuário por risco de quebrar aplicações terceiras).' + colorama.Style.RESET_ALL,
        'python_version_supported': colorama.Fore.GREEN + '\tSua versão do Python é suportada por este aplicativo!' + colorama.Style.RESET_ALL,
        'check_user_os': colorama.Fore.YELLOW + 'Verificando seu sistema operacional...' + colorama.Style.RESET_ALL,
        'unsupported_os': colorama.Fore.RED + '\tDesculpe, seu sistema operacional não é suportado por este aplicativo.\nSaindo.' + colorama.Style.RESET_ALL,
        'supported_os': colorama.Fore.GREEN + '\tSeu sistema operacional é suportado por este aplicativo!' + colorama.Style.RESET_ALL,
        'prompt_master_password': colorama.Fore.YELLOW + 'Digite a senha mestra a ser utilizada para acessar sua instância do Katomart:\n' + colorama.Style.RESET_ALL,
        'cli_tool_introduction': colorama.Fore.YELLOW + 'Agora, vamos verificar se você possui as ferramentas de sistema instaladas e explicar uma por uma.\n' + colorama.Style.RESET_ALL,
        'check_for_cli_tool': '\tVerificando se a ferramenta "{}" está instalada...',
        'cli_tool_not_located': colorama.Fore.RED + '\tA ferramenta "{}" não foi localizada.\n' + colorama.Style.RESET_ALL +
                                colorama.Fore.GREEN + '\t\tDigite "download" para indicar que o programa deverá tentar realizar o download da ferramenta.\n' + colorama.Style.RESET_ALL +
                                colorama.Fore.YELLOW + '\t\tDigite "skip" para ignorar a instalação desta ferramenta.\n' + colorama.Style.RESET_ALL,
        'cli_tool_located': colorama.Fore.GREEN + '\tA ferramenta "{}" foi localizada em seu sistema com sucesso!' + colorama.Style.RESET_ALL,
        'ffmpeg_introduction': colorama.Fore.YELLOW + 'O FFMPEG é uma ferramenta que permite a manipulação de arquivos de áudio e vídeo. '
                                'Ele é necessário para a execução de algumas funcionalidades do Katomart que lidam com a codificação e normalização de vídeos.\n' + colorama.Style.RESET_ALL,
        'ffmpeg_download_instructions': colorama.Fore.MAGENTA + 'Para instalar o FFMPEG, siga as instruções abaixo:\n' + colorama.Style.RESET_ALL +
                                        colorama.Fore.YELLOW + '1. Acesse o site oficial do FFMPEG: https://ffmpeg.org/download.html\n' + colorama.Style.RESET_ALL +
                                        colorama.Fore.YELLOW + '2. Baixe a versão mais recente do FFMPEG para o seu sistema operacional, de um distribuidor oficial (painel localizado à esquerda na página).\n' + colorama.Style.RESET_ALL +
                                        colorama.Fore.YELLOW + '3. Extraia os arquivos e adicione o arquivo /bin/ffmpeg à variável "PATH" de suas Variáveis de Ambiente no seu sistema operacional.\n' + colorama.Style.RESET_ALL,
        'cli_tool_optin_input_error': colorama.Fore.RED + 'Você deve digitar "download" ou "skip" apenas!',
        'geckodriver_introduction': colorama.Fore.YELLOW + 'O Geckodriver é uma ferramenta que permite a automação de navegadores web, e é necessário para alguns downloaders específicos funcionarem. Você também precisa ter o Firefox instalado.\n' + colorama.Style.RESET_ALL
                                    + colorama.Fore.MAGENTA + '\t#Boycott Manifest V3 (chromium)' + colorama.Style.RESET_ALL,
        'geckodriver_download_instructions': colorama.Fore.MAGENTA + 'Para instalar o Geckodriver, siga as instruções abaixo:\n' + colorama.Style.RESET_ALL +
                                            colorama.Fore.YELLOW + '1. Instale o Mozilla Firefox (caso não tenha instalado): https://www.mozilla.org/pt-BR/firefox/new/\n' + colorama.Style.RESET_ALL +
                                            colorama.Fore.YELLOW + '2. Acesse a aba de releases do Github do Geckodriver e baixe a versão correspondente ao seu sistema: https://github.com/mozilla/geckodriver/releases' + colorama.Style.RESET_ALL +
                                            colorama.Fore.YELLOW + '3. Extraia os arquivos e adicione o arquivo "geckodriver" à variável "PATH" de suas Variáveis de Ambiente no seu sistema operacional.\n' + colorama.Style.RESET_ALL,
        'bento4_introduction': colorama.Fore.YELLOW + 'O MP4Decrypt é uma ferramenta que faz parte do Bento4 que permite a descriptografia de arquivos de vídeo no formato MP4.\n' + colorama.Style.RESET_ALL +
                                   colorama.Fore.MAGENTA + 'Ela é necessária apenas para baixar vídeos do Widevine, e para fazer esse processo você precisa de uma CDM válida de um ANDROID extraída pelo Frida.\n' +
                                   'Caso você não saiba o que é isso, pule a instalação desta ferramenta, pois isto não será ensinado aqui, e você pode sempre baixar mais tarde.\n' + colorama.Style.RESET_ALL,
        'bento4_download_instructions': colorama.Fore.MAGENTA + 'Para instalar o MP4Decrypt, você precisa baixar o pacote do Bento4, para isto, siga as instruções abaixo:\n' + colorama.Style.RESET_ALL +
                                             colorama.Fore.YELLOW + '1. Acesse o site oficial do Bento4: https://www.bento4.com/downloads/\n' + colorama.Style.RESET_ALL +
                                             colorama.Fore.YELLOW + '2. Baixe a versão mais recente do Bento4 para o seu sistema operacional.\n' + colorama.Style.RESET_ALL +
                                             colorama.Fore.YELLOW + '3. Extraia os arquivos e adicione o arquivo /bin/mp4decrypt à variável "PATH" de suas Variáveis de Ambiente no seu sistema operacional.\n' + colorama.Style.RESET_ALL,
        'start_string': 'Iniciando o Katomart...',
        'batch_name': 'executar_katomart',
        'setup_complete': colorama.Fore.GREEN + 'Configuração concluída com sucesso! O Katomart está pronto para ser executado.\n '
                                                'Para iniciar o Katomart, execute o arquivo "{}.{}" que foi criado nesta pasta. Bons downloads :)' + colorama.Style.RESET_ALL
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
                    + colorama.Fore.RED + ' (This script does not install the tools, only checks for their presence, and the use of the software itself should follow the applicable jurisdiction in the country)' + colorama.Style.RESET_ALL,
        'check_python_version': colorama.Fore.YELLOW + 'Checking your Python version (minimum version: 3.12),,,' + colorama.Style.RESET_ALL,
        'python_version_not_supported': colorama.Fore.RED + '\tSorry, your Python version is not supported by this software.\nPlease update it (this script does not interfere with the user\'s Python to avoid breaking third party applications).' + colorama.Style.RESET_ALL,
        'python_version_supported': colorama.Fore.GREEN + '\tYour Python version is supported by this software!' + colorama.Style.RESET_ALL,
        'check_user_os': colorama.Fore.YELLOW + 'Checking your operating system...' + colorama.Style.RESET_ALL,
        'unsupported_os': colorama.Fore.RED + '\tSorry, your operating system is not supported by this software.\nExiting.' + colorama.Style.RESET_ALL,
        'supported_os': colorama.Fore.GREEN + '\tYour operating system is supported by this software!' + colorama.Style.RESET_ALL,
        'prompt_master_password': colorama.Fore.YELLOW + 'Type the master password to be used to access your Katomart instance:\n' + colorama.Style.RESET_ALL,
        'cli_tool_introduction': colorama.Fore.YELLOW + 'Now, we will be checking if you\'ve got the necessary third party system tools, as well as explain the need for each\n' + colorama.Style.RESET_ALL,
        'check_for_cli_tool': '\tchecking if the tool "{}" is installed...',
        'cli_tool_not_located': colorama.Fore.RED + '\tThe tool "{}" was not found on your system.\n' + colorama.Style.RESET_ALL +
                        colorama.Fore.GREEN + '\t\tType "download" to flag this tool as desirable and for the software to attempt installing it in your system.\n' + colorama.Style.RESET_ALL +
                        colorama.Fore.YELLOW + '\t\tType "skip" to ignore this tool completely.\n' + colorama.Style.RESET_ALL,
        'cli_tool_located': colorama.Fore.GREEN + '\tThe tool "{}" was successfully located in your system!' + colorama.Style.RESET_ALL,
        'ffmpeg_introduction': colorama.Fore.YELLOW + 'FFMPEG is a tool that allows for the manipulation of audio and video files. '
                                'It is required for some of Katomart\'s functionalities that deal with video encoding and normalization.\n' + colorama.Style.RESET_ALL,
        'ffmpeg_download_instructions': colorama.Fore.MAGENTA + 'To install FFMPEG, follow the instructions below:\n' + colorama.Style.RESET_ALL +
                                        colorama.Fore.YELLOW + '1. Access the official FFMPEG website: https://ffmpeg.org/download.html\n' + colorama.Style.RESET_ALL +
                                        colorama.Fore.YELLOW + '2. Download the latest version of FFMPEG for your operating system, from an official distributor (located on the left panel of the page).\n' + colorama.Style.RESET_ALL +
                                        colorama.Fore.YELLOW + '3. Extract the files and add /bin/ffmpeg file to your system\'s "PATH" variable in your Environment Variables.\n' + colorama.Style.RESET_ALL,
        'cli_tool_optin_input_error': colorama.Fore.RED + 'You must type only "download", or "skip"!',
        'geckodriver_introduction': colorama.Fore.YELLOW + 'Geckodriver is a tool that allows for web browser automation, and is required for some specific downloaders to work. You also need to have Firefox installed.\n' + colorama.Style.RESET_ALL
                                    + colorama.Fore.MAGENTA + '\t#Boycott Manifest V3 (chromium)' + colorama.Style.RESET_ALL,
        'geckodriver_download_instructions': colorama.Fore.MAGENTA + 'To install Geckodriver, follow the instructions below:\n' + colorama.Style.RESET_ALL +
                                            colorama.Fore.YELLOW + '1. Install Mozilla Firefox (if you haven\'t already): https://www.mozilla.org/en-US/firefox/new/\n' + colorama.Style.RESET_ALL +
                                            colorama.Fore.YELLOW + '2. Access the releases tab on the Geckodriver Github page and download the version corresponding to your system: https://github.com/mozilla/geckodriver/releases' + colorama.Style.RESET_ALL +
                                            colorama.Fore.YELLOW + '3. Extract the files and add the "geckodriver" file to your system\'s "PATH" variable in your Environment Variables.\n' + colorama.Style.RESET_ALL,
        'bento4_introduction': colorama.Fore.YELLOW + 'MP4Decrypt is a tool that is part of Bento4 that allows for the decryption of MP4 video files.\n' + colorama.Style.RESET_ALL +
                                   colorama.Fore.MAGENTA + 'It is only required for downloading Widevine videos, and to do so you need a valid ANDROID CDM extracted through Frida.\n' +
                                   'If you don\'t know what this is, you SHOULD skip this, as it won\'t be taught here, and you can always download it later.\n' + colorama.Style.RESET_ALL,
        'bento4_download_instructions': colorama.Fore.MAGENTA + 'To install MP4Decrypt, you need to download the Bento4 package, follow the instructions below:\n' + colorama.Style.RESET_ALL +
                                             colorama.Fore.YELLOW + '1. Access the official Bento4 website: https://www.bento4.com/downloads/\n' + colorama.Style.RESET_ALL +
                                             colorama.Fore.YELLOW + '2. Download the latest version of Bento4 for your operating system.\n' + colorama.Style.RESET_ALL +
                                             colorama.Fore.YELLOW + '3. Extract the files and add /bin/mp4decrypt file to your system\'s "PATH" variable in your Environment Variables.\n' + colorama.Style.RESET_ALL,
        'start_string': 'Initializing Katomart...',
        'batch_name': 'run_katomart',
        'setup_complete': colorama.Fore.GREEN + 'Setup completed successfully! Katomart is ready to be run.\n '
                                                'To start Katomart, run the "{}.{}" file that was created in this folder. Happy downloading :)' + colorama.Style.RESET_ALL
    }
}