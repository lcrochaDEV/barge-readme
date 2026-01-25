import os
import sys
import re
from ControllerClass.ControllerAPI import ControllerAPI
from ControllerClass.ControllerGithub import ControllerGithub
from settings import START_SECTION, END_SECTION, LIST_REGEX

if __name__ == "__main__":
    # Pega o usuário das variáveis de ambiente do GitHub Actions
    user = os.getenv("ALURA_USER", "lcrochaDEV")

    # Aqui capturamos as ENVs. Se não existirem, o settings.py já tratou o fallback.
    start_m = os.getenv("START_SECTION") or START_SECTION
    end_m = os.getenv("END_SECTION") or END_SECTION
    limit = os.getenv("INPUT_NUMBER_LAST_BADGES", "16")
    
    # 1. Busca os dados e gera o conteúdo formatado
    bot = ControllerAPI(username=user, start_marker=start_m, end_marker=end_m, number_badges=int(limit))
    github_bot = ControllerGithub()

    try:
        readme_obj = github_bot.repo.get_contents("README.md")
        readme_atual = readme_obj.decoded_content.decode("utf-8")
    except Exception as e:
        print(f"❌ Erro ao acessar o README.md: {e}")
        sys.exit(1)

    novo_readme_completo = bot.varrerDadosAlura()

    if novo_readme_completo:
        bloco_final = f"{START_SECTION}\n{novo_readme_completo}\n{END_SECTION}"

        if re.search(LIST_REGEX, readme_atual):
            print(novo_readme_completo)
            # Substitui apenas o que está entre as tags no readme_atual
            novo_readme_completo = re.sub(LIST_REGEX, lambda _: novo_readme_completo, readme_atual)
            print("✅ Badges injetadas com sucesso entre os marcadores!")
        else:
            print(f"⚠️ Erro: Marcadores não encontrados no README do usuário.")
            print(f"Procurei por:\n{start_m}\n{end_m}")
            sys.exit(1)

    # Salva no GitHub
    github_bot.atualizar_readme(novo_readme_completo)
    