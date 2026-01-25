import os
import re

# Pega da ENV ou usa o valor padrão caso a ENV não esteja definida
USER = os.getenv("ALURA_USER") or "lcrochaDEV"
START_SECTION = os.getenv("START_SECTION") or "<!--START_SECTION:badges-->"
END_SECTION = os.getenv("END_SECTION") or "<!--END_SECTION:badges-->"
LIMITE = os.getenv("INPUT_NUMBER_LAST_BADGES") or "16"

URL_ALURA = "https://cursos.alura.com.br"

LIST_REGEX = f"{re.escape(START_SECTION)}[\\s\\S]*?{re.escape(END_SECTION)}"



