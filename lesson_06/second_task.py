import datetime
GLOBAL_CONFIG = {"feature_a": True, "max_retries": 3}


class Configuration:
    def __init__(self, updates: dict, validator=None):
        self.updates = updates
        self.validator = validator
        self.old_config = GLOBAL_CONFIG.copy()
        if not self.validator:
            raise Exception("Обновления не прошли валидацию")

    def __enter__(self):
        global GLOBAL_CONFIG
        for key, value in self.updates.items():
            if key in GLOBAL_CONFIG:
                GLOBAL_CONFIG[key] = value
        with open('global_config_changes_logs.txt', 'a') as file:
            file.write(f"Date log: {datetime.datetime.now()}, Changes: {str(GLOBAL_CONFIG)}\n") # добавил логирование изменений
        print(f"Значение GLOBAL CONFIG сменилось с {self.old_config} на {GLOBAL_CONFIG}")




    def __exit__(self, exc_type, exc_value, traceback):
        global GLOBAL_CONFIG
        GLOBAL_CONFIG = self.old_config.copy()
        print(f"\nGLOBAL_CONFIG вернулся на старое значение {GLOBAL_CONFIG}")

def validate_config(config):
    # Ensure max_retries >= 0
    return config.get("max_retries", 0) >= 0

updates = {'max_retries': 5, 'feature_a': False}

with Configuration(updates, validate_config(updates)):
    print('test')

