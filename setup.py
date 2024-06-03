import colorama


colorama.init(autoreset=True)

print(colorama.Fore.CYAN + 'Boas vindas ao utilitário de instalação do Katomart!\n\n' + colorama.Style.RESET_ALL
      + 'Este utilitário irá verificar se você possui as ferramentas de sistema necessárias para '
      'executar o Katomart\n\t' + colorama.Fore.YELLOW + 'Caso você não possua alguma das ferramentas, '
      'o utilitário irá te explicar sua necessidade e perguntar se você deseja instalar a ferramenta.\n\n'
      + colorama.Style.RESET_ALL + 'Nem todas as ferramentas são necessárias, mas, melhoram a experiência!')

