import os
from ControllerClass.ControllerAPI import ControllerAPI
from settings import START_COMMENT, END_COMMENT

if __name__ == "__main__":
    # Pega o usuário das variáveis de ambiente do GitHub Actions
    user = os.getenv("ALURA_USER", "lucasDEV")
    # Aqui capturamos as ENVs. Se não existirem, o settings.py já tratou o fallback.
    start_m = os.getenv("START_MARKER", START_COMMENT)
    end_m = os.getenv("END_MARKER", END_COMMENT)
    limit = os.getenv("INPUT_NUMBER_LAST_BADGES", "16")
    
    bot = ControllerAPI(username=user, start_marker=start_m, end_marker=end_m, number_badges=int(limit))
    bot.varrerDadosAlura()