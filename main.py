import os
from ControllerClass.ControllerAPI import ControllerAPI
from ControllerClass.ControllerGithub import ControllerGithub
from settings import START_COMMENT, END_COMMENT

if __name__ == "__main__":
    # Pega o usuário das variáveis de ambiente do GitHub Actions
    user = os.getenv("ALURA_USER", "lcrochaDEV")

    # Aqui capturamos as ENVs. Se não existirem, o settings.py já tratou o fallback.
    start_m = os.getenv("START_MARKER", START_COMMENT)
    end_m = os.getenv("END_MARKER", END_COMMENT)
    limit = os.getenv("INPUT_NUMBER_LAST_BADGES", "16")
    
    # 1. Busca os dados e gera o conteúdo formatado
    bot = ControllerAPI(username=user, start_marker=start_m, end_marker=end_m, number_badges=int(limit))
    novo_readme_completo = bot.varrerDadosAlura()

    # 2. Salva no GitHub
    github_bot = ControllerGithub()
    github_bot.atualizar_readme(novo_readme_completo)
    