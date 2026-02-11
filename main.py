import sys
import re
from ControllerClass.ControllerAPI import ControllerAPI
from ControllerClass.ControllerGithub import ControllerGithub
import settings

if __name__ == "__main__":
    # Inicializa os controladores básicos
    # Note: Certifique-se que o ControllerAPI aceite username="" se for usar apenas o genérico
    bot = ControllerAPI(number_badges=int(settings.LIMITE))
    github_bot = ControllerGithub()

    try:
        readme_obj = github_bot.repo.get_contents("README.md")
        readme_atual = readme_obj.decoded_content.decode("utf-8")
    except Exception as e:
        print(f"❌ Erro ao acessar o README.md: {e}")
        sys.exit(1)

    readme_modificado = readme_atual
    houve_alteracao = False

    # --- 1. BLOCO ALURA ---
    # Só executa se houver URL_ALURA E os marcadores no README
    if settings.ALURA_USER and re.search(settings.LIST_REGEX_ALURA, readme_modificado):
        print("🔍 Buscando dados da Alura...")
        html_alura = bot.varrerDadosAlura(USER=settings.ALURA_USER)
        if html_alura:
            bloco_alura = f"{settings.START_ALURA}\n{html_alura}\n{settings.END_ALURA}"
            readme_modificado = re.sub(settings.LIST_REGEX_ALURA, lambda _: bloco_alura, readme_modificado)
            houve_alteracao = True
            print("✅ Seção Alura preparada!")
    else:
        print("⏭️ Pulando Alura (Usuário não definido ou marcadores ausentes).")

    # --- 2. BLOCO CREDLY ---
    if settings.CREDLY_USER and re.search(settings.LIST_REGEX_CREDLY, readme_modificado):
        print("🔍 Buscando dados do Credly...")
        html_credly = bot.varrerDadosCredly(USER=settings.CREDLY_USER)
        if html_credly:
            bloco_credly = f"{settings.START_CREDLY}\n{html_credly}\n{settings.END_CREDLY}"
            readme_modificado = re.sub(settings.LIST_REGEX_CREDLY, lambda _: bloco_credly, readme_modificado)
            houve_alteracao = True
            print("✅ Seção Credly preparada!")
    else:
        print("⏭️ Pulando Credly (Usuário não definido ou marcadores ausentes).")

    # --- 3. BLOCO GENERIC ---
    # Só executa se a URL genérica tiver sido preenchida no YAML/Settings
    if settings.GENERIC_USER and re.search(settings.LIST_REGEX, readme_modificado):
        print(f"🔍 Buscando dados genéricos em: {settings.URL}")
        html_generic = bot.varrerDadosGeneric(
            USER=settings.GENERIC_USER,
            url=settings.URL,
            XPATH_a=settings.XPATH_A,
            XPATH_b=settings.XPATH_B,
            XPATH_c=settings.XPATH_C
        )
        if html_generic:
            bloco_final = f"{settings.START_SECTION}\n{html_generic}\n{settings.END_SECTION}"
            readme_modificado = re.sub(settings.LIST_REGEX, lambda _: bloco_final, readme_modificado)
            houve_alteracao = True
            print("✅ Seção Generic preparada!")
    else:
        print("⏭️ Pulando Seção Genérica (URL não definida ou marcadores ausentes).")

    # Encerra o WebDriver
    bot.finalizar()

    # --- FINALIZAÇÃO ---
    if houve_alteracao and readme_modificado != readme_atual:
        github_bot.atualizar_readme(readme_modificado)
        print("🚀 README atualizado com sucesso no GitHub!")
    else:
        print("ℹ️ Nenhuma alteração realizada no README.")