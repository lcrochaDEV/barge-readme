import os
import re

# Pega da ENV ou usa o valor padrão caso a ENV não esteja definida
START_SECTION = os.getenv("START_SECTION") or "<!--START_SECTION:badges-->"
END_SECTION = os.getenv("END_SECTION") or "<!--END_SECTION:badges-->"

URL_ALURA = "https://cursos.alura.com.br"

LIST_REGEX = f"{re.escape(START_SECTION)}?[\\s\\S]*?\w+{re.escape(END_SECTION)}"



