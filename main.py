import os
import sys
import re
from ControllerClass.ControllerAPI import ControllerAPI
from ControllerClass.ControllerGithub import ControllerGithub
from settings import USER, START_SECTION, END_SECTION, LIST_REGEX, LIMITE

if __name__ == "__main__":
   
    # 1. Busca os dados e gera o conteúdo formatado
    bot = ControllerAPI(username=USER, start_section=START_SECTION, end_section=END_SECTION, number_badges=int(LIMITE))
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
            # Substitui apenas o que está entre as tags no readme_atual
            novo_readme_completo = re.sub(LIST_REGEX, lambda _: bloco_final, readme_atual)
            print(novo_readme_completo)
            print("✅ Badges injetadas com sucesso entre os marcadores!")
        else:
            print(f"⚠️ Erro: Marcadores não encontrados no README do usuário.")
            print(f"Procurei por:\n{START_SECTION}\n{END_SECTION}")
            sys.exit(1)

    # Salva no GitHub
    #github_bot.atualizar_readme(novo_readme_completo)
