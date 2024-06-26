import time
import logging
import toml
import requests
import datetime

from logging.handlers import TimedRotatingFileHandler

from TelegramBot.send_message import send_message

config_toml = toml.load('config.toml')

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
    "logs/function.log", 
    when="D",        # Rotate daily
    interval=1,      # Every 1 day
    backupCount=config_toml['logging']['backup_count_last_day']    # Keep logs for 7 days
)
log_f.setLevel(logging.DEBUG)
log_f.setFormatter(formatter)
log.addHandler(log_f)

def runtime_check(times: str) -> bool:
    time_now = datetime.datetime.now().utcnow().time()
    log.info(f"Get {times} now time {time_now}")

    if times == '':
        return True
    
    elif times != '':
        
        for time in times.split(','):
            time = time.split(":")
            
            if len(time) != 2:
                time.append(0)
                
            log.info(f"{datetime.timedelta()} <= {datetime.timedelta(hours=time_now.hour, minutes=time_now.minute) - datetime.timedelta(hours=int(time[0]), minutes=int(time[1]))} < {datetime.timedelta(minutes=config_toml['time_check'])}")
            
            if datetime.timedelta() <= datetime.timedelta(hours=time_now.hour, minutes=time_now.minute) - datetime.timedelta(hours=int(time[0]), minutes=int(time[1]))  < datetime.timedelta(minutes=config_toml['time_check']):
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

def add_config_nodeId_to_setting(settings: dict) -> None:
    
    log.info(f"# ======= Check status node_id ======= #")
    for number_node in config_toml['node_ids']:
        node_id = config_toml['node_ids'][number_node]

        log.info(f"{number_node}. {node_id}")
        if node_id not in settings:
            settings[node_id] = {}

def Check_status_node(
        log_id: int, 
        data: dict
        ) -> None:
    
    # add_config_nodeId_to_setting(settings=settings)

    for node in data['nodes']:
        node_id = node['node_id']
        status = node['status']

        if node_id in config_toml['node_ids'].values():
            log.debug(f"Node_id: {node_id}\nStatus: {status}\n")

            if status == "DEGRADED" or status == "DOWN":
                log.info(f"Node ID: {node_id}\n"
                    f"Status: {status}")

                message = (f"Node ID: <code>{node_id}</code>\n"
                    f"I get status: <code>{status}</code>")
                
                send_message(log_id=log_id, message=message)
                