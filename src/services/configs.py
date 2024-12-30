import logging
import logging.config
import yaml
from utils.generate_logs import generate_logs

# Inicializando arquivos de logs
generate_logs();

# Carregar configuração do arquivo YAML
with open('./services/configs.logs.yaml', 'r') as file:
    config = yaml.safe_load(file)
    logging.config.dictConfig(config)

# Criar loggers específicos
users_logger = logging.getLogger("users")
exercices_logger = logging.getLogger("exercices")
workouts_logger = logging.getLogger("workouts")
plans_logger = logging.getLogger("plans")
workout_exercices_logger = logging.getLogger("workout_exercices")
plan_workouts_logger = logging.getLogger("plan_workouts")
user_plans_logger = logging.getLogger("user_plans")