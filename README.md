# 🎓 Badges Updater

Este projeto automatiza a atualização de certificados de **Cursos e Formações** diretamente no seu perfil do GitHub. Ele utiliza Web Scraping para coletar suas conquistas recentes e as injeta de forma organizada entre marcadores específicos no seu `README.md`.

>[!IMPORTANT]
>Para criar um `README.md` de alto nível, vamos focar na clareza técnica e no visual. Essa aplicação utiliza **Selenium** (para o scraping), **Regex** (para injeção de conteúdo) e **GitHub Actions** (para automação), o documento precisa refletir essa robustez.

> [!CAUTION]
> Antes de qualquer ação faça um backup do seu README.md.

## ✨ Funcionalidades

* **Scraping Automatizado:** Utiliza Selenium para navegar no perfil publico de sua formação e capturar badges, links e títulos.
* **Controle de Fluxo Inteligente:** Exibe as 13 badges mais recentes e organiza o restante dentro de um menu expansível (`<details>`), mantendo o perfil limpo.
* **Injeção via Regex:** Identifica marcadores HTML específicos e substitui o conteúdo sem afetar o restante do seu arquivo.
* **GitHub Actions:** Roda de forma agendada ou manual sem que você precise executar o script localmente.

---

## 🚀 Como Configurar

### 1. Prepare o seu README
Adicione os seguintes marcadores no local onde deseja que as badges apareçam:

```html
<!--START_SECTION:badges-->
<!--END_SECTION:badges-->
```

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Selenium:** Para automação de navegação e coleta de dados.
* **Regex (Expressões Regulares):** Para manipulação precisa de strings.
* **PyGithub:** Para integração com a API do GitHub.

---

## 🏗️ Arquitetura do Projeto

O fluxo de dados segue a seguinte lógica:

1. **ControllerAPI:** Acessa o perfil da Alura e gera o HTML das tags.
2. **Lógica de Fluxo:** Se houver mais de 13 badges, as excedentes são colocadas em um bloco `<details>`.
3. **ControllerGithub:** Busca o conteúdo atual do seu repositório.
4. **Regex Engine:** Localiza o padrão `[\s\S]*?` entre os marcadores e realiza a substituição.

---

> [!NOTE]
> Todo esse repositório está baseado na plataforma de cursos ***Alura***, mas pode ser escalonado para qualquer outra formação que tenha seus certificados em uma página pública, seguindo as ideias aqui apresentadas de mapeamento de tags para scraping.
>
>Fico à disposição caso algum desenvolvedor queira escalar para outro nível esse simples repositório.

---

## ⚙ Configurções do git actions 

```yaml

name: Update Badges

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Get Alura Badges
        # Aqui ele chama o SEU repositório como se fosse uma biblioteca
        uses: lcrochaDEV/barge-readme@main
        with:
          username: 'guitarralcs'                             # O usuário Alura
          start_section: '<!--START_SECTION_ALURA:badges-->'  # Tag Inicio
          end_section: '<!--END_SECTION_ALURA:badges-->'      # Tag fim
          badge_limit: '55'                                   # O limite que ele desejar

```
>[!NOTE]
>Caso não queira uma tag personalizada, as padrão serão essas:
>
>```html
><!--START_SECTION:badges-->
><!--END_SECTION:badges-->
>```

## 📜 Créditos

Este projeto foi inspirado e utiliza conceitos baseados no excelente trabalho de:

👤 **pemtajo** - [GitHub Repository](https://github.com/pemtajo)

Agradecimentos especiais pela base lógica de atualização de perfis que serviu de fundação para esta implementação customizada.

---