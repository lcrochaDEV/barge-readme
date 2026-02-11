import os
import re

# Pega da ENV ou usa o valor padrão caso a ENV não esteja definida
START_SECTION = os.getenv("START_SECTION") or "<!--START_SECTION:badges-->"
END_SECTION = os.getenv("END_SECTION") or "<!--END_SECTION:badges-->"
LIST_REGEX = f"{re.escape(START_SECTION)}[\\s\\S]*?{re.escape(END_SECTION)}"

URL = os.getenv("URL_GENERIC") or ""
XPATH_A = os.getenv("XPATH_A") or ""
XPATH_B = os.getenv("XPATH_B") or ""
XPATH_C = os.getenv("XPATH_C") or ""


ALURA_USER = os.getenv("ALURA_USER") or "lcrochaDEV"
CREDLY_USER = os.getenv("CREDLY_USER") or "lcrochaDEV"
GENERIC_USER = os.getenv("GENERIC_USER") or "lcrochaDEV"

# --- CONFIGURAÇÕES ALURA ---
URL_ALURA = "https://cursos.alura.com.br"
# 1. Captura o que foi escrito no YAML (ou usa um padrão)
START_ALURA = os.getenv("START_ALURA") or "<!--START_SECTION_ALURA:badges-->"
END_ALURA = os.getenv("END_ALURA") or "<!--END_SECTION_ALURA:badges-->"
LIST_REGEX_ALURA = f"{re.escape(START_ALURA)}[\\s\\S]*?{re.escape(END_ALURA)}"

# --- CONFIGURAÇÕES CREDLY ---
URL_CREDLY = "https://www.credly.com"
# Marcadores para Credly (Dinâmicos)
START_CREDLY = os.getenv("START_CREDLY") or "<!--START_SECTION_CREDLY:badges-->"
END_CREDLY = os.getenv("END_CREDLY") or "<!--END_SECTION_CREDLY:badges-->"
LIST_REGEX_CREDLY = f"{re.escape(START_CREDLY)}[\\s\\S]*?{re.escape(END_CREDLY)}"

LIMITE = os.getenv("INPUT_NUMBER_LAST_BADGES") or "16"

