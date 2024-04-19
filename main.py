import time
import logging
import toml

from logging.handlers import RotatingFileHandler

from function import Get_nodes
from function import Check_status_node
from function import runtime_check
from WorkWithJson import WorkWithJson
from TelegramBot.send_message import send_message

config_toml = toml.load('config.toml')
setting = WorkWithJson('settings.json')


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

log_s = logging.StreamHandler()
log_s.setLevel(logging.INFO)
formatter2 = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s")
log_s.setFormatter(formatter2)

log_f = RotatingFileHandler(
    f"logs/main.log",
    maxBytes=config_toml['logging']['max_log_size'] * 1024 * 1024, 
    backupCount=config_toml['logging']['backup_count'])
log_f.setLevel(logging.DEBUG)
formatter2 = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s")
log_f.setFormatter(formatter2)

log.addHandler(log_s)
log.addHandler(log_f)


def main():
    while True:
        settings = setting.get_json()
        answer = Get_nodes(log_id=settings['id'])

        Check_status_node(log_id=settings['id'], data=answer)
        

        if config_toml['tg_bot']['lighthouse']['enable'] and runtime_check(config_toml['tg_bot']['lighthouse']['time']):
            send_message(log_id=settings['id'], message=config_toml['tg_bot']['lighthouse']['message'])
            
        settings['id'] += 1
        setting.set_json(settings)
        log.info(f"Wait {config_toml['time_check']} min")
        time.sleep(config_toml['time_check'] * 60)


if __name__ == "__main__":
    main()