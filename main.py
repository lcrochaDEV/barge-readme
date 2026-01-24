import os
import sys
from ControllerClass.ControllerAPI import ControllerAPI
from ControllerClass.ControllerGithub import ControllerGithub
from settings import START_COMMENT, END_COMMENT

if __name__ == "__main__":
    # 1. Captura de Variáveis de Ambiente
    user = os.getenv("ALURA_USER")
    start_m = os.getenv("START_MARKER", START_COMMENT)
    end_m = os.getenv("END_MARKER", END_COMMENT)
    limit = os.getenv("INPUT_NUMBER_LAST_BADGES", "16")

    if not user:
        print("❌ Erro: ALURA_USER não configurado.")
        sys.exit(1)

    # 2. Inicializa o Bot da API e busca as badges
    # (Supondo que seu varrerDadosAlura retorne apenas a string das badges ou o README completo)
    bot = ControllerAPI(username=user, start_marker=start_m, end_marker=end_m, number_badges=int(limit))
    
    # 3. Inicializa o Bot do GitHub
    github_bot = ControllerGithub()
    
    # 4. Busca o conteúdo ATUAL do README para validar as tags
    try:
        # Pega o conteúdo direto do repo do amigo via API
        readme_obj = github_bot.repo.get_contents("README.md")
        readme_atual = readme_obj.decoded_content.decode("utf-8")
    except Exception as e:
        print(f"❌ Erro ao buscar README.md: {e}")
        sys.exit(1)

    # 5. Validação das Tags (Crucial para o amigo não quebrar o bot)
    if start_m not in readme_atual or end_m not in readme_atual:
        print(f"❌ Erro: Marcadores não encontrados no README.md")
        print(f"Certifique-se de que existam:\n{start_m}\n{end_m}")
        sys.exit(1)

    # 6. Gera o novo conteúdo
    # Aqui seu bot deve injetar as badges entre as tags no readme_atual
    novo_readme_completo = bot.gerar_novo_conteudo(readme_atual) 

    # 7. Salva via API
    github_bot.atualizar_readme(novo_readme_completo)