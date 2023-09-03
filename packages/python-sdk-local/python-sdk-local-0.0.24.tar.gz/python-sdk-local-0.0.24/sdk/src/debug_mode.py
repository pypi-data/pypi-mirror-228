import json
import os
import sys
from dotenv import load_dotenv
load_dotenv()
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.Logger import Logger
sys.path.append(os.getcwd())
from python_sdk_local.sdk.src.LoggerOutputEnum import LoggerOutputEnum

PYTHON_SDK_LOCAL_COMPONENT_ID = 184
PYTHON_SDK_LOCAL_COMPONENT_NAME = 'python_sdk_local/src/debug_mode.py'
LOGGER_CONFIGURATION_JSON = '.logger.json'
LOGGER_MINIMUM_SEVERITY = os.getenv('LOGGER_MINIMUM_SEVERITY')

if not LOGGER_MINIMUM_SEVERITY:
    LOGGER_MINIMUM_SEVERITY = 0
else:
    LOGGER_MINIMUM_SEVERITY = int(LOGGER_MINIMUM_SEVERITY)


obj = {
    'component_id': PYTHON_SDK_LOCAL_COMPONENT_ID,
    'component_name': PYTHON_SDK_LOCAL_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'yoav.e@circ.zone'
}

logger = Logger.create_logger(object=obj)
class DebugMode:
    def __init__(self):
        self.logger_json = {}
        self._init()

    def _init(self):
        INIT_METHOD_NAME = "_init()"
        logger.start(INIT_METHOD_NAME)

        try:
            with open(LOGGER_CONFIGURATION_JSON, 'r') as file:
                self.logger_json = json.load(file)
        except Exception as e:
            logger.exception("got exception while reading json from file", object={'exception': e})
            logger.end(INIT_METHOD_NAME)
            return

        logger.end(INIT_METHOD_NAME)

    def fetch(self, component_id:str, logger_output: LoggerOutputEnum, severity_level:int):

        severity_level = max(severity_level, LOGGER_MINIMUM_SEVERITY)
        
        FETCH_METHOD_NAME = "fetch()"
        logger.start(FETCH_METHOD_NAME, object={'component_id': component_id, 'logger_output': str(logger_output), 'severity_level': severity_level})

        if component_id in self.logger_json:
            output_info = self.logger_json[component_id]
            if logger_output in output_info:
                result = severity_level >= output_info[logger_output]
                logger.end(FETCH_METHOD_NAME, object={'result': result})
                return result
        

        result = False
        logger.end(FETCH_METHOD_NAME, object={'result': result})
        return result