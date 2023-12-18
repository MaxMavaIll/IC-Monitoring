import time
import logging
import toml
import requests
import datetime

from logging.handlers import RotatingFileHandler

from TelegramBot.send_message import send_message

config_toml = toml.load('config.toml')

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

log_s = logging.StreamHandler()
log_s.setLevel(logging.INFO)
formatter2 = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s")
log_s.setFormatter(formatter2)

log_f = RotatingFileHandler(
    f"logs/{__name__}.log",
    maxBytes=config_toml['logging']['max_log_size'] * 1024 * 1024, 
    backupCount=config_toml['logging']['backup_count'])
log_f.setLevel(logging.DEBUG)
formatter2 = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s")
log_f.setFormatter(formatter2)

log.addHandler(log_s)
log.addHandler(log_f)

def runtime_check(times: str) -> bool:
    time_now = datetime.datetime.now().utcnow().time()
    log.info(f"Get {times} now time {time_now}")

    if times == '':
        return True
    
    elif times != '':
        
        for time in times.split(','):
            log.debug(f"ID: {id} -> {datetime.timedelta()} <= {datetime.timedelta(hours=time_now.hour, minutes=time_now.minute) - datetime.timedelta(hours=int(time))} <= {datetime.timedelta(minutes=config_toml['time_check'])}")
            
            if datetime.timedelta() <= datetime.timedelta(hours=time_now.hour, minutes=time_now.minute) - datetime.timedelta(hours=int(time))  <= datetime.timedelta(minutes=config_toml['time_check']):
                log.info(f"Get True")
                return True
    
    log.info(f"Get False")
    return False

def Get_nodes(log_id: int) -> dict:
    log.info("Get nodes data")

    url = f'https://ic-api.internetcomputer.org/api/v3/nodes'

    response = requests.get(url=url)
    

    if response.status_code == 200:
        log.info(f"ID: {log_id} -> "
            f"Status {response.status_code}")

        data = response.json()
        return data
    
    else:
        log.error(f"ID: {log_id} -> "
            f"Повідомлення отримало код {response.status_code}")
        log.error(response.text)
        log.debug(f"ID: {log_id} -> url: {url}")

def add_config_nodeId_to_setting(settings: dict):
    for node_id in config_toml['node_ids']:
        if node_id not in settings:
            settings[node_id] = {}

def Check_status_node(log_id: int, 
        data: dict,
        settings: dict) -> None:
    
    add_config_nodeId_to_setting(settings=settings)

    for node in data['nodes']:
        node_id = node['node_id']
        status = node['status']

        if node_id in settings:
            if settings[node_id] == {}:
                settings[node_id]['status'] = ""

            if status != settings[node_id]['status']:
                message = (f"Node ID: <code>{node_id}</code>\n"
                    f"I get status: <code>{status}</code>")
                
                send_message(log_id=log_id, message=message)
                
                settings[node_id]['status'] = status