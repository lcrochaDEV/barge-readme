# 🎓 Badges Updater

Este projeto automatiza a atualização de certificados de **Cursos e Formações** diretamente no seu perfil do GitHub. Ele utiliza Web Scraping para coletar suas conquistas recentes e as injeta de forma organizada entre marcadores específicos no seu `README.md`.

> [!IMPORTANT]
> Para criar um `README.md` de alto nível, vamos focar na clareza técnica e no visual. Essa aplicação utiliza **Selenium** (para o scraping), **Regex** (para injeção de conteúdo) e **GitHub Actions** (para automação), o documento precisa refletir essa robustez.

> [!CAUTION]
> Antes de qualquer ação faça um backup do seu README.md.

## ✨ Funcionalidades

* **Scraping Multi-Plataforma:** Suporte integrado para **Alura** e **Credly**, capturando badges de cursos, bootcamps e certificações internacionais.
* **Carregamento Dinâmico de Conteúdo:** Utiliza automação para gerenciar scrolls e expansões de lista, garantindo a captura completa de portfólios extensos.
* **Controle de Fluxo Inteligente:** Exibe as 13 badges mais recentes e organiza o restante dentro de um menu expansível (`<details>`), mantendo a estética do perfil limpa.
* **Injeção via Regex:** Identifica marcadores HTML específicos e substitui o conteúdo de forma atômica, sem afetar outras seções do documento.

---

## 🚀 Como Configurar

### 1. Prepare o seu README

Adicione os seguintes marcadores no local onde deseja que as badges apareçam (você pode criar seções separadas para diferentes fontes):

```html

```

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Selenium (Headless Mode):** Automação de navegação otimizada para execução em servidores (GitHub Actions).
* **WebDriver Manager:** Gerenciamento automatizado de drivers para o Google Chrome.
* **Regex (Expressões Regulares):** Manipulação precisa de blocos de texto e padrões Markdown.

---

## 🏗️ Arquitetura do Projeto

O fluxo de dados segue a lógica de **Extração Relativa por Card**:

1. **ControllerAPI:** Responsável por instanciar o navegador, gerenciar a sessão e realizar o carregamento total do DOM.
2. **Card Parser:** Itera sobre cada container de certificado de forma independente, extraindo o primeiro nó de texto e imagem correspondente, o que evita inconsistências de sincronização.
3. **Lógica de Fluxo:** Aplica o fatiamento de arrays para separar a exibição direta da exibição oculta via tags `<details>`.
4. **Git Engine:** Realiza a leitura do arquivo `README.md` e aplica a substituição do conteúdo entre os marcadores configurados.

---

> [!NOTE]
> O projeto foi estruturado para ser escalonável. Através dos métodos genéricos de captura, é possível adaptar a ferramenta para outras plataformas de ensino que disponibilizem portfólios públicos.

---

## ⚙ Configurações do GitHub Actions

Exemplo de workflow para múltiplas fontes de badges:

```yaml
name: Update Badges@v1

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
        uses: lcrochaDEV/barge-readme@beta-version
        with:
          username_alura: 'guitarralcs'
          username_credly: 'lucas-rocha.e2b61fbf'
          badge_limit: '55'

          #username_generic: 'guitarralcs'
          #badge_limit: '15'
          ## Ele só preenche o que quiser usar:
          #generic_url: 'https://www.exemplo.com/certificados'
          #xpath_a: '//a[@class="link"]'
          #xpath_b: '//img[@class="icon"]'
          #xpath_c: '//span[@class="title"]'
          


#<!--START_SECTION_ALURA:badges-->
#<!--END_SECTION_ALURA:badges-->

```

## 📜 Créditos

Este projeto foi inspirado e utiliza conceitos baseados no excelente trabalho de:

👤 **pemtajo** - [GitHub Repository](https://github.com/pemtajo)

Agradecimentos especiais pela base lógica de atualização de perfis que serviu de fundação para esta implementação customizada.