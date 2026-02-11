import sys
import re
from ControllerClass.ControllerAPI import ControllerAPI
from ControllerClass.ControllerGithub import ControllerGithub
import settings

if __name__ == "__main__":
   
    # 1. Busca os dados e gera o conteúdo formatado
    bot = ControllerAPI(username=settings.USER, number_badges=int(settings.LIMITE))
    github_bot = ControllerGithub()

    try:
        readme_obj = github_bot.repo.get_contents("README.md")
        readme_atual = readme_obj.decoded_content.decode("utf-8")
    except Exception as e:
        print(f"❌ Erro ao acessar o README.md: {e}")
        sys.exit(1)

    html_alura = bot.varrerDadosAlura()
    html_credly = bot.varrerDadosCredly()
    bot.finalizar() # Agora sim fechamos o navegador

    readme_modificado = readme_atual
    houve_alteracao = False

    if html_alura and re.search(settings.LIST_REGEX_ALURA, readme_modificado):
        # Substitui apenas o que está entre as tags no readme_modificado
        bloco_alura = f"{settings.START_ALURA}\n{html_alura}\n{settings.END_ALURA}"
        readme_modificado = re.sub(settings.LIST_REGEX_ALURA, lambda _: bloco_alura, readme_modificado)
        houve_alteracao = True
        # Salva no GitHub
        #github_bot.atualizar_readme(html_alura)
        print("✅ Badges injetadas com sucesso entre os marcadores!")
    else:
        print(f"⚠️ Erro: Marcadores não encontrados no README do usuário.")
        print(f"Procurei por:\n{settings.START_ALURA}\n{settings.END_ALURA}")

    if html_credly and re.search(settings.LIST_REGEX_CREDLY, readme_modificado):
        # Substitui apenas o que está entre as tags no readme_modificado
        bloco_credly = f"{settings.START_CREDLY}\n{html_credly}\n{settings.END_CREDLY}"
        readme_modificado = re.sub(settings.LIST_REGEX_CREDLY, lambda _: bloco_credly, readme_modificado)
        houve_alteracao = True
        # Salva no GitHub
        #github_bot.atualizar_readme(html_credly)
        print("✅ Badges injetadas com sucesso entre os marcadores!")
    else:
        print(f"⚠️ Erro: Marcadores não encontrados no README do usuário.")
        print(f"Procurei por:\n{settings.START_CREDLY}\n{settings.END_CREDLY}")

    if houve_alteracao and readme_modificado != readme_atual:
        github_bot.atualizar_readme(readme_modificado)
        print("🚀 README atualizado com sucesso no GitHub!")
    else:
        print("ℹ️ Nenhuma alteração necessária no README.")

'''
    if novo_readme_completo and re.search(LIST_REGEX, readme_atual):
        # Substitui apenas o que está entre as tags no readme_atual
        bloco_final = f"{START_SECTION}\n{novo_readme_completo}\n{END_SECTION}"
        novo_readme_completo = re.sub(LIST_REGEX, lambda _: bloco_final, readme_atual)
        # Salva no GitHub
        github_bot.atualizar_readme(novo_readme_completo)
        print("✅ Badges injetadas com sucesso entre os marcadores!")
    else:
        print(f"⚠️ Erro: Marcadores não encontrados no README do usuário.")
        print(f"Procurei por:\n{START_SECTION}\n{END_SECTION}")
        sys.exit(1)
'''