import time
import logging
import toml

from logging.handlers import TimedRotatingFileHandler

from function import Get_nodes
from function import Check_status_node
from function import runtime_check
from WorkWithJson import WorkWithJson
from TelegramBot.send_message import send_message

config_toml = toml.load('config.toml')
setting = WorkWithJson('settings.json')


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Handler for console output
log_s = logging.StreamHandler()
log_s.setLevel(logging.INFO)
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
log_s.setFormatter(formatter)
log.addHandler(log_s)

# Handler for file output that rotates daily
log_f = TimedRotatingFileHandler(
    "logs/main.log", 
    when="D",        # Rotate daily
    interval=1,      # Every 1 day
    backupCount=config_toml['logging']['backup_count_last_day']    # Keep logs for 7 days
)
log_f.setLevel(logging.DEBUG)
log_f.setFormatter(formatter)
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