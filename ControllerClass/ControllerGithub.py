from github import Github
import os

class ControllerGithub:
    def __init__(self):
        # O GITHUB_TOKEN é fornecido automaticamente pelo GitHub Actions
        self.token = os.getenv("GITHUB_TOKEN")
        self.repo_name = os.getenv("GITHUB_REPOSITORY") # Pega "usuario/repo" automaticamente
        self.g = Github(self.token)
        self.repo = self.g.get_repo(self.repo_name)

    def atualizar_readme(self, novo_conteudo):
        try:
            contents = self.repo.get_contents("README.md")
            self.repo.update_file(
                path=contents.path,
                message="docs: update alura badges [skip ci]",
                content=novo_conteudo,
                sha=contents.sha,
                branch="main"
            )
            print("✅ README.md atualizado via API com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao atualizar via API: {e}")