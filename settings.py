import os
import re

# Pega da ENV ou usa o valor padrão caso a ENV não esteja definida
START_COMMENT = os.getenv("START_MARKER") or "<!--START_MARKER:badges-->"
END_COMMENT = os.getenv("END_MARKER") or "<!--END_MARKER:badges-->"

URL_ALURA = "https://cursos.alura.com.br"

LIST_REGEX = f"{re.escape(START_COMMENT)}[\\s\\S]*?{re.escape(END_COMMENT)}"



