import json
import logging
import pprint
import signal
import subprocess

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Tuple, Union

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from config import CHECKED_ENVIRONMENT_VARIABLES, OOKLA_SPEEDTEST_CLI_EULA_FILE, Config
from db_models import Result
from engine import engine
from log import logger

config = Config()


def run_command(cmd: str, debug: bool = True) -> Tuple[bytes, bytes]:
    """Run the provided command.

    :param cmd: The command to run
    :param debug: Debug flag; if true, send the output stream to the logger debug and error stream to logger error.
    :return: Tuple of the output stream and error stream
    """
    logger.debug(f'Running command: [{cmd}]')
    outstream, errstream = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
    if debug:
        logger.debug(f'Command output: {outstream}')
        if errstream:
            logger.error(f'Command error: {errstream}')
    return outstream, errstream


def accept_ookla_speedtest_eula() -> None:
    """Accept the OOKLA Speedtest.net EULA."""
    outstream, errstream = run_command(f'speedtest --accept-license', debug=False)
    logger.debug(f'Accept EULA output: {outstream}')
    if errstream:
        logger.error(f'Accept EULA error: {errstream}')


def get_data(server_id: str) -> Dict[str, Union[Dict[str, Any], str]]:
    """Get the data from running `speedtest` CLI.

    :param server_id: The server ID to use during the speedtest.
    :return: The loaded JSON data as a dict
    """
    outstream, errstream = run_command(f'speedtest --server-id={server_id} --format=json')
    data = json.loads(outstream)
    return data


def job(server_id: str = None) -> None:
    """The main job; will get the data from the provided server id, and update the sheet with a new row.

    :param server_id: The server ID to query
    """
    logger.info('==========================================')
    logger.info('Starting next run...')

    logger.info('Getting data...')
    data = get_data(server_id=server_id)
    dl_bandwidth = data.get('download', {}).get('bandwidth', 0) / 125000
    ul_bandwidth = data.get('upload', {}).get('bandwidth', 0) / 125000
    result_url = data.get('result', {}).get('url', 'Unknown')
    logger.info(f'{dl_bandwidth} Mbps / {ul_bandwidth} Mbps (D/U) --> {result_url}')
    logger.debug('Data:')
    logger.debug(pprint.pformat(data, indent=4))

    # Update DB
    Result.add_data(engine=engine, data=data)


if __name__ == '__main__':
    ##
    # Accept Speedtest.net EULA
    ##
    if not Path(OOKLA_SPEEDTEST_CLI_EULA_FILE).expanduser().exists():
        logger.info('OOKLA Speedtest.net EULA file *NOT* found, automatically accepting EULA...')
        accept_ookla_speedtest_eula()
        logger.info('OOKLA Speedtest.net EULA accepted!')
    else:
        logger.info('OOKLA Speedtest.net EULA file found, proceeding...')

    ##
    # Validate Environment Variables
    ##
    DEBUG = config.get('DEBUG', 'false').lower() == 'true'
    logger.info(f'DEBUG: {DEBUG}\n')
    logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

    SCHEDULE_INTERVAL = int(config.get('SCHEDULE_INTERVAL', default='0'))
    CRON_EXPRESSION = config.get('CRON_EXPRESSION')
    SERVER_ID = config.get('SERVER_ID')
    DB_HOSTNAME = config.get('DB_HOSTNAME')
    DB_USERNAME = config.get('DB_USERNAME')
    DB_PASSWORD = config.get('DB_PASSWORD')
    DB_DATABASE = config.get('DB_DATABASE')

    # Env Var input validation (basic.)
    for envvar_name in CHECKED_ENVIRONMENT_VARIABLES:
        envvar_value = locals()[envvar_name]
        if not envvar_value:
            logger.info('The following environment variable is not set correctly.')
            padding = ' ' * (32 - len(envvar_name))
            logger.info(f'    {envvar_name}:{padding}{envvar_value}')
            logger.info('')
            logger.info('Please check the environment variables and start the container again. Exiting.')
            exit(1)

    # If both are set, exit; we only want one set.
    if not SCHEDULE_INTERVAL and not CRON_EXPRESSION:
        logger.critical('Set either `CRON_EXPRESSION` or `SCHEDULE_INTERVAL`, but not both. Exiting.')
        exit(1)

    ##
    # Display Running Variables
    ##
    logger.debug('Running with the below environment variables:')
    for envvar_name in CHECKED_ENVIRONMENT_VARIABLES:
        envvar_value = locals()[envvar_name]
        padding = ' ' * (32 - len(envvar_name))
        logger.info(f'    {envvar_name}:{padding}{envvar_value}')

    ##
    # Clients
    ##
    logger.info('Creating scheduler...')
    scheduler = BlockingScheduler()

    def gracefully_exit(signum, frame):
        logger.info('Stopping scheduler...')
        scheduler.shutdown()
        logger.info('Scheduler shutdown.')

    logger.info('Adding shutdown signal handlers...')
    signal.signal(signal.SIGINT, gracefully_exit)
    signal.signal(signal.SIGTERM, gracefully_exit)

    if CRON_EXPRESSION:
        logger.info(f'Adding job to run on the following cron schedule: {CRON_EXPRESSION}')
        scheduler.add_job(
            func=lambda: job(server_id=SERVER_ID),
            trigger=CronTrigger.from_crontab(CRON_EXPRESSION),
        )
    elif SCHEDULE_INTERVAL:
        logger.info(f'Adding job to run every {SCHEDULE_INTERVAL} minutes...')
        scheduler.add_job(
            func=lambda: job(server_id=SERVER_ID),
            trigger='interval',
            minutes=SCHEDULE_INTERVAL,
            next_run_time=datetime.now() + timedelta(seconds=1),
        )
    else:
        logger.critical('No schedule information set.')
        logger.critical('Set either `CRON_EXPRESSION` or `SCHEDULE_INTERVAL` and restart the application.')
        exit(1)
    logger.info(f'Starting job [{scheduler}] ...')
    scheduler.start()
